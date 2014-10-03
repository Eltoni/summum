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



class ParcelasContasPagarInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à pagar.
    """
    model = ParcelasContasPagar
    fields = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas', 'status')
    readonly_fields = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas',)
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class ContasPagarAdmin(admin.ModelAdmin):
    model = ContasPagar
    list_display = ('id', 'compra_associada', 'data', 'descricao', 'status')
    list_filter = ('status', 'compras',)

    inlines = [ 
        ParcelasContasPagarInline,
    ]

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('status', 'id', 'compra_associada', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento')
        }),
    )
    
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'compra_associada', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento',]
        else:
            return ['status', 'id', 'compra_associada', ]



class ParcelasContasPagarAdmin(admin.ModelAdmin):
    model = ParcelasContasPagar
    list_display = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas', 'status')
    #readonly_fields = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas',)



admin.site.register(ContasPagar, ContasPagarAdmin)
admin.site.register(ParcelasContasPagar, ParcelasContasPagarAdmin)
admin.site.register(Pagamento, PagamentoAdmin)