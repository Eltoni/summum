#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from contas_receber.models import Recebimento


def retorna_recebimentos_parcela(request, id_parcela):
    u""" Retorna os recebimentos efetuados para a parcela do contexto. """
    recebimentos = Recebimento.objects.filter(parcelas_contas_receber=id_parcela).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber')
    data = {
        'title': u'Recebimentos da parcela',
        'app_name': Recebimento._meta.app_label,
        #'is_popup': True,
        'recebimentos': recebimentos,
    }
    return render_to_response('admin/recebimentos_parcela.html', data, context_instance=RequestContext(request))


def retorna_recebimentos_conta(request, id_conta):
    u""" Retorna os recebimentos efetuados para a conta do contexto. """
    recebimentos = Recebimento.objects.filter(parcelas_contas_receber__contas_receber=id_conta).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber__contas_receber')
    data = {
        'title': u'Pagamentos da conta',
        'app_name': Recebimento._meta.app_label,
        'recebimentos': recebimentos,
    }
    return render_to_response('admin/recebimentos_conta.html', data, context_instance=RequestContext(request))