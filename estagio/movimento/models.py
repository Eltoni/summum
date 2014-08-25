#-*- coding: UTF-8 -*-
from django.db import models


class Produtos(models.Model):
    nome = models.CharField(max_length=255) 
    preco = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de compra') 
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de venda')
    quantidade = models.IntegerField()
    descricao = models.TextField(blank=True) 

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = "Produtos"

    def __unicode__(self):
        return u'%s' % (self.nome)