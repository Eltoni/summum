#-*- coding: UTF-8 -*-
from django.contrib import admin
from import_export.admin import ExportMixin
from export import ProdutosResource
from app_global.admin import GlobalAdmin
from django.contrib.admin.views.main import IS_POPUP_VAR
from sorl.thumbnail.admin import AdminImageMixin
from salmonella.admin import SalmonellaMixin
from models import *


class MarcaAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Marca
    fields = ('nome', 'logo', 'descricao')


class CategoriaAdmin(admin.ModelAdmin):
    model = Categoria
    fields = ('nome', 'descricao')


class ProdutosAdmin(ExportMixin, SalmonellaMixin, GlobalAdmin):
    resource_class = ProdutosResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Produtos
    filter_horizontal = ('categorias',)
    salmonella_fields = ('marca',)
    popup_list_display = ('nome', 'marca', 'quantidade', 'descricao')
    list_display = ('nome', 'quantidade', 'descricao', 'status')
    list_filter = ('status',)
    search_fields = ['nome',]
    readonly_fields = ('quantidade',)

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'preco', 'preco_venda', 'quantidade', 'status')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-detalhes',),
            'fields': ('descricao', 'marca', 'categorias')
        }),
    )

    suit_form_tabs = (
        ('geral', 'Geral'),
        ('detalhes', 'Detalhes'),
    )

    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if not obj.status:
            rowclass = 'error'

        return {'class': rowclass}


    def queryset(self, request):
        qs = super(ProdutosAdmin, self).queryset(request)
        if IS_POPUP_VAR in request.GET:  
            return qs.filter(status=True)
        return qs



admin.site.register(Produtos, ProdutosAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)