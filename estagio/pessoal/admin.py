#-*- coding: UTF-8 -*-
from django.contrib import admin
from pessoal.models import *
from pessoal.forms import *
from import_export.admin import ExportMixin
from sorl.thumbnail.admin import AdminImageMixin
from pessoal.export import ClienteResource, FornecedorResource, FuncionarioResource, CargoResource
from contas_receber.models import ContasReceber, ParcelasContasReceber
from contas_pagar.models import ContasPagar, ParcelasContasPagar
from django.contrib.admin.views.main import IS_POPUP_VAR
from app_global.admin import GlobalAdmin
from django.utils.translation import ugettext_lazy as _
import xml.etree.ElementTree
from selectable_filter.filter import SelectableFilter


def remove_tags(text):
    """Remove elementos html de uma string e retorna o resultado"""
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())


class StatusFinanceiroFilter(admin.SimpleListFilter):
    title = 'Status Financeiro'
    parameter_name = 'status_financeiro'
    def lookups(self, request, model_admin):
        return (
            ('Adimplente', 'Adimplente'),
            ('Inadimplente', 'Inadimplente'),
        )
    def queryset(self, request, queryset):
        if self.value():
            array = []
            for element in queryset:
                if self.value() == 'Adimplente' and remove_tags(element.status_financeiro.__call__()) == 'Adimplente':
                    array.append(element.id)
                if self.value() == 'Inadimplente' and remove_tags(element.status_financeiro.__call__()) == 'Inadimplente':
                    array.append(element.id)
            return queryset.filter(pk__in=array)



class BaseCadastroPessoaAdmin(AdminImageMixin, GlobalAdmin):
    model = BaseCadastroPessoa
    form = BaseCadastroPessoaForm

    list_display = ('nome', 'email', 'data')
    list_filter = (('cidade', SelectableFilter), 'status')
    popup_list_filter = ('cidade',)
    search_fields = ['nome', 'email', 'cpf',]
    date_hierarchy = 'data'
    readonly_fields = ('id', 'data', 'formata_data_nascimento')

    suit_form_tabs = (
        ('geral', _(u"Geral")),
        ('endereco', _(u"Endereço")),
        ('identidade', _(u"Identidade")),
        ('detalhes', _(u"Detalhes")),
    )

    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if not obj.status:
            rowclass = 'error'

        return {'class': rowclass}


    def get_queryset(self, request):
        qs = super(BaseCadastroPessoaAdmin, self).get_queryset(request)
        
        if IS_POPUP_VAR in request.GET:  
            return qs.filter(status=True)
        return qs



class ContasReceberInline(admin.TabularInline):
    model = ContasReceber
    ordering = ("status", "pk",)
    suit_classes = 'suit-tab suit-tab-financeiro'
    extra = 0
    fields = ('link_conta', 'data', 'venda_associada', 'valor_total', 'descricao', 'status')
    readonly_fields = ('link_conta', 'data', 'venda_associada', 'valor_total', 'descricao', 'status')

    def save_formset(self, request, form, formset, change):
        pass

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def link_conta(object, instance):
        return "<a href=\"/%s/%s/%s\" target='_blank'>%s</a>" % (instance._meta.app_label, instance._meta.module_name, instance.id, instance.id,)
    
    link_conta.allow_tags = True
    link_conta.short_description = _(u"ID")

# class ParcelasContasReceberInline(admin.TabularInline):
#     model = ParcelasContasReceber
#     #fk_name = cliente_associado()
#     suit_classes = 'suit-tab suit-tab-financeiro'
#     extra = 0
#     fields = ('id', 'vencimento', 'valor',)
#     readonly_fields = ('id', 'vencimento', 'valor',)

#     def save_formset(self, request, form, formset, change):
#         pass

#     def has_add_permission(self, request):
#         return False

#     def has_delete_permission(self, request, obj=None):
#         return False


