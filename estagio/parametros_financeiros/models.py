#-*- coding: UTF-8 -*-
from django.db import models


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100) 
    descricao = models.CharField(max_length=250, blank=True, verbose_name=u'Descrição')
    quant_parcelas = models.IntegerField(verbose_name=u'Quantidade de parcelas') 
    prazo_entre_parcelas = models.IntegerField() 
    tipo_prazo = models.CharField(
        max_length=1, 
        blank=True,
        choices=(
            (u'S', 'Semanal'),
            (u'M', 'Mensal'),
        )
    ) 
    carencia = models.IntegerField(verbose_name=u'Carência')
    tipo_carencia = models.CharField(
        max_length=1, 
        blank=True, 
        verbose_name=u'Tipo de carência',
        choices=(
            (u'S', 'Semanal'),
            (u'M', 'Mensal'),
        )
    )
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as observações relevantes sobre a parametrização desta forma de pagamento.")

    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = "Formas de Pagamento"

    def __unicode__(self):
        return u'%s' % (self.nome)
        