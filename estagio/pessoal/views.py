#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.translation import gettext as _g, ugettext_lazy as _
from django import forms
from django.views.decorators.cache import cache_page

from itertools import groupby

from pessoal.models import Cliente
from contas_receber.models import ContasReceber, ParcelasContasReceber, Recebimento


ANOS_CHOICES = [
    ('', u'---'), 
    ('2014', u'2014'), 
    ('2015', u'2015'),
    ('2016', u'2016'),
]

class Opcoes(forms.Form):
    ano = forms.ChoiceField(choices=ANOS_CHOICES)

    def __init__(self, *args, **kwargs):
        # self.ano = kwargs.pop('ano', None)
        super(Opcoes, self).__init__(*args, **kwargs)
        self.fields['ano'].widget.attrs['class'] = 'auto-width'
        # ano = request.GET.get('ano', '')
        # self.fields['ano'].initial = ano


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


@cache_page(60 * 30)
def cliente_detalhe_financeiro(request, id_cliente):
    # Busca todos os dados do cliente
    cliente = Cliente.objects.get(pk=id_cliente)
    contas_cliente = ContasReceber.objects.filter(cliente=id_cliente).values_list('pk')
    parcelas_cliente = ParcelasContasReceber.objects.filter(contas_receber__cliente=id_cliente).values_list('pk')
    recebimentos_cliente = Recebimento.objects.filter(parcelas_contas_receber__contas_receber__cliente=id_cliente).values_list('pk', 'data', 'valor', 'parcelas_contas_receber').order_by('data')
    
    # filtra os itens financeiros pelo parâmetro Ano caso o filtro seja utilizado
    if request.GET.get('ano'):
        f_ano = int(request.GET.get('ano'))
        contas_cliente = contas_cliente.filter(data__year=f_ano)
        parcelas_cliente = parcelas_cliente.filter(vencimento__year=f_ano)
        recebimentos_cliente = recebimentos_cliente.filter(data__year=f_ano)
    else:
        f_ano = None

    opcoes = Opcoes(initial=request.GET)

    receb_group_mes = []
    receb_mes = [(1, _g('janeiro')), (2, _g('fevereiro')), (3, _g('março')), (4, _g('abril')), (5, _g('maio')), (6, _g('junho')), (7, _g('julho')), (8, _g('agosto')), (9, _g('setembro')), (10, _g('outubro')), (11, _g('novembro')), (12, _g('dezembro'))]
    for rm in receb_mes:
        vt = sum([ float(r[2]) for r in recebimentos_cliente if r[1].month == rm[0]]) or float(0.00)
        qt = len([r[2] for r in recebimentos_cliente if r[1].month == rm[0]]) or 0
        receb_group_mes.append((rm[0], rm[1], vt, qt))

    extra_serie = {"tooltip": {"y_start": "R$ ", "y_end": _g(" recebidos")}}
    
    chartdata_1 = {
        'x': [ x[1] for x in receb_group_mes ],
        'name1': _g(u'Valor recebido'), 
        'y1': [ x[2] for x in receb_group_mes ],
        'extra1': extra_serie
    }
    charttype_1 = "discreteBarChart"
    chartcontainer_1 = 'discretebarchart_container'



    encargos_recebidos = encargos_a_receber = totais_recebidos = totais_a_receber = totais_encargos = totais_sem_encargos = totais_a_pagar_sem_encargos = totais_cobrados = 0
    for i in range(len(contas_cliente)):
        c = ContasReceber.objects.get(cliente=id_cliente, pk=contas_cliente[i][0])
        encargos_recebidos += c.valor_total_encargos_pagos()
        encargos_a_receber += c.valor_total_encargos_a_pagar()
        totais_recebidos += c.valor_total_recebido()
        totais_a_receber += c.valor_total_a_receber()
        totais_encargos += c.valor_total_encargos()
        totais_sem_encargos += c.valor_total
        totais_cobrados += c.valor_total_cobrado()

    totais_recebidos_sem_encargos = totais_recebidos - encargos_recebidos
    totais_a_pagar_sem_encargos = totais_a_receber - encargos_a_receber


    parcelas_hist = []
    parcelas = []
    for i in range(len(parcelas_cliente)):
        p = ParcelasContasReceber.objects.get(contas_receber__cliente=id_cliente, pk=parcelas_cliente[i][0])
        parcelas.append(((_g(p.status_parcela()[1])), p.status_parcela()[0]))
        parcelas_hist.append(p.quant_dias_vencidos())

    
    parcelas_hist_q_atrasadas = sum(1 for i in parcelas_hist if i > 0)
    parcelas_hist_qd_atrasadas = sum(i for i in parcelas_hist if i > 0)
    parcelas_hist_q_total = len(parcelas_hist)
    parcelas_hist_per_atrasadas = (parcelas_hist_q_atrasadas * 100) / parcelas_hist_q_total if parcelas_hist_q_total != 0 else 0
    parcelas_hist_md_atrasadas = round(parcelas_hist_qd_atrasadas / parcelas_hist_q_atrasadas) if parcelas_hist_q_atrasadas != 0 else 0


    parcelas = sorted(parcelas)
    p_status = []
    for key, values in groupby(parcelas, lambda d: (d)):
        p_status.append((key[0], key[1], len(list(values))))

    quant_status_t = (sum([ x[2] for x in p_status ]))
    percent_status = [ (i[2] * 100.00) / quant_status_t for i in p_status ]
    quant_status = [ x[2] for x in p_status ]
    cores_status = [ x[1] for x in p_status ]
    nome_status = [ x[0] for x in p_status ]
    percent_status_t = (sum([ x for x in percent_status ]))

    # Início do Gráfico de percentuais
    xdata = nome_status
    ydata = percent_status
    color_list = cores_status
    extra_serie = { 
        "tooltip": {"y_start": "", "y_end": "%"}, 
        "color_list": color_list
    }
    
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    # Fim do Gráfico de percentuais


    perm_visualizacao = cliente._meta.app_label+'.'+'change_'+cliente._meta.model_name
    if perm_visualizacao in request.user.get_all_permissions():
        has_change_permission = True
    else:
        has_change_permission = False

    data = {
        'title': _(u"Detalhes Financeiros - Cliente"),
        'app_name': cliente._meta.app_label,
        'opts': cliente._meta,
        'has_change_permission': has_change_permission,
        'original': cliente,
        'contas_cliente': contas_cliente,
        'encargos_recebidos': encargos_recebidos,
        'encargos_a_receber': encargos_a_receber,
        'totais_recebidos': totais_recebidos,
        'totais_recebidos_sem_encargos': totais_recebidos_sem_encargos,
        'totais_a_pagar_sem_encargos': totais_a_pagar_sem_encargos,
        'totais_a_receber': totais_a_receber,
        'totais_encargos': totais_encargos,
        'totais_sem_encargos': totais_sem_encargos,
        'totais_cobrados': totais_cobrados,
        'opcoes': opcoes,
        'f_ano': f_ano,
        
        'nome_status': nome_status,
        'quant_status': quant_status,
        'percent_status': percent_status,
        'quant_status_t': quant_status_t,
        'percent_status_t': percent_status_t,
        'parcelas_hist_q_atrasadas': parcelas_hist_q_atrasadas,
        'parcelas_hist_per_atrasadas': parcelas_hist_per_atrasadas,
        'parcelas_hist_md_atrasadas': parcelas_hist_md_atrasadas,
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        },

        'receb_group_mes': receb_group_mes,
        'charttype_1': charttype_1,
        'chartdata_1': chartdata_1,
        'chartcontainer_1': chartcontainer_1,
        'extra_1': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': False,
            'jquery_on_ready': False,
        },
    }

    return render_to_response('admin/cliente_detalhes_financeiros.html', data, context_instance=RequestContext(request))

