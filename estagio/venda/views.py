#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from movimento.models import Produtos
from pessoal.models import EnderecoEntregaCliente


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