class EnderecoEntregaClienteInline(admin.StackedInline):
    model = EnderecoEntregaCliente
    form = EnderecoEntregaClienteForm
    template = "admin/pessoal/edit_inline/stacked.html"
    ordering = ("status", "pk",)
    suit_classes = 'suit-tab suit-tab-endereco'
    extra = 0
    fields = ('status', ('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep', 'observacao',)



class ClienteAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = ClienteResource
    model = Cliente
    form = ClienteForm
    readonly_fields = ('status_financeiro', 'id', 'data', 'formata_data_nascimento')
    list_display = ('nome', 'email', 'data', 'status_financeiro',)
    list_filter = (('cidade', SelectableFilter), 'status', StatusFinanceiroFilter)

    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status_financeiro', 'nome', 'telefone', 'celular', 'email', 'status')
            }),
            ('Informações do cadastro', {
                'classes': ('suit-tab suit-tab-geral collapse',),
                'fields': ('id', 'data')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('tipo_pessoa', 'cnpj', 'razao_social', 'cpf', 'rg', 'data_nasc', 'formata_data_nascimento')
            }),
            ('Dados bancários', {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('banco', 'agencia', 'conta_banco')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-endereco',),
                'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhes',),
                'fields': ('sexo', 'estado_civil', 'foto', 'observacao',)
            }),
        )

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
            ('endereco', _(u"Endereço")),
            ('identidade', _(u"Identidade")),
            ('detalhes', _(u"Detalhes")),
        )

        if obj is None:
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='id' and x!='data'))
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status_financeiro'))
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='formata_data_nascimento'))

        else:
            insert_into_suit_form_tabs = tuple([('financeiro', _(u"Financeiro"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

        return super(ClienteAdmin, self).get_form(request, obj, **kwargs)


    def save_model(self, request, obj, form, change):
        # Trata o save no banco de dados para que o registro que seja de pessoa física não seja salvo com dados de pessoa jurídica e vice-versa
        if obj.tipo_pessoa == 'PJ':
            obj.cpf = None
        else:
            obj.cnpj = None
            obj.razao_social = None

        obj.save()


    # trata as inlines que aparecem no resumo financeiro dos clientes
    def get_inline_instances(self, request, obj=None):
        
        self.inlines = [EnderecoEntregaClienteInline,]

        #self.inlines.insert(1, ParcelasContasReceberInline)
        try:
            tem_contas = ContasReceber.objects.filter(cliente=obj.pk).exists()
            if tem_contas:
                self.inlines.insert(1, ContasReceberInline)

        except:
            pass

        return super(ClienteAdmin, self).get_inline_instances(request, obj)



class ContasPagarInline(admin.TabularInline):
    model = ContasPagar
    ordering = ("status", "pk",)
    suit_classes = 'suit-tab suit-tab-financeiro'
    extra = 0
    fields = ('link_conta', 'data', 'compra_associada', 'valor_total', 'descricao', 'status')
    readonly_fields = ('link_conta', 'data', 'compra_associada', 'valor_total', 'descricao', 'status')

    def save_formset(self, request, form, formset, change):
        pass

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def link_conta(object, instance):
        return "<a href=\"/%s/%s/%s\" target='_blank'>%s</a>" % (instance._meta.app_label, instance._meta.module_name, instance.id, instance.id,)
    
    link_conta.allow_tags = True
    link_conta.short_description = _(u"ID")



class FornecedorAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = FornecedorResource
    model = Fornecedor
    form = FornecedorForm
    readonly_fields = ('status_financeiro', 'id', 'data', 'formata_data_nascimento')
    list_display = ('nome', 'email', 'status', 'status_financeiro')
    list_filter = (('cidade', SelectableFilter), 'status', StatusFinanceiroFilter)
    popup_list_display = ('nome', 'email', 'status', 'status_financeiro')


    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status_financeiro', 'nome', 'telefone', 'celular', 'email', 'status')
            }),
            ('Informações do cadastro', {
                'classes': ('suit-tab suit-tab-geral collapse',),
                'fields': ('id', 'data')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('tipo_pessoa', 'cnpj', 'razao_social', 'cpf', 'rg', 'data_nasc', 'formata_data_nascimento')
            }),
            ('Dados bancários', {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('banco', 'agencia', 'conta_banco')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-endereco',),
                'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhes',),
                'fields': ('sexo', 'estado_civil', 'foto', 'observacao',)
            }),
        )

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
            ('endereco', _(u"Endereço")),
            ('identidade', _(u"Identidade")),
            ('detalhes', _(u"Detalhes")),
        )

        if obj is None:
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='id' and x!='data'))
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status_financeiro'))
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='formata_data_nascimento'))
        
        else:
            insert_into_suit_form_tabs = tuple([('financeiro', _(u"Financeiro"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

        return super(FornecedorAdmin, self).get_form(request, obj, **kwargs)


    def save_model(self, request, obj, form, change):
        # Trata o save no banco de dados para que o registro que seja de pessoa física não seja salvo com dados de pessoa jurídica e vice-versa
        if obj.tipo_pessoa == 'PJ':
            obj.cpf = None
        else:
            obj.cnpj = None
            obj.razao_social = None

        obj.save()


    # trata as inlines que aparecem no resumo financeiro dos fornecedores
    def get_inline_instances(self, request, obj=None):
        
        self.inlines = []

        try:
            tem_contas = ContasPagar.objects.filter(fornecedores=obj.pk).exists()
            if tem_contas:
                self.inlines.insert(0, ContasPagarInline)

        except:
            pass

        return super(FornecedorAdmin, self).get_inline_instances(request, obj)



class CargoAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CargoResource
    model = Cargo
    list_display = ('nome', 'descricao')



class FuncionarioAdmin(ExportMixin, BaseCadastroPessoaAdmin):
    resource_class = FuncionarioResource
    model = Funcionario
    form = FuncionarioForm

    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            ('Informações profissionais', {
                'classes': ('suit-tab suit-tab-geral',),
                'description': 'Dados do usuário',
                'fields': ('usuario', 'cargo', 'salario')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('nome', 'telefone', 'celular', 'email', 'status')
            }),
            ('Informações do cadastro', {
                'classes': ('suit-tab suit-tab-geral collapse',),
                'fields': ('id', 'data')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-endereco',),
                'fields': (('endereco', 'numero'), 'complemento', 'bairro', ('estado', 'cidade'), 'cep')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('cpf', 'rg', 'data_nasc', 'formata_data_nascimento')
            }),
            ('Dados bancários', {
                'classes': ('suit-tab suit-tab-identidade',),
                'fields': ('banco', 'agencia', 'conta_banco')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhes',),
                'fields': ('sexo', 'estado_civil', 'foto', 'observacao',)
            }),
        )

        if obj is None:
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='id' and x!='data'))
            self.fieldsets[4][1]['fields'] = tuple(x for x in self.fieldsets[4][1]['fields'] if (x!='formata_data_nascimento'))

        return super(FuncionarioAdmin, self).get_form(request, obj, **kwargs)



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)