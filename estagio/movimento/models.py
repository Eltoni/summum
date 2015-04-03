#-*- coding: UTF-8 -*-
from django.db import models
from sorl.thumbnail import ImageField


class Marca(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    logo = ImageField(upload_to='marcas', max_length=255, blank=True)
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 

    def __unicode__(self):
        return u'%s' % (self.nome)


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 

    def __unicode__(self):
        return u'%s' % (self.nome)


class Produtos(models.Model):
    nome = models.CharField(max_length=255) 
    preco = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de compra') 
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Preço de venda')
    quantidade = models.IntegerField(default=0)
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 
    status = models.BooleanField(default=True, help_text=u'Indica se o produto está ativo para atividades de compra e venda.')
    marca = models.ForeignKey(Marca, blank=True, null=True, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria, blank=True, null=True)

    class Meta:
        verbose_name = u'Produto'
        verbose_name_plural = "Produtos"
        permissions = ((u"visualizar_rel_produtos_esgotando", u"Ver relatorio de produtos esgotando em estoque"),
                       (u"visualizar_rel_debitos_creditos_diario", u"Ver relatorio de debitos e creditos diarios"),)

    def __unicode__(self):
        return u'%s' % (self.nome)
