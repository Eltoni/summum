#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Cidade(models.Model):
    nome = models.CharField(max_length=255, verbose_name=_(u"Nome"))
    estado = models.CharField(max_length=2, blank=True, null=True, db_index=True, verbose_name=_(u"Estado"))

    def __str__(self):
        return u'%s' % (self.nome)

    class Meta(object):
        verbose_name = _(u"Cidade")
        verbose_name_plural = _(u"Cidades")
        unique_together = ("nome", "estado")