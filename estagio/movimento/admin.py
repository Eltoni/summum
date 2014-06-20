#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from import_export.admin import ExportMixin
from export import ProdutosResource


class ProdutosAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ProdutosResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Produtos
    list_display = ('nome', 'quantidade', 'preco_venda')


admin.site.register(Produtos, ProdutosAdmin)