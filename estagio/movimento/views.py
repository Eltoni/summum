#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Produtos
from configuracoes.models import Parametrizacao


def produtos_esgotando(request):
	u""" Indica na página inicial do sistema os produtos que estão se esgotando no estoque. """
	
	quantidade_minima = Parametrizacao.objects.values_list('qtde_minima_produtos_em_estoque')[0][0]
	
	try:
		produtos_esgotando = Produtos.objects.filter(status=True, quantidade__lte=quantidade_minima).values_list('id', 'nome', 'quantidade').order_by('quantidade', 'id')
	except:
		produtos_esgotando = None 

	data = {
		'produtos_esgotando': produtos_esgotando,
		'quantidade_minima': quantidade_minima,
	}

	return render_to_response('admin/index.html', data, context_instance=RequestContext(request))