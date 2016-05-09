#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from configuracoes.models import Parametrizacao
from configuracoes.forms import ParametrizacaoForm


class ParametrizacaoAdmin(admin.ModelAdmin):
    actions = None
    form = ParametrizacaoForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral wide',),
            'fields': (
                'perc_valor_minimo_recebimento',
            )
        }),
        ('Eventos', {
            'classes': ('suit-tab suit-tab-geral wide',),
            'fields': (
                'evento_calendario',
            )
        }),
        ('Caixa', {
            'classes': ('suit-tab suit-tab-geral wide',),
            'fields': (
                'email_abertura_caixa',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-compra wide',),
            'fields': (
                'quantidade_inlines_compra',
                'habilita_pedido_compra',
                'periodo_venc_pedido_compra',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-venda wide',),
            'fields': (
                'quantidade_inlines_venda',
                'habilita_pedido_venda',
                'periodo_venc_pedido_venda',
            )
        }),
        ('Entrega', {
            'classes': ('suit-tab suit-tab-venda wide',),
            'fields': (
                'intervalo_dias_entrega_venda',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-relatorios wide',),
            'fields': (
                'qtde_minima_produtos_em_estoque',
            )
        }),
    )
    
    suit_form_tabs = (
        ('geral', _(u"Geral")),
        ('compra', _(u"Compra")),
        ('venda', _(u"Venda")),
        ('relatorios', _(u"Relatórios")),
    )

    def has_delete_permission(self, request, obj=None):
        u""" Não permite deleção do registro de parametrização do sistema. """
        return False

    def has_add_permission(self, request):
        u""" Não permite adicionar outros registros de parametrização do sistema. """
        parametrizacao = Parametrizacao.objects.filter().exists()
        if parametrizacao:
            return False
        else:
            return True

    def save_model(self, request, obj, form, change):
        if not obj.perc_valor_minimo_recebimento:
            obj.perc_valor_minimo_recebimento = 0

        obj.save()


admin.site.register(Parametrizacao, ParametrizacaoAdmin)