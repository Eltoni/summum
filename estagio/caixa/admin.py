#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *


class CaixaAdmin(admin.ModelAdmin):
    model = Caixa
    list_display = ('id', 'data', 'valor_fechamento', 'status')



class MovimentosCaixaAdmin(admin.ModelAdmin):
    model = MovimentosCaixa
    list_display = ('id', 'caixa', 'pagamento', 'tipo_mov', 'valor')
    #readonly_fields = ('status', 'id', 'compras', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento',)



admin.site.register(Caixa, CaixaAdmin)
admin.site.register(MovimentosCaixa, MovimentosCaixaAdmin)