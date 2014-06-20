#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from import_export.admin import ExportMixin
from export import ClienteResource, FornecedorResource, FuncionarioResource, CargoResource


class BaseCadastroPessoaAdmin(admin.ModelAdmin):
    model = BaseCadastroPessoa
    form = BaseCadastroPessoaForm

    list_display = ('nome', 'email', 'data')
    list_filter = ('ativo', 'cidade')
    search_fields = ['nome', 'email', 'cpf',]
    date_hierarchy = 'data'
    readonly_fields = ('id', 'data')

    suit_form_tabs = (
        ('geral', 'Geral'),
        ('endereco', 'Endereço'),
        ('identidade', 'Identidade')
    )



class ClienteAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = ClienteResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Cliente
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'telefone', 'celular', 'email', 'ativo')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('id', 'data')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-identidade',),
            'fields': ('cpf', 'rg', 'data_nasc', 'observacao')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-endereco',),
            'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
        }),
    )



class FornecedorAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = FornecedorResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Fornecedor
    form = FornecedorForm

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'telefone', 'celular', 'email', 'ativo')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('id', 'data')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-identidade',),
            'fields': ('tipo_pessoa', 'cnpj', 'razao_social', 'cpf', 'data_nasc', 'observacao')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-endereco',),
            'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
        }),
    )



class CargoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CargoResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Cargo
    list_display = ('nome', 'descricao')



class FuncionarioAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = FuncionarioResource
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = Funcionario

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('usuario', 'cargo', 'salario')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'telefone', 'celular', 'email', 'ativo', 'observacao')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('id', 'data')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-endereco',),
            'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-identidade',),
            'fields': ('cpf', 'rg', 'data_nasc')
        }),
    )



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)