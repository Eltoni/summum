#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from localidade.models import Cidade
from sorl.thumbnail import ImageField


@python_2_unicode_compatible
class Banco(models.Model):
    
    banco = models.CharField(unique=True, max_length=10, verbose_name=_(u"Banco"))
    nome = models.CharField(max_length=200, verbose_name=_(u"Nome"))
    site = models.URLField(blank=True, verbose_name=_(u"Site"))
    logo = ImageField(upload_to='logo_banco', max_length=255, blank=True, null=True, verbose_name=_(u"Logo"))
    
    class Meta:
        verbose_name = _(u"Banco")
        verbose_name_plural = _(u"Bancos")

    def __str__(self):
        return u'%s' % self.nome



@python_2_unicode_compatible
class Agencia(models.Model):
    
    banco = models.ForeignKey(Banco, on_delete=models.PROTECT, verbose_name=_(u"Banco"))
    agencia = models.CharField(max_length=7, verbose_name=_(u"Agência"))
    nome = models.CharField(max_length=75, verbose_name=_(u"Nome"))
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, default='', blank=True, null=True, verbose_name=_(u"Cidade"))
    bairro = models.CharField(max_length=50, blank=True, null=True, verbose_name=_(u"Bairro"))
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name=_(u"Estado"))
    endereco = models.CharField(max_length=50, blank=True, null=True, verbose_name=_(u"Endereço"))
    numero = models.CharField(max_length=15, blank=True, null=True, verbose_name=_(u"Número"))
    complemento = models.CharField(max_length=50, blank=True, null=True, verbose_name=_(u"Complemento"))
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name=_(u"Cep"))
    contato = models.CharField(max_length=30, blank=True, null=True, verbose_name=_(u"Contato"))

    class Meta:
        unique_together = (("banco", "agencia"),)
        verbose_name = _(u"Agência")
        verbose_name_plural = _(u"Agências")

    def __str__(self):
        return u'%s (%s)' % (self.agencia, self.nome)