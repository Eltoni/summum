#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *


class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm
    model = Pagamento
    list_display = ('id', 'parcelas_contas_pagar', 'data', 'valor')

    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['data', 'valor', 'juros', 'desconto', 'parcelas_contas_pagar',]
        else:
            return []



class ContasPagarAdmin(admin.ModelAdmin):
    model = ContasPagar
    list_display = ('id', 'compras', 'data', 'descricao', 'status')
    readonly_fields = ('status', 'id', 'compras', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento',)



class ParcelasContasPagarAdmin(admin.ModelAdmin):
    model = ParcelasContasPagar
    list_display = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas', 'status')
    readonly_fields = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas',)



admin.site.register(ContasPagar, ContasPagarAdmin)
admin.site.register(ParcelasContasPagar, ParcelasContasPagarAdmin)
admin.site.register(Pagamento, PagamentoAdmin)