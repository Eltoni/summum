#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Cidade(models.Model):
    nome = models.CharField(max_length=255, verbose_name=_(u"Nome"))
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name=_(u"Estado"))
    ultima_alteracao = models.DateTimeField(auto_now=True, verbose_name=_(u"Última alteração"))

    def __unicode__(self):
        return u'%s' % (self.nome)

    class Meta:
        verbose_name = _(u"Cidade")
        verbose_name_plural = _(u"Cidades")
        unique_together = ("nome", "estado")