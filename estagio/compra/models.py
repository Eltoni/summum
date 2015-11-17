#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from movimento.models import Produtos
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Compra(models.Model):
    u""" 
    Classe Compra. 
    Criada para registrar todas as compras efetivadas no estabelecimento.

    Criada em 15/06/2014. 
    """
    total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Total (R$)"), help_text=_(u"Valor total da compra."))
    data_compra = models.DateTimeField(null=True, verbose_name=_(u"Data da compra"))
    data_pedido = models.DateTimeField(null=True, verbose_name=_(u"Data do pedido"))
    data_cancelamento = models.DateTimeField(null=True, verbose_name=_(u"Data do cancelamento"))
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=_(u"Desconto (%)"), help_text=_(u"Desconto sob o valor total da compra."))
    status = models.BooleanField(default=False, verbose_name=_(u"Cancelado?"), help_text=_(u"Indica se o status da compra está ativo ou cancelada."))
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name=_(u"Fornecedor"))
    forma_pagamento = models.ForeignKey(FormaPagamento, verbose_name=_(u"Forma de pagamento"), on_delete=models.PROTECT)
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=_(u"Grupo de encargo"), on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"), help_text=_(u"Descreva na área as informações relavantes da compra."))
    pedido = models.CharField(max_length=1, blank=True, choices=((u'S', _(u"Sim")), (u'N', _(u"Não")),), verbose_name=_(u"Pedido?")) 
    status_pedido = models.BooleanField(default=False, verbose_name=_(u"Pedido confirmado?"), help_text=_(u"Caso confirmado, os itens financeiros serão gerados e o estoque movimentado."))
    
    class Meta:
        verbose_name = _(u"Compra")
        verbose_name_plural = _(u"Compras")
        permissions = ((u"pode_exportar_compra", _(u"Exportar Compras")),)

    def __str__(self):
        return u'%s' % (self.id)


    def formata_data_compra(self):
        if self.data_compra:
            return self.data_compra
        return '-'
    formata_data_compra.allow_tags = True
    formata_data_compra.short_description = _(u"Data da compra")
    formata_data_compra.admin_order_field = 'data_compra'


    def conta_associada(self):
        try:
            conta = ContasPagar.objects.get(compras__pk=self.pk).pk
        except: 
            conta = None

        if conta:
            url = reverse("admin:contas_pagar_contaspagar_change", args=[conta])
            return u"<a href='%s'>%s</a>" % (url, conta)
        return '-'
    conta_associada.allow_tags = True
    conta_associada.short_description = _(u"Conta a pagar")
    conta_associada.admin_order_field = 'contas_pagar'


    def clean(self):
        """ 
        Bloqueia o registro de uma compra quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar uma compra é necessário ter o caixa aberto."))


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma compra.
        """

        if self.pk:

            conta_gerada = ContasPagar.objects.filter(compras=self.pk).exists()
            super(Compra, self).save(*args, **kwargs)

            # Gera financeiro somente se compra for confirmada
            if self.pedido == 'N' and self.data_compra and not conta_gerada or (self.status_pedido and not conta_gerada):

                # Descrição informada no contas à pagar
                descricao = _(u"Conta aberta proveniente de compra %(compra)s") % {'compra': self}

                # Insere o contas à pagar
                conta = ContasPagar(data=self.data_compra, 
                                    valor_total=self.total, 
                                    descricao=descricao,
                                    compras=self, 
                                    fornecedores=self.fornecedor, 
                                    forma_pagamento=self.forma_pagamento, 
                                    grupo_encargo=self.grupo_encargo,
                                    status=False
                                    )
                conta.save()      
            
            try:
                cancela_compra = self.botao_acionado
            except:
                cancela_compra = None

            # trata cancelamento de compra efetuada
            if not self.status and cancela_compra == '_addcancelacompra' and (self.pedido == 'N' or (self.pedido == 'S' and self.status_pedido)):
                # Define a compra com status cancelado
                self.status = True
                self.save()

                # Numa compra cancelada: decrescenta a quantidade dos produtos cancelados novamente ao estoque.
                for i in ItensCompra.objects.filter(compras=self.pk).values_list('id', 'produto', 'quantidade'):
                    produto = Produtos.objects.get(pk=i[1])
                    produto.quantidade = produto.quantidade - i[2]
                    produto.save()
                
                # Fecha a conta à pagar
                conta = ContasPagar.objects.get(compras=self.pk)
                conta.status = True
                conta.save()

        else:

            # Chama a função save original para o save atual do modelo
            super(Compra, self).save(*args, **kwargs)



@python_2_unicode_compatible
class ItensCompra(models.Model):
    u""" 
    Classe ItensCompra. 
    Inline criada para ser exibida na página de compras.
    Nesta, todos os itens de uma compra são registrados.
    
    Criada em 15/06/2014. 
    """

    quantidade = models.IntegerField(verbose_name=_(u"Quantidade"))
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor unitário (R$)"))
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Total (R$)"))
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=_(u"Desconto (%)"))
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT, verbose_name=_(u"Produto"))
    compras = models.ForeignKey(Compra, on_delete=models.PROTECT, verbose_name=_(u"Compra"))
    add_estoque = models.BooleanField(default=False, verbose_name=_(u"Adicionado ao estoque?"))

    class Meta:
        verbose_name = _(u"Item de Compra")
        verbose_name_plural = _(u"Itens de Compra")


    def __str__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a adição da quantidade de produtos ao estoque.
        """
        if self.pk and not self.add_estoque:
            
            # Soma a quantidade de produtos comprados com a que já existe no estoque
            compra = Compra.objects.get(pk=self.compras.pk)
            super(ItensCompra, self).save(*args, **kwargs)

            if compra.pedido == 'N' or (compra.pedido == 'S' and compra.status_pedido):
                self.add_estoque = True
                self.save()

                produto = Produtos.objects.get(pk=self.produto.pk)
                produto.quantidade = produto.quantidade + self.quantidade
                produto.save()

        else:

            super(ItensCompra, self).save(*args, **kwargs)



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_pagar.models import ContasPagar
