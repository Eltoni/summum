#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *


class RecebimentoAdmin(admin.ModelAdmin):
    form = RecebimentoForm
    model = Recebimento
    list_display = ('id', 'parcelas_contas_receber', 'data', 'valor')

    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['data', 'valor', 'juros', 'desconto', 'parcelas_contas_receber',]
        else:
            return []



class ParcelasContasReceberInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à receber.
    """
    model = ParcelasContasReceber
    form = ParcelasContasReceberForm
    fields = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas', 'status')
    readonly_fields = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas',)
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class ContasReceberAdmin(admin.ModelAdmin):
    model = ContasReceber
    form = ContasReceberForm
    list_display = ('id', 'venda_associada', 'data', 'descricao', 'status')
    list_filter = ('status', 'vendas',)

    inlines = [ 
        ParcelasContasReceberInline,
    ]

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('status', 'id', 'venda_associada', 'valor_total', 'data', 'descricao', 'cliente', 'forma_pagamento')
        }),
    )
    
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'venda_associada', 'valor_total', 'data', 'descricao', 'cliente', 'forma_pagamento',]
        else:
            return ['status', 'id', 'venda_associada', ]



class ParcelasContasReceberAdmin(admin.ModelAdmin):
    model = ParcelasContasReceber
    list_display = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas', 'status')
    #readonly_fields = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas',)



admin.site.register(ContasReceber, ContasReceberAdmin)
admin.site.register(ParcelasContasReceber, ParcelasContasReceberAdmin)
admin.site.register(Recebimento, RecebimentoAdmin)