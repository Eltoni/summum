#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from sorl.thumbnail import ImageField


@python_2_unicode_compatible
class Marca(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name=_(u"Nome"))
    logo = ImageField(upload_to='marcas', max_length=255, blank=True, verbose_name=_(u"Logo"))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição")) 

    def __str__(self):
        return u'%s' % (self.nome)


@python_2_unicode_compatible
class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name=_(u"Nome"))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição")) 

    def __str__(self):
        return u'%s' % (self.nome)


@python_2_unicode_compatible
class Produtos(models.Model):
    nome = models.CharField(max_length=255, verbose_name=_(u"Nome")) 
    preco = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Preço de compra")) 
    preco_venda = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Preço de venda"))
    quantidade = models.IntegerField(default=0, verbose_name=_(u"Quantidade"))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição")) 
    status = models.BooleanField(default=True, db_index=True, verbose_name=_(u"Status"), help_text=_(u"Indica se o produto está ativo para atividades de compra e venda."))
    marca = models.ForeignKey(Marca, blank=True, null=True, on_delete=models.PROTECT, verbose_name=_(u"Marca"))
    categorias = models.ManyToManyField(Categoria, blank=True, verbose_name=_(u"Categoria"))
    imagem = ImageField(upload_to='produtos', max_length=255, blank=True, verbose_name=_(u"Imagem"))

    class Meta:
        verbose_name = _(u"Produto")
        verbose_name_plural = _(u"Produtos")
        permissions = ((u"visualizar_rel_produtos_esgotando", _(u"Ver relatorio de produtos esgotando em estoque")),
                       (u"visualizar_rel_debitos_creditos_diario", _(u"Ver relatorio de debitos e creditos diarios")),
                       (u"visualizar_relatorios", _(u"Ver relatorios")),
                       (u"pode_exportar_produtos", _(u"Exportar Produtos")),)

    def __str__(self):
        return u'%s' % (self.nome)
