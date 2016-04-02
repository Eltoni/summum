#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

from movimento.models import Produtos

 
def get_valor_unitario(request, id):
    u""" Retorna para o template, em tempo real, os atributos do produto selecionado """

    produtos = Produtos.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  produtos)
    return HttpResponse(retorno, content_type="text/javascript")

