#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Sum

from movimento.models import Produtos
from pessoal.models import EnderecoEntregaCliente, Funcionario
from venda.models import Venda


def get_valor_unitario(request, id):
    u""" Retorna para o template, em tempo real, os atributos do produto selecionado """

    produtos = Produtos.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  produtos)
    return HttpResponse(retorno, content_type="text/javascript")


def get_endereco_entrega_cliente(request, id):
    u""" Retorna para o template, em tempo real, os atributos do endereço selecionado """

    endereco = EnderecoEntregaCliente.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  endereco, fields=('endereco', 'cidade', 'estado'))
    return HttpResponse(retorno, content_type="text/javascript")


def overview_vendas(request):
    # Busca todos os dados do funcionario
    funcionario = Funcionario.objects.get(pk=1)
    funcionarios_list = Funcionario.objects.all()
    valores_venda = Venda.objects.filter(status=0).values('vendedor').annotate(quant=Count('vendedor'), total=Sum('total')).order_by('total')

    print (valores_venda)
    for key, value in valores_venda.iteritems():
        print(key, '. Value: ', value)

    perm_visualizacao = funcionario._meta.app_label+'.'+'change_'+funcionario._meta.model_name
    if perm_visualizacao in request.user.get_all_permissions():
        has_change_permission = True
    else:
        has_change_permission = False

    data = {
        'title': _(u"Detalhes Financeiros - Cliente"),
        'app_name': funcionario._meta.app_label,
        'opts': funcionario._meta,
        'has_change_permission': has_change_permission,
        'original': funcionario,
    }

    return render_to_response('admin/desempenho_vendedores.html', data, context_instance=RequestContext(request))