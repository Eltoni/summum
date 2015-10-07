#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from configuracoes.models import *
from contas_receber.models.parcela_conta_receber import ParcelasContasReceber
from contas_receber.models.conta_receber import ContasReceber


@python_2_unicode_compatible
class Recebimento(models.Model):
    u""" 
    Classe Recebimento. 
    Criada para registrar todas as entradas financeiras do estabelecimento.
    Os registros de recebimentos entrarão automaticamente na tabela. 

    Criada em 15/06/2014. 
    """

    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber, on_delete=models.PROTECT, verbose_name=_(u"Recebimento de parcela"))

    class Meta:
        verbose_name = _(u"Recebimento")
        verbose_name_plural = _(u"Recebimentos")


    def __str__(self):
        return u'%s' % (self.id)


    def clean(self):
        u""" 
        Bloqueia os recebimentos parciais que forem abaixo do percentual mínimo parametrizado nas configurações do sistema.
        Bloqueia somente o primeiro pagamento da parcela.

        Bloqueia a tentativa de efetuar um recebimento enquanto não houver caixa aberto no sistema.
        Bloqueia quaisquer alterações num registro de recebimento enquanto não houver caixa aberto no sistema.
        """
        # Checa a situação do caixa
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar um recebimento é necessário ter o caixa aberto."))

        if not Caixa.objects.filter(status=1).exists() and self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Alterações num recebimento só podem ser efetivados após a abertura do caixa."))

        # Checa a situação do valor do recebimento
        perc_valor_minimo_recebimento = Parametrizacao.objects.all().values_list('perc_valor_minimo_pagamento')[0][0]
        
        parcela = ParcelasContasReceber.objects.get(pk=self.parcelas_contas_receber.pk)
        valor_minimo_recebimento = round((parcela.valor_total() * perc_valor_minimo_recebimento) / 100, 2)
        primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.parcelas_contas_receber.pk).exists()
        if self.valor < valor_minimo_recebimento and not primeiro_recebimento:
            raise ValidationError(_(u"Primeiro recebimento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_recebimento, 'valor_minimo': valor_minimo_recebimento})


    def save(self, *args, **kwargs):

        if self.pk is None:
            super(Recebimento, self).save(*args, **kwargs)
            parcela_recebimento = Recebimento.objects.filter(pk=self.pk).values_list('parcelas_contas_receber')[0]

            parcela = ParcelasContasReceber.objects.get(pk=parcela_recebimento[0])
            if parcela.valor_pago() >= parcela.valor_total():
                parcela.status = True
                parcela.save()

                #Atualiza o status da conta à receber indicando se a venda está fechada, ou tem parcelas em aberto.
                conta_receber = ContasReceber.objects.get(pk=parcela.contas_receber.pk)
                conta_aberta = ParcelasContasReceber.objects.filter(contas_receber=conta_receber.pk, status=0).exists()
                if conta_aberta:
                    conta_receber.status = False
                    conta_receber.save()
                else:
                    conta_receber.status = True
                    conta_receber.save()
        else:
            super(Recebimento, self).save(*args, **kwargs)