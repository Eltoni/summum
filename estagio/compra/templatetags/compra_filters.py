#-*- coding: UTF-8 -*-
from django import template

from contas_pagar.models import ContasPagar, ParcelasContasPagar
from configuracoes.models import Parametrizacao

register = template.Library()


@register.assignment_tag
def checa_habilita_pedido_compra():
    habilita_pedido_compra = Parametrizacao.objects.get().habilita_pedido_compra
    return habilita_pedido_compra



@register.filter(name='checa_pagamentos_compra')
def checa_pagamentos_compra(value):
    """ 
    Bloqueia o cancelamento de uma compra quando já há pagamentos no caixa proveniente da conta da compra do contexto.
    """
    try:
        contas_pagar = ContasPagar.objects.filter(compras__pk=value)
        compra_movimento_financeiro = ParcelasContasPagar.objects.filter(contas_pagar=contas_pagar, status=True).select_related('contas_pagar__contaspagar').values_list('status').exists()
        if compra_movimento_financeiro:
            return True
        else:
            return False
    except: 
        return None
