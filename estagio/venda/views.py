#-*- coding: UTF-8 -*-
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from movimento.models import Produtos
 
# Create your views here.
 
def get_valor_unitario(request, id):
    produtos = Produtos.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  produtos)
    return HttpResponse(retorno, mimetype="text/javascript")