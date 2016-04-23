#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.translation import gettext as _g, ugettext_lazy as _
from django import forms
from django.views.decorators.cache import cache_page
import pandas as pd

from itertools import groupby
import calendar
import locale

from pessoal.models import Cliente
from contas_receber.models import ContasReceber, ParcelasContasReceber, Recebimento


locale.setlocale(locale.LC_ALL, '')

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
    recebimentos_cliente = Recebimento.objects.filter(parcelas_contas_receber__contas_receber__cliente=id_cliente).order_by('data').values() 
    
    # filtra os itens financeiros pelo parâmetro Ano caso o filtro seja utilizado
    f_ano = None
    if request.GET.get('ano'):
        f_ano = int(request.GET.get('ano'))
        contas_cliente = contas_cliente.filter(data__year=f_ano)
        parcelas_cliente = parcelas_cliente.filter(vencimento__year=f_ano)
        recebimentos_cliente = recebimentos_cliente.filter(data__year=f_ano)

    # Início do bloco - Manipula os dados que serão exibidos na tabela dos itens financeiros gerados
    #----------------------------------------------------------------------------------------------
    encargos_recebidos = encargos_a_receber = totais_recebidos = totais_a_receber = \
    totais_encargos = totais_sem_encargos = totais_a_pagar_sem_encargos = totais_cobrados = 0
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
    #----------------------------------------------------------------------------------------------
    # Fim do bloco


    # Início do bloco
    #----------------------------------------------------------------------------------------------
    status_parcelas = []
    for i in range(len(parcelas_cliente)):
        p = ParcelasContasReceber.objects.get(contas_receber__cliente=id_cliente, pk=parcelas_cliente[i][0])
        status_parcelas.append((p.status_parcela()[2], 
                                _g(p.status_parcela()[1]), 
                                p.status_parcela()[0], 
                                p.quant_dias_vencidos()
                                ))

    df_parcelas = pd.DataFrame(status_parcelas)
    df_parcelas = df_parcelas.rename(columns = {0:'id_status', 1:'status', 2:'cor', 3:'dias_vencidos',})

    df_parcelas_agrupados = df_parcelas.groupby(['id_status','status','cor'], as_index=False).agg(['count', 'mean'])    # Agrupa pelo status, e obtém a média de dias atrasados, e a quantidade de parcelas
    df_parcelas_agrupados.columns = df_parcelas_agrupados.columns.droplevel(0)
    df_parcelas_agrupados = df_parcelas_agrupados.reset_index()
    df_parcelas_agrupados['hist_quant_parc_total'] = df_parcelas.count()[0].astype(int)
    df_parcelas_agrupados['hist_quant_parc_venc'] = df_parcelas[df_parcelas['dias_vencidos'] > 0].count()[0]
    df_parcelas_agrupados['hist_quant_parc_dias_venc_total'] = df_parcelas[df_parcelas['dias_vencidos'] > 0]['dias_vencidos'].sum()
    df_parcelas_agrupados['hist_perc_parc_venc'] = df_parcelas_agrupados['hist_quant_parc_venc'] * 100 / df_parcelas_agrupados['hist_quant_parc_total']
    df_parcelas_agrupados['hist_media_dias_parc_venc'] = df_parcelas_agrupados['hist_quant_parc_dias_venc_total'] / df_parcelas_agrupados['hist_quant_parc_venc']

    df_parcelas_agrupados['status_percentual'] = df_parcelas_agrupados['count'] * 100 / df_parcelas_agrupados['hist_quant_parc_total']
    df_parcelas_agrupados['status_percentual_total'] = df_parcelas_agrupados['status_percentual'].sum()

    df_parcelas_agrupados['option_selected'] = df_parcelas_agrupados['id_status'] == 1
    df_parcelas_agrupados['option_selected'] = df_parcelas_agrupados['option_selected'].map({True:'true', False:''})

    list_p = df_parcelas_agrupados.values.tolist()
    lista_status_parcelas = [ {'name':i[1], 'color':i[2], 'y':float(i[10]), 'sliced':i[12], 'selected':i[12]} for i in list_p ]
    #----------------------------------------------------------------------------------------------
    # Fim do bloco


    lista_meses = [ (i, calendar.month_abbr[i], calendar.month_name[i]) for i in range(1,13) ]              # busca lista de meses
    df_meses = pd.DataFrame(lista_meses)                                                                    # gera o DataFrame ds lista de meses
    df_meses = df_meses.rename(columns = {0:'mes', 1:'mes_nome_abr', 2:'mes_nome',})                        # renomeia as colunas    

    df_recebimentos = pd.DataFrame.from_records(recebimentos_cliente)
    df_recebimentos = df_recebimentos.get(['data', 'valor'])
    df_recebimentos['mes'] = df_recebimentos['data'].dt.month
    df_recebimentos_agrupados = df_recebimentos.groupby(['mes',], as_index=True).agg(['sum', 'count'])      # função agg permite que seja aplicado uma lista com vários métodos de agregação de uma só vez.
    df_recebimentos_agrupados.columns = df_recebimentos_agrupados.columns.droplevel(0)                      # Deleta o nível mais externo do índice de coluna hierárquica
    df_recebimentos_agrupados = df_recebimentos_agrupados.reset_index()                                     # Gera uma nova coluna de índice

    df_meses_recebimentos = pd.merge(df_meses, df_recebimentos_agrupados, on='mes', how='left')                        
    df_meses_recebimentos['sum'] = df_meses_recebimentos['sum'].fillna(0)                                   # substitui valores nulos por 0
    df_meses_recebimentos['count'] = df_meses_recebimentos['count'].fillna(0)                               # substitui valores nulos por 0
    df_meses_recebimentos['count'] = df_meses_recebimentos['count'].astype(int)                             # converte tipo do dado para int
    
    dict_mr = df_meses_recebimentos.to_dict()
    list_mr = df_meses_recebimentos.values.tolist()
    lista_meses_recebimentos = list(dict_mr['mes_nome_abr'].values())
    # lista_valor_recebimentos = [ float(i) for i in list(dict_mr['sum'].values()) ]
    lista_valor_recebimentos = [ {'y':float(i[3]), 'mes_nome':i[2]} for i in list_mr ]


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

        'encargos_recebidos': encargos_recebidos,
        'encargos_a_receber': encargos_a_receber,
        'totais_recebidos': totais_recebidos,
        'totais_a_receber': totais_a_receber,
        'totais_encargos': totais_encargos,
        'totais_sem_encargos': totais_sem_encargos,
        'totais_cobrados': totais_cobrados,
        'totais_recebidos_sem_encargos': totais_recebidos_sem_encargos,
        'totais_a_pagar_sem_encargos': totais_a_pagar_sem_encargos,

        'opcoes': Opcoes(initial=request.GET),
        'f_ano': f_ano,
        
        'lista_status_parcelas': lista_status_parcelas,
        'list_p': list_p,

        'list_mr': list_mr,
        'lista_meses_recebimentos': lista_meses_recebimentos,
        'lista_valor_recebimentos': lista_valor_recebimentos,
    }

    return render_to_response('admin/cliente_detalhes_financeiros.html', data, context_instance=RequestContext(request))

