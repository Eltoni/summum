#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100) 
    descricao = models.CharField(max_length=250, blank=True, verbose_name=u'Descrição')
    quant_parcelas = models.IntegerField(verbose_name=u'Quantidade de parcelas') 
    prazo_entre_parcelas = models.IntegerField() 
    tipo_prazo = models.CharField(
        max_length=1, 
        blank=True,
        choices=(
            (u'D', 'Diário'),
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
            (u'D', 'Diário'),
            (u'S', 'Semanal'),
            (u'M', 'Mensal'),
        )
    )
    status = models.BooleanField(default=True, help_text="Indica se a forma de pagamento está ativa para uso.")

    class Meta:
        verbose_name = u'Forma de Pagamento'
        verbose_name_plural = "Formas de Pagamento"

    def __unicode__(self):
        return u'%s' % (self.nome)


    def clean(self):
        """ Não permite que seja registrado uma forma de pagamento que tenha a quantidade de parcelas maior que 1, 
            e que o prazo entre as parcelas seja de zero. 
        """
        if self.quant_parcelas > 1 and self.prazo_entre_parcelas == 0:
            raise ValidationError('Prazo entre parcelas não pode ser 0(zero), quando a quantidade de parcelas é maior que 1(uma).')
        