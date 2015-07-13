from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from pessoal.models import Cliente
from contas_receber.models import ContasReceber, ParcelasContasReceber, Recebimento
from django.utils.translation import ugettext_lazy as _
from django.db.models import Sum
 

def get_dados_usuario(request, id):
    usuario = User.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  usuario)
    return HttpResponse(retorno, content_type="text/javascript")


def cliente_financeiro(request):
    cliente = Cliente.objects.filter() 

    data = {
        'title': _(u"Financeiro - Cliente"),
        'cliente': cliente,
    }

    return render_to_response('admin/cliente_financeiro.html', data, context_instance=RequestContext(request))


def cliente_detalhe_financeiro(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente)
    contas_cliente = ContasReceber.objects.filter(cliente=id_cliente).values_list('pk', 'data', 'vendas', 'valor_total', 'descricao', 'status')
    parcelas_cliente = ParcelasContasReceber.objects.filter(contas_receber__cliente=id_cliente).values_list('pk', 'vencimento', 'valor', 'status', 'contas_receber')
    recebimentos_cliente = Recebimento.objects.filter(parcelas_contas_receber__contas_receber__cliente=id_cliente).values_list('pk', 'data', 'valor', 'parcelas_contas_receber')

    encargos_recebidos = 0
    encargos_a_receber = 0
    totais_recebidos = 0
    totais_a_receber = 0
    for i in range(len(contas_cliente)):
        c = ContasReceber.objects.get(cliente=id_cliente, pk=contas_cliente[i][0])
        encargos_recebidos += c.valor_total_encargos_pagos()
        encargos_a_receber += c.valor_total_encargos_a_pagar()
        totais_recebidos += c.valor_total_recebido()
        totais_a_receber += c.valor_total_a_receber()

    totais_recebidos_sem_encargos = totais_recebidos - encargos_recebidos
    totais_a_pagar_sem_encargos = totais_a_receber - encargos_a_receber

    data = {
        'title': _(u"Detalhes financeiros - Cliente"),
        'cliente': cliente,
        'contas_cliente': contas_cliente,
        'parcelas_cliente': parcelas_cliente,
        'recebimentos_cliente': recebimentos_cliente,
        'encargos_recebidos': encargos_recebidos,
        'encargos_a_receber': encargos_a_receber,
        'totais_recebidos': totais_recebidos,
        'totais_recebidos_sem_encargos': totais_recebidos_sem_encargos,
        'totais_a_pagar_sem_encargos': totais_a_pagar_sem_encargos,
        'totais_a_receber': totais_a_receber
    }

    return render_to_response('admin/cliente_detalhes_financeiros.html', data, context_instance=RequestContext(request))

