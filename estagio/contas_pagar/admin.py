#-*- coding: UTF-8 -*-
from django.contrib import admin
from contas_pagar.models import *
from contas_pagar.forms import *
from django.http import HttpResponseRedirect
from django.conf.urls import patterns
from contas_pagar.views import retorna_pagamentos_parcela, retorna_pagamentos_conta, efetiva_pagamento_parcela
from salmonella.admin import SalmonellaMixin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from contas_pagar.export import ContasPagarResource, ParcelasContasPagarResource
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter
from decimal import Decimal


class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm
    model = Pagamento
    list_display = ('id', 'parcelas_contas_pagar', 'conta_associada', 'data', 'valor', 'juros', 'multa', 'desconto')
    date_hierarchy = 'data'

    def get_urls(self):
        urls = super(PagamentoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'pagamentos_parcela/(?P<id_parcela>\d+)/$', self.admin_site.admin_view(retorna_pagamentos_parcela)),
            (r'pagamentos_conta/(?P<id_conta>\d+)/$', self.admin_site.admin_view(retorna_pagamentos_conta)),
            (r'efetiva_pagamento_parcela/(?P<id_parcela>\d+)/$', self.admin_site.admin_view(efetiva_pagamento_parcela)),
        )
        return my_urls + urls


    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """
    
        if obj:
            return ['data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar', 'conta_associada', 'observacao']
        else:
            return []


    def has_add_permission(self, request):
        return False

    # O pagamento não é mais realizado no formulário original do Django, deste modo, o processo abaixo não é mais utilizado
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(PagamentoAdmin, self).get_form(request, obj, **kwargs)
    #     try:
    #         parcela = request.GET.get('id_parcela', '')
    #         dados_pagamento = ParcelasContasPagar.objects.get(pk=parcela)
    #         form.base_fields['juros'].initial = Decimal(dados_pagamento.calculo_juros()).quantize(Decimal("0.00"))
    #         form.base_fields['multa'].initial = Decimal(dados_pagamento.calculo_multa()).quantize(Decimal("0.00"))
    #         form.base_fields['valor'].initial = Decimal(dados_pagamento.valor_a_pagar()).quantize(Decimal("0.00"))
    #         form.base_fields['parcelas_contas_pagar'].initial = parcela
    #     except ValueError:
    #         pass
    #     return form

    # O pagamento não é mais realizado no formulário original do Django, deste modo, o processo abaixo não é mais utilizado
    # def response_add(self, request, obj):
    #     u""" Adição: Ao clicar em Salvar, redireciona o usuário para a página da conta a pagar da parcela da qual estava """
    #
    #     if '_save' in request.POST:
    #         return HttpResponseRedirect("../../contaspagar/%s" % (obj.parcelas_contas_pagar.contas_pagar))
    #     else:
    #         return super(PagamentoAdmin, self).response_add(request, obj)

    # O pagamento não é mais realizado no formulário original do Django, deste modo, o processo abaixo não é mais utilizado
    # def response_change(self, request, obj):
    #     u""" Edição: Ao clicar em Salvar, redireciona o usuário para a página da conta a pagar da parcela da qual estava """
    #
    #     if '_save' in request.POST:
    #         return HttpResponseRedirect("../../contaspagar/%s" % (obj.parcelas_contas_pagar.contas_pagar))
    #     else:
    #         return super(PagamentoAdmin, self).response_change(request, obj)

    # Tratamento substituído no Form - PagamentoForm
    # def save_model(self, request, obj, form, change):
    #     if not obj.juros:
    #         obj.juros = 0.00
    #     if not obj.multa:
    #         obj.multa = 0.00
    #     if not obj.desconto:
    #         obj.desconto = 0.00
            
    #     obj.save()



class ParcelasContasPagarInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à pagar.
    """
    model = ParcelasContasPagar
    form = ParcelasContasPagarForm
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('id', 'num_parcelas', 'contas_pagar', 'formata_data', 'valor', 'encargos_calculados', 'valor_desconto', 'valor_total', 'cor_valor_pago', 'valor_a_pagar', 'acoes_parcela')
    readonly_fields = ('id', 'num_parcelas', 'contas_pagar', 'formata_data', 'encargos_calculados', 'valor_desconto', 'valor_total', 'valor', 'valor_pago', 'valor_a_pagar', 'acoes_parcela', 'cor_valor_pago')
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class CompraAssociadaListFilter(admin.SimpleListFilter):
    title = ('Oriundo de compra')
    parameter_name = 'compras'

    def lookups(self, request, model_admin):
        return (
            ('sim', ('Sim')),
            ('nao', ('Não')),
            )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(compras__isnull=False) 
        
        if self.value() == 'nao':
            return queryset.filter(compras__isnull=True)



class ContasPagarAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = ContasPagarResource
    model = ContasPagar
    form = ContasPagarForm
    search_fields = ['id',]
    list_display = ('id', 'compra_associada', 'data', 'descricao', 'status')
    list_filter = (('fornecedores', SelectableFilter), ('data', DateRangeFilter), 'status', CompraAssociadaListFilter,)
    date_hierarchy = 'data'
    salmonella_fields = ('fornecedores', 'forma_pagamento', 'grupo_encargo',)


    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status', 'id', 'compra_associada', 'valor_total', 'data', 'fornecedores', 'fornecedor_associado', 'forma_pagamento', 'forma_pagamento_associada', 'grupo_encargo', 'grupo_encargo_associado', 'descricao')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhe',),
                'fields': ('valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_descontos', 'valor_total_cobrado', 'link_pagamentos_conta', 'valor_total_a_pagar')
            }),
        )

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
        )

        self.suit_form_includes = []
        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='compra_associada' and x!='id' and x!='status' and x!='fornecedor_associado' and x!='forma_pagamento_associada' and x!='grupo_encargo_associado'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='link_pagamentos_conta' and x!='valor_total_cobrado' and x!='valor_total_a_pagar' and x!='valor_total_encargos' and x!='valor_total_descontos' and x!='valor_total_juros' and x!='valor_total_multa'))
        
        else:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='fornecedores' and x!='forma_pagamento' and x!='grupo_encargo'))
            obj.usuario_sessao = request.user
            
            insert_into_suit_form_tabs = tuple([('detalhe', _(u"Detalhes da Conta"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

            self.suit_form_includes = (
                ('admin/legenda_parcelas_contas_pagar.html', '', 'geral'),
            )

        return super(ContasPagarAdmin, self).get_form(request, obj, **kwargs)



    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'compra_associada', 'fornecedor_associado', 'forma_pagamento_associada', 'grupo_encargo_associado', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento', 'grupo_encargo', 'valor_total_pago', 'valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_descontos', 'valor_total_cobrado', 'valor_total_a_pagar', 'link_pagamentos_conta',]
        else:
            return ['status', 'id', 'compra_associada', 'fornecedor_associado', 'forma_pagamento_associada', 'grupo_encargo_associado']


    # trata as inlines que aparecem na página de conta a pagar
    def get_inline_instances(self, request, obj=None):
        
        self.inlines = []

        try:
            if obj.pk:
                self.inlines.insert(0, ParcelasContasPagarInline)
        except:
            pass

        return super(ContasPagarAdmin, self).get_inline_instances(request, obj)


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if obj.status:
            rowclass = 'success'

        return {'class': rowclass}



class ParcelasContasPagarAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ParcelasContasPagarResource
    model = ParcelasContasPagar
    list_display = ('id', 'conta_associada', 'vencimento', 'valor', 'num_parcelas', 'status')
    list_filter = (('contas_pagar__fornecedores', SelectableFilter), 'status')
    readonly_fields = ('id', 'conta_associada', 'vencimento', 'valor', 'num_parcelas', 'status')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(ContasPagar, ContasPagarAdmin)
admin.site.register(ParcelasContasPagar, ParcelasContasPagarAdmin)
admin.site.register(Pagamento, PagamentoAdmin)