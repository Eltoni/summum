#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from django.utils.translation import ugettext_lazy as _


class ParametrizacaoAdmin(admin.ModelAdmin):
    form = ParametrizacaoForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': (
                'quantidade_inlines_compra',
                'quantidade_inlines_venda',
                'habilita_pedido_compra',
                'habilita_pedido_venda',
                'qtde_minima_produtos_em_estoque',
                'perc_valor_minimo_pagamento'
            )
        }),
    )
    
    suit_form_tabs = (
        ('geral', _(u"Geral")),
    )

    def has_delete_permission(self, request, obj=None):
        u""" Não permite deleção do registro de parametrização do sistema. """
        return False

    def has_add_permission(self, request):
        u""" Não permite adicionar outros registros de parametrização do sistema. """
        return False

    def save_model(self, request, obj, form, change):
        if not obj.perc_valor_minimo_pagamento:
            obj.perc_valor_minimo_pagamento = 0

        obj.save()


admin.site.register(Parametrizacao, ParametrizacaoAdmin)