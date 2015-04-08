#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from movimento.models import Produtos
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import ugettext_lazy as _


class Venda(models.Model):
    u""" 
    Classe Venda. 
    Criada para registrar todas as vendas efetivadas no estabelecimento.

    Criada em 05/10/2014. 
    """
    total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Total (R$)"), help_text=u'Valor total da venda.')
    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data da venda"))
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=_(u"Desconto (%)"), help_text=_(u"Desconto sob o valor total da venda."))
    status = models.BooleanField(default=False, verbose_name=_(u"Cancelada?"), help_text=_(u"Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados."))
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name=_(u"Cliente?"))
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, verbose_name=_(u"Forma de pagamento"))
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=_(u"Grupo de encargo"), on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"), help_text=_(u"Descreva na área as informações relavantes da venda."))
    pedido = models.CharField(max_length=1, blank=True, choices=((u'S', _(u"Sim")), (u'N', _(u"Não")),), verbose_name=_(u"Pedido?")) 
    status_pedido = models.BooleanField(default=False, verbose_name=_(u"Pedido confirmado?"), help_text=_(u"Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado."))

    def __unicode__(self):
        return u'%s' % (self.id)


    def clean(self):
        """ 
        Bloqueia o registro de uma venda quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar uma venda é necessário ter o caixa aberto."))


    def clean_fields(self, *args, **kwargs):
        """ 
        Bloqueia o cancelamento de uma venda quando já há pagamentos no caixa.
        """

        contas_receber = ContasReceber.objects.filter(vendas__pk=self.pk)
        venda_movimento_financeiro = ParcelasContasReceber.objects.filter(contas_receber=contas_receber, status=True).select_related('contas_receber__contasreceber').values_list('status').exists()
        if self.status and venda_movimento_financeiro:
            raise ValidationError({'status': [_(u"Venda não pode ser cancelada. Já há pagamento feito para esta venda. [Conta a Receber: %(conta_receber)s]") % {'conta_receber': contas_receber[0]},]})


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma venda.
        """
        data = datetime.date.today()
        
        if self.pk:

            status_antigo = Venda.objects.get(pk=self.pk)
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
            
            # trata cancelamento de venda/pedido de venda efetuada
            if not status_antigo.status and self.status:
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


    def __unicode__(self):
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


    def clean_fields(self, *args, **kwargs):
        """
        Método que trata o movimento no estoque.
        """
        quant_produto_estoque = Produtos.objects.filter(pk=self.produto.pk).values_list('quantidade')[0][0]
        if self.quantidade > quant_produto_estoque:
            raise ValidationError({'quantidade': ["Há somente %(quantidade)s unidade(s) deste produto em estoque." % {'quantidade': quant_produto_estoque},]})



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_receber.models import ContasReceber, ParcelasContasReceber
