#-*- coding: UTF-8 -*-
from django.contrib import admin
from localidade.models import *
from localidade.forms import *


class CidadeAdmin(admin.ModelAdmin):
    u""" 
    Classe CidadeAdmin. 
    Criada para o cadastro das cidades que servem para localizar os clientes, funcionários, fornecedores e afins.
    
    Criada em 15/06/2014. 
    Última alteração em 17/06/2014.
    """

    model = Cidade
    form = CidadeForm
    list_display = ('nome', 'estado')
    search_fields = ['nome',]
    list_filter = ('estado',)



admin.site.register(Cidade, CidadeAdmin)



