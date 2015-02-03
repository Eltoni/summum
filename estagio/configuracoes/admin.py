#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *


class ParametrizacaoAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': (
                'quantidade_inlines_compra',
                'quantidade_inlines_venda',
                'habilita_pedido_compra',
                'habilita_pedido_venda',
                'qtde_minima_produtos_em_estoque'
            )
        }),
    )
    
    suit_form_tabs = (
        ('geral', 'Geral'),
    )

    def has_delete_permission(self, request, obj=None):
        u""" Não permite deleção do registro de parametrização do sistema. """
        return False

    def has_add_permission(self, request):
        u""" Não permite adicionar outros registros de parametrização do sistema. """
        return False


admin.site.register(Parametrizacao, ParametrizacaoAdmin)