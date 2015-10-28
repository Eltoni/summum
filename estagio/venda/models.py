#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente, EnderecoEntregaCliente
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from movimento.models import Produtos
from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from configuracoes.models import Parametrizacao
from utilitarios.funcoes_data import datetime_settings_timezone
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Venda(models.Model):
    u""" 
    Classe Venda. 
    Criada para registrar todas as vendas efetivadas no estabelecimento.

    Criada em 05/10/2014. 
    """
    total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Total (R$)"), help_text=u'Valor total da venda.')
    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data da venda"))
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=_(u"Desconto (%)"), help_text=_(u"Desconto sob o valor total da venda."))
    status = models.BooleanField(default=False, verbose_name=_(u"Cancelado?"), help_text=_(u"Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados."))
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name=_(u"Cliente"))
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, verbose_name=_(u"Forma de pagamento"))
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=_(u"Grupo de encargo"), on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"), help_text=_(u"Descreva na área as informações relavantes da venda."))
    pedido = models.CharField(max_length=1, blank=True, choices=((u'S', _(u"Sim")), (u'N', _(u"Não")),), verbose_name=_(u"Pedido?")) 
    status_pedido = models.BooleanField(default=False, verbose_name=_(u"Pedido confirmado?"), help_text=_(u"Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado."))
    vendedor = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name=_(u"Vendedor"))

    class Meta:
        verbose_name = _(u"Venda")
        verbose_name_plural = _(u"Vendas")
        permissions = ((u"pode_exportar_venda", _(u"Exportar Vendas")),)

    def __str__(self):
        return u'%s' % (self.id)


    def vendedor_associado(self):
        if self.vendedor:
            return u"<b>%s (%s %s)</b>" % (self.vendedor, self.vendedor.first_name, self.vendedor.last_name)
        return '-'
    vendedor_associado.allow_tags = True
    vendedor_associado.short_description = _(u"Vendedor")


    def clean(self):
        """ 
        Bloqueia o registro de uma venda quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar uma venda é necessário ter o caixa aberto."))


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma venda.
        """
        data = datetime.datetime.utcnow().replace(tzinfo=utc)
        
        if self.pk:

            conta_gerada = ContasReceber.objects.filter(vendas=self.pk).exists()
            super(Venda, self).save(*args, **kwargs)

            # Gera financeiro somente se venda for confirmada
            if self.pedido == 'N' and not conta_gerada or (self.status_pedido and not conta_gerada):

                # Descrição informada no contas à receber
                descricao = _(u"Conta aberta proveniente de venda %(venda)s") % {'venda': self}

                # Insere o contas à receber
                venda = ContasReceber(data=data, 
                                    valor_total=self.total, 
                                    descricao=descricao,
                                    vendas=self, 
                                    cliente=self.cliente, 
                                    forma_pagamento=self.forma_pagamento, 
                                    grupo_encargo=self.grupo_encargo, 
                                    status=False
                                    )
                venda.save()
            
            try:
                cancela_venda = self.botao_acionado
            except:
                cancela_venda = None

            # trata cancelamento de venda/pedido de venda efetuada
            if not self.status and cancela_venda == '_addcancelavenda':
                # Define a venda/pedido de venda com status cancelado
                self.status = True
                self.save()

                # Numa venda cancelada: acrescenta a quantidade dos produtos cancelados novamente ao estoque.
                for i in ItensVenda.objects.filter(vendas=self.pk).values_list('id', 'produto', 'quantidade'):
                    produto = Produtos.objects.get(pk=i[1])
                    produto.quantidade = produto.quantidade + i[2]
                    produto.save()

                    # desativa a movimentação feita dos itens de venda
                    item_venda = ItensVenda.objects.get(pk=i[0])
                    item_venda.remove_estoque = False
                    item_venda.save()
                
                if conta_gerada:
                    # Fecha a conta à receber
                    conta = ContasReceber.objects.get(vendas=self.pk)
                    conta.status = True
                    conta.save()
        
        else:

            # Chama a função save original para o save atual do modelo
            super(Venda, self).save(*args, **kwargs)



