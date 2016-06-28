#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from daterange_filter.filter import DateRangeFilter

from notificacao.models import Mensagem, Anexo
from notificacao.forms import MensagemForm, AnexoFormSet


class AnexoInline(admin.TabularInline):
    model = Anexo
    formset = AnexoFormSet
    fields = ('arquivo_anexo',)
    extra = 3
    suit_classes = 'suit-tab suit-tab-anexos'


class MensagemAdmin(admin.ModelAdmin):
    form = MensagemForm
    list_display = ('id', 'assunto', 'data_envio', 'enviado')
    search_fields = ['id', 'assunto']
    date_hierarchy = 'data_envio'
    list_filter = (('data_envio', DateRangeFilter), 'enviado',)
    readonly_fields = ['enviado', 'endereco_email_enviado']
    inlines = [AnexoInline,]
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral full-width',),
            'fields': ('texto',)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('assunto', 'destinatario', 'destinatario_lote', 'data_envio', 'enviado')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-logs',),
            'fields': ('endereco_email_enviado',)
        }),
    )
    
    suit_form_tabs = (
        ('geral', _(u"Geral")),
        ('anexos', _(u"Anexos")),
        ('tags', _(u"Tags")),
        ('logs', _(u"Logs")),
    )

    suit_form_includes = (
        ('admin/legenda_tags_disponiveis.html', '', 'tags'),
    )


admin.site.register(Mensagem, MensagemAdmin)