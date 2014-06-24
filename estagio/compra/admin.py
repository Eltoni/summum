#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *


class ItensCompraInline(admin.TabularInline):
    form = FormFields
    model = ItensCompra
    extra = 3
    fields = ('produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total')



class CompraAdmin(admin.ModelAdmin):
    inlines = [ 
        ItensCompraInline,
    ]
    form = FormFieldsMain
    model = Compra

    search_fields = ['id', 'fornecedor']
    list_filter = ('data', 'status', 'forma_pagamento')
    readonly_fields = ('data',)


    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('total', 'desconto', 'status')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('fornecedor', 'forma_pagamento', 'data')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-info_adicionais',),
            'fields': ('observacao',)
        }),
    )

    suit_form_tabs = (
        ('geral', 'Geral'),
        ('info_adicionais', 'Informações adicionais')
    )


class PagamentoAdmin(admin.ModelAdmin):
    model = Pagamento
    list_display = ('id', 'data', 'valor')


admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Compra, CompraAdmin)