#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
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
    periodo_venc_pedido_compra = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Período de vencimento do pedido (dias)"),
        help_text=_(u"Defina o período de vencimento de um pedido de compra. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.")
    )
    periodo_venc_pedido_venda = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Período de vencimento do pedido (dias)"),
        help_text=_(u"Defina o período de vencimento de um pedido de venda. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.")
    )
    qtde_minima_produtos_em_estoque = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=_(u"Qtde mínima em estoque"),
        help_text=_(u"Indique a quantidade mínima de itens de produto no estoque.")
    )
    perc_valor_minimo_recebimento = models.DecimalField(
        max_digits=20, 
        decimal_places=0, 
        blank=True, 
        null=True,
        verbose_name=_(u"Perc. Valor do 1º recebimento"),
        help_text=_(u"Percentual mínimo do valor do primeiro recebimento de uma parcela.")
    )
    intervalo_dias_entrega_venda = models.IntegerField(
        verbose_name=_(u"Intervalo para entrega"),
        help_text=_(u"Intervalo mínimo entre a data de venda e a data de entrega (dias)."),
        default=0
    )
    email_abertura_caixa = models.TextField(
        blank=True, 
        verbose_name=_(u"Email de abertura de caixa"), 
        help_text=_(u"Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.")
    )
    evento_calendario = models.CharField(
        verbose_name=_("Calendário de eventos"), 
        max_length=200,
        help_text=_(u"Defina o calendário de eventos que aparecerão no dashboard do sistema."),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _(u"Parametrização")
        verbose_name_plural = _(u"Parametrizações")


    def __str__(self):
        return u'%s' % self.id