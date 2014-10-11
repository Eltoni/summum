#-*- coding: UTF-8 -*-
from django.db import models


class Produtos(models.Model):
    nome = models.CharField(max_length=255) 
    preco = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de compra') 
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de venda')
    quantidade = models.IntegerField(default=0)
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 
    status = models.BooleanField(default=True, help_text=u'Indica se o produto está ativo para atividades de compra e venda.')

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = "Produtos"

    def __unicode__(self):
        return u'%s' % (self.nome)