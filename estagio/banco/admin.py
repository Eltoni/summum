#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin

from banco.models import *
from banco.forms import *


class AgenciaInline(admin.TabularInline):
    model = Agencia
    form = AgenciaForm
    formset = AgenciaFormSet
    fields = ('banco', 'agencia', 'nome', 'endereco', 'numero', 'bairro', 'estado', 'cidade', 'cep', 'contato')


class BancoAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Banco
    list_display = ('banco', 'nome', 'site')
    search_fields = ['banco', 'nome']
    fields = ('banco', 'nome', 'site', 'logo')
    inlines = [AgenciaInline,]

    suit_js_includes = [
            'js/inline_endereco_banco.js',
    ]


admin.site.register(Banco, BancoAdmin)