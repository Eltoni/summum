#-*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from contas_receber.models import ParcelasContasReceber
from datetime import date


def status_financeiro(id_cliente):
    u""" 
        Método que retorna a situação financeira atual do cliente junto a empresa.
     """

    hoje = date.today()
    status = ParcelasContasReceber.objects.filter(vencimento__lt=hoje, status=False, contas_receber__cliente=id_cliente).select_related('contas_receber__contasreceber').exists()
    if status:
        return ['I', _(u"Inadimplente"),]
    else:
        return ['A', _(u"Adimplente"),]