#-*- coding: UTF-8 -*-
from django.db import models


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100) 
    descricao = models.CharField(max_length=250, blank=True, verbose_name=u'Descrição')
    quant_parcelas = models.IntegerField(verbose_name=u'Quantidade de parcelas') 
    prazo_entre_parcelas = models.IntegerField() 
    tipo_prazo = models.CharField(max_length=1, blank=True) 
    carencia = models.IntegerField(verbose_name=u'Carência')
    tipo_carencia = models.CharField(max_length=1, blank=True, verbose_name=u'Tipo de carência')

    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = "Formas de Pagamento"

    def __unicode__(self):
        return u'%s' % (self.nome)
        

