#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.template import RequestContext
from models import Produtos
from configuracoes.models import Parametrizacao
from caixa.models import *
import time
from itertools import groupby


def index(request):
	u""" Indica na página inicial do sistema os produtos que estão se esgotando no estoque. """

	if request.user.is_authenticated():
		quantidade_minima = Parametrizacao.objects.values_list('qtde_minima_produtos_em_estoque')[0][0]
		tab_limite_estoque = None if quantidade_minima is None else 1
		
		try:
			produtos_esgotando = Produtos.objects.filter(status=True, quantidade__lte=quantidade_minima).values_list('id', 'nome', 'quantidade').order_by('quantidade', 'id')
		except:
			produtos_esgotando = None 

		####################################################################################################################################################
		# Início do gráfico de movimentos monetários diários
		####################################################################################################################################################
		data = MovimentosCaixa.objects.values_list('data', 'valor', 'tipo_mov').order_by('data')
		grafico_mov_dia = data or None

		datas = []
		for key, values in groupby(data, key=lambda d: d[0].date()):
			datas.append(key)

		data_mov = [ int(time.mktime(d.timetuple()) * 1000) for d in datas ]
		# data_mov = [ int(time.mktime(d[0].date().timetuple()) * 1000) for d in data ]

		credito = []
		debito = []
		for d in datas:
			deb = 0
			cred = 0
			for d2 in data:
				if d == d2[0].date():
					if d2[2] == u'Crédito':
						cred += Decimal(d2[1].strip(' "'))
						deb += 0
					else:
						deb += Decimal(d2[1].strip(' "'))
						cred += 0
			credito.append(str(cred))
			debito.append(str(deb))

		# print credito
		# print debito
		formato_data = "%d/%m/%Y"
		extra_serie1 = {
			"tooltip": {"y_start": "R$", "y_end": ""},
			"date_format": formato_data,
			'color': '#a4c639'
		}
		extra_serie2 = {
			"tooltip": {"y_start": "R$", "y_end": ""},
			"date_format": formato_data,
			'color': '#FF8aF8'
		}
		chartdata = {'x': data_mov,
		'name1': 'Crédito', 'y1': credito, 'extra1': extra_serie1,
		'name2': 'Débito', 'y2': debito, 'extra2': extra_serie2}

		charttype = "lineChart"
		chartcontainer = 'linechart_container'  # container name
		####################################################################################################################################################
		# Fim do gráfico de movimentos monetários diários
		####################################################################################################################################################

		data = {
			'title': 'Dashboard',
			'dashboard': True,
			'tab_limite_estoque': tab_limite_estoque,
			'produtos_esgotando': produtos_esgotando,
			'quantidade_minima': quantidade_minima,
			'grafico_mov_dia': grafico_mov_dia,
			'charttype': charttype,
			'chartdata': chartdata,
			'chartcontainer': chartcontainer,
			'extra': {
				'x_is_date': True,
				'x_axis_format': '%d/%m/%Y',
				'tag_script_js': True,
				'jquery_on_ready': False,
			}
		}

		return render_to_response('admin/index.html', data, context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect('/logout/')
