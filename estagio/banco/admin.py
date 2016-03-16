#-*- coding: UTF-8 -*-
from django.contrib import admin
from banco.models import *
from banco.forms import *
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin


class AgenciaInline(admin.TabularInline):
    model = Agencia
    form = AgenciaForm
    formset = AgenciaFormSet
    # form = EnderecoEntregaClienteForm
    fields = ('banco', 'agencia', 'nome', 'endereco', 'numero', 'bairro', 'estado', 'cidade', 'cep', 'contato')


class BancoAdmin(AdminImageMixin, admin.ModelAdmin):
    #form = BancoForm
    model = Banco
    list_display = ('banco', 'nome',)
    search_fields = ['banco', 'nome']
    fields = ('banco', 'nome', 'logo')
    inlines = [AgenciaInline,]

    suit_js_includes = [
            'js/inline_endereco_banco.js',
    ]


admin.site.register(Banco, BancoAdmin)