#-*- coding: UTF-8 -*-
from django.db import models


class Cidade(models.Model):
    nome = models.CharField(max_length=255)
    estado = models.CharField(max_length=2, blank=True, null=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.nome)

