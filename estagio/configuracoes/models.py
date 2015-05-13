#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Parametrizacao(models.Model):
    u"""
        Tabela que conterá registro único que armazenará as configurações de todo o sistema.

        Criada em: 04/12/2014.
    """
    
    quantidade_inlines_compra = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Qtde itens de compra"),
        help_text=_(u"Quantidade de inlines prévios na compra")
    )
    quantidade_inlines_venda = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Qtde itens de venda"),
        help_text=_(u"Quantidade de inlines prévios na venda")
    )
    habilita_pedido_compra = models.BooleanField(
        default=True, 
        verbose_name=_(u"Habilita pedido de compra?"),
        help_text=_(u"Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.")
    )
    habilita_pedido_venda = models.BooleanField(
        default=True, 
        verbose_name=_(u"Habilita pedido de venda?"),
        help_text=_(u"Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.")
    )
    qtde_minima_produtos_em_estoque = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Qtde mínima em estoque"),
        help_text=_(u"Indique a quantidade mínima de itens de produto no estoque.")
    )
    perc_valor_minimo_pagamento = models.DecimalField(
        max_digits=20, 
        decimal_places=0, 
        blank=True, 
        null=True,
        verbose_name=_(u"Perc. Valor do 1º pagamento"),
        help_text=_(u"Percentual mínimo do valor do primeiro pagamento de uma parcela.")
    )
    intervalo_dias_entrega_venda = models.IntegerField(
        verbose_name=_(u"Intervalo para entrega"),
        help_text=_(u"Intervalo mínimo entre a data de venda e a data de entrega (dias)."),
        default=0
    )
    
    class Meta:
        verbose_name = _(u"Parametrização")
        verbose_name_plural = _(u"Parametrizações")


    def __unicode__(self):
        return u'%s' % self.id