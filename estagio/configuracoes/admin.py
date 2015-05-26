#-*- coding: UTF-8 -*-
from django.contrib import admin
from configuracoes.models import *
from configuracoes.forms import *
from django.utils.translation import ugettext_lazy as _
from suit.admin import SortableTabularInline


class OrdemModelosInline(SortableTabularInline):
    #form = OrdemModelosForm
    model = OrdemModelos
    fields = ('campo', 'classe', 'exibe_listagem_principal', 'permite_exportar',)
    readonly_fields = ('campo', 'classe',)
    extra = 0
    verbose_name_plural = 'Listagem (Compra)'
    sortable = 'ordem'
    suit_classes = 'suit-tab suit-tab-ordem'

    def has_delete_permission(self, request, obj=None):
        u""" Não permite deleção do registro de parametrização do sistema. """
        return False

    def has_add_permission(self, request):
        u""" Não permite adicionar outros registros de parametrização do sistema. """
        return False


class OrdemModelosVendaInline(OrdemModelosInline):
    verbose_name_plural = 'Listagem (Venda)'

    def get_queryset(self, request):
        get_queryset = self.model.objects.filter(classe='Venda')
        return get_queryset


class OrdemModelosCompraInline(OrdemModelosInline):
    verbose_name_plural = 'Listagem (Compra)'

    def get_queryset(self, request):
        get_queryset = self.model.objects.filter(classe='Compra')
        return get_queryset


class OrdemModelosMovimentoInline(OrdemModelosInline):
    verbose_name_plural = 'Listagem (Produtos)'

    def get_queryset(self, request):
        get_queryset = self.model.objects.filter(classe='Produtos')
        return get_queryset



class ParametrizacaoAdmin(admin.ModelAdmin):
    inlines = (OrdemModelosMovimentoInline, OrdemModelosCompraInline, OrdemModelosVendaInline)
    actions = None
    form = ParametrizacaoForm
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': (
                'perc_valor_minimo_pagamento',
            )
        }),
        ('Caixa', {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': (
                'email_abertura_caixa',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-compra',),
            'fields': (
                'quantidade_inlines_compra',
                'habilita_pedido_compra',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-venda',),
            'fields': (
                'quantidade_inlines_venda',
                'habilita_pedido_venda',
            )
        }),
        ('Entrega', {
            'classes': ('suit-tab suit-tab-venda',),
            'fields': (
                'intervalo_dias_entrega_venda',
            )
        }),
        (None, {
            'classes': ('suit-tab suit-tab-relatorios',),
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
        ('ordem', _(u"Ordem")),
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