@python_2_unicode_compatible
class ItensVenda(models.Model):
    u""" 
    Classe ItensVenda. 
    Inline criada para ser exibida na página de vendas.
    Nesta, todos os itens de uma venda são registrados.
    
    Criada em 05/10/2014. 
    """

    quantidade = models.IntegerField(verbose_name=_(u"Quantidade"))
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor unitário (R$)"))
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Total (R$)"))
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=_(u"Desconto (%)"))
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, verbose_name=_(u"Produto"))
    vendas = models.ForeignKey(Venda, on_delete=models.PROTECT, verbose_name=_(u"Venda"))
    remove_estoque = models.BooleanField(default=False, verbose_name=_(u"Removido do estoque?"))

    class Meta:
        verbose_name = _(u"Item de Venda")
        verbose_name_plural = _(u"Itens de Venda")


    def __str__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a remoção da quantidade de produtos ao estoque.
        """
        if self.pk is None:
            
            # Subtrai a quantidade de produtos vendidos com a que já existe no estoque
            super(ItensVenda, self).save(*args, **kwargs)
            self.remove_estoque = True
            self.save()
            produto = Produtos.objects.get(pk=self.produto.pk)
            produto.quantidade = produto.quantidade - self.quantidade
            produto.save()

        else:

            super(ItensVenda, self).save(*args, **kwargs)


    # def clean_fields(self, *args, **kwargs):
    #     """
    #     Método que trata o movimento no estoque.
    #     """
    #     quant_produto_estoque = Produtos.objects.filter(pk=self.produto.pk).values_list('quantidade')[0][0]
    #     if self.pk is None and self.quantidade > quant_produto_estoque:
    #         raise ValidationError({'quantidade': ["Há somente %(quantidade)s unidade(s) deste produto em estoque." % {'quantidade': quant_produto_estoque},]})



@python_2_unicode_compatible
class EntregaVenda(models.Model):
    status = models.BooleanField(default=False, verbose_name=_(u"Entrega agendada?"))
    endereco = models.ForeignKey(EnderecoEntregaCliente, null=True, blank=True, on_delete=models.PROTECT, verbose_name=_(u"Endereço"))
    data = models.DateTimeField(null=True, blank=True, verbose_name=_(u"Data de entrega"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"), help_text=_(u"Descreva na área as informações relavantes da entrega."))
    posicao = GeopositionField(blank=True, verbose_name=_(u"Posição"))
    venda = models.OneToOneField(Venda, null=True, blank=True, verbose_name=_(u"Venda"))
    # status_entrega = models.CharField(max_length=1, blank=True, choices=((u'1', _(u"Realizada")), (u'2', _(u"Em andamento")), (u'3', _(u"Atrasada")),), verbose_name=_(u"Status da entrega")) 

    class Meta:
        verbose_name = _(u"Entrega")
        verbose_name_plural = _(u"Entregas")
        permissions = ((u"pode_exportar_entregavenda", _(u"Exportar Entregas")),)

    def __str__(self):
        return u'%s' % (self.id)


    def clean_fields(self, *args, **kwargs):

        quantidade = Parametrizacao.objects.get().intervalo_dias_entrega_venda
        venda = Venda.objects.get(pk=self.venda.pk)
        data_minima_para_entrega = datetime_settings_timezone(venda.data) + datetime.timedelta(days=quantidade)

        # Data de entrega não pode ser menor que data de venda + quantidade de dias para entrega (configurada nas parametrizações do sistema)
        if self.data and self.data < data_minima_para_entrega:
            raise ValidationError({'data': [_(u"Data de entrega inválida. Data mínima para entrega dos produtos: %(data_minima_entrega)s") % {'data_minima_entrega': data_minima_para_entrega.strftime('%d/%m/%Y às %H:%M:%S')},]})



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_receber.models import ContasReceber, ParcelasContasReceber
