#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from movimento.models import Produtos
from configuracoes.models import Parametrizacao
 
 
def get_valor_unitario(request, id):
    u""" Retorna para o template, em tempo real, os atributos do produto selecionado """

    produtos = Produtos.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  produtos)
    return HttpResponse(retorno, mimetype="text/javascript")


def checa_pedido_compra_habilitado(request, id):
    exibe_botao_pedido_compra = Parametrizacao.objects.filter(id=id)
    retorno = serializers.serialize("json",  exibe_botao_pedido_compra)
    return HttpResponse(retorno, mimetype="text/javascript")