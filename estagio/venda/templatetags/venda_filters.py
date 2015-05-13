#-*- coding: UTF-8 -*-
from django import template
from contas_receber.models import ContasReceber, ParcelasContasReceber

register = template.Library()


@register.assignment_tag
def checa_habilita_pedido_venda():
    from configuracoes.models import Parametrizacao
    habilita_pedido_venda = Parametrizacao.objects.get().habilita_pedido_venda
    return habilita_pedido_venda



@register.filter(name='checa_pagamentos_venda')
def checa_pagamentos_venda(value):
    """ 
    Bloqueia o cancelamento de uma venda quando já há pagamentos no caixa proveniente da conta da venda do contexto.
    """
    try:
        contas_receber = ContasReceber.objects.filter(vendas__pk=value)
        venda_movimento_financeiro = ParcelasContasReceber.objects.filter(contas_receber=contas_receber, status=True).select_related('contas_pagar__contaspagar').values_list('status').exists()
        if venda_movimento_financeiro:
            return True
        else:
            return False
    except: 
        return None
