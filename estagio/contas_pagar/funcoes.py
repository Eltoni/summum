#-*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from contas_pagar.models import ParcelasContasPagar
from datetime import date


def status_financeiro(id_cliente):
    u""" 
        Método que retorna a situação financeira atual da empresa com determinado fornecedor.
     """

    hoje = date.today()
    status = ParcelasContasPagar.objects.filter(vencimento__lt=hoje, status=False, contas_pagar__fornecedores=id_cliente).select_related('contas_pagar__contaspagar').exists()
    if status:
        return ['I', _(u"Inadimplente"),]
    else:
        return ['A', _(u"Adimplente"),]