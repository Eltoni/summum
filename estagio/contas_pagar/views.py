#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from contas_pagar.models import Pagamento


def retorna_pagamentos_parcela(request, id_parcela):
    u""" Retorna os pagamentos efetuados para a parcela do contexto. """
    pagamentos = Pagamento.objects.filter(parcelas_contas_pagar=id_parcela).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar')
    data = {
        'title': u'Pagamentos da parcela',
        'app_name': Pagamento._meta.app_label,
        #'is_popup': True,
        'pagamentos': pagamentos,
    }
    return render_to_response('admin/pagamentos_parcela.html', data, context_instance=RequestContext(request))


def retorna_pagamentos_conta(request, id_conta):
    u""" Retorna os pagamentos efetuados para a conta do contexto. """
    pagamentos = Pagamento.objects.filter(parcelas_contas_pagar__contas_pagar=id_conta).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar__contas_pagar')
    data = {
        'title': u'Pagamentos da conta',
        'app_name': Pagamento._meta.app_label,
        'pagamentos': pagamentos,
    }
    return render_to_response('admin/pagamentos_conta.html', data, context_instance=RequestContext(request))