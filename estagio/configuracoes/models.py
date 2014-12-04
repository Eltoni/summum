#-*- coding: UTF-8 -*-
from django.db import models


class Parametrizacao(models.Model):
    u"""
        Tabela que conterá registro único que armazenará as configurações de todo o sistema.

        Criada em: 04/12/2014.
    """
    
    quantidade_inlines_compra = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=u'Qtde itens de compra',
        help_text=u'Quantidade de inlines prévios na compra'
    )
    quantidade_inlines_venda = models.IntegerField(
        blank=True, 
        null=True,
        verbose_name=u'Qtde itens de venda',
        help_text=u'Quantidade de inlines prévios na venda'
    )

    class Meta:
        verbose_name = u'Parametrização'
        verbose_name_plural = u'Parametrizações'


    def __unicode__(self):
        return u'%s' % self.id