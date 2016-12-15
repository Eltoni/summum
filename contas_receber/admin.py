#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _
from salmonella.admin import SalmonellaMixin
from import_export.admin import ExportMixin
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter

from contas_receber.models import ContasReceber, ParcelasContasReceber, Recebimento
from contas_receber.forms import ContasReceberForm, RecebimentoForm, ParcelasContasReceberForm
from contas_receber.views import EfetivaRecebimentoParcela, retorna_recebimentos_parcela, retorna_recebimentos_conta
from contas_receber.export import ContasReceberResource, ParcelasContasReceberResource


class RecebimentoAdmin(admin.ModelAdmin):
    form = RecebimentoForm
    model = Recebimento
    list_display = ('id', 'parcelas_contas_receber', 'conta_associada', 'data', 'valor', 'juros', 'multa', 'desconto')
    date_hierarchy = 'data'

    def get_urls(self):
        urls = super(RecebimentoAdmin, self).get_urls()
        my_urls = [
            url(r'recebimentos_parcela/(?P<id_parcela>\d+)/$', self.admin_site.admin_view(retorna_recebimentos_parcela)),
            url(r'recebimentos_conta/(?P<id_conta>\d+)/$', self.admin_site.admin_view(retorna_recebimentos_conta)),
            url(r'efetiva_recebimento_parcela/(?P<id_parcela>\d+)/$', permission_required('contas_receber.add_recebimento')(EfetivaRecebimentoParcela.as_view())),
        ]
        return my_urls + urls


    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber', 'conta_associada', 'observacao']
        else:
            return []


    def has_add_permission(self, request):
        return False



class ParcelasContasReceberInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à receber.
    """
    model = ParcelasContasReceber
    form = ParcelasContasReceberForm
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('id', 'num_parcelas', 'contas_receber', 'formata_data', 'valor', 'encargos_calculados', 'valor_desconto', 'valor_total', 'cor_valor_pago', 'valor_a_receber', 'acoes_parcela')
    readonly_fields = ('id', 'num_parcelas', 'contas_receber', 'formata_data', 'encargos_calculados', 'valor_desconto', 'valor_total', 'valor', 'valor_pago', 'valor_a_receber', 'acoes_parcela', 'cor_valor_pago')
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class VendaAssociadaListFilter(admin.SimpleListFilter):
    title = ('Oriundo de venda')
    parameter_name = 'vendas'

    def lookups(self, request, model_admin):
        return (
            ('sim', ('Sim')),
            ('nao', ('Não')),
            )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(vendas__isnull=False) 
        
        if self.value() == 'nao':
            return queryset.filter(vendas__isnull=True)



class ContasReceberAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = ContasReceberResource
    model = ContasReceber
    form = ContasReceberForm
    search_fields = ['id',]
    list_display = ('id', 'venda_associada', 'data', 'descricao', 'status')
    list_filter = (('cliente', SelectableFilter), ('data', DateRangeFilter), 'status', VendaAssociadaListFilter,)
    date_hierarchy = 'data'
    salmonella_fields = ('cliente', 'forma_pagamento', 'grupo_encargo',)


    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status', 'id', 'venda_associada', 'valor_total', 'data', 'cliente', 'cliente_associado', 'forma_pagamento', 'forma_pagamento_associada', 'grupo_encargo', 'grupo_encargo_associado', 'descricao')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhe',),
                'fields': ('valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_descontos', 'valor_total_cobrado', 'link_recebimentos_conta', 'valor_total_a_receber')
            }),
        )

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
        )

        self.suit_form_includes = []
        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='venda_associada' and x!='id' and x!='status' and x!='cliente_associado' and x!='forma_pagamento_associada' and x!='grupo_encargo_associado'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='link_recebimentos_conta' and x!='valor_total_cobrado' and x!='valor_total_a_receber' and x!='valor_total_encargos' and x!='valor_total_descontos' and x!='valor_total_juros' and x!='valor_total_multa'))
        
        else:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='cliente' and x!='forma_pagamento' and x!='grupo_encargo'))
            obj.usuario_sessao = request.user
            
            insert_into_suit_form_tabs = tuple([('detalhe', _(u"Detalhes da Conta"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

            self.suit_form_includes = (
                ('admin/legenda_parcelas_contas_receber.html', '', 'geral'),
            )

        return super(ContasReceberAdmin, self).get_form(request, obj, **kwargs)


    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'venda_associada', 'cliente_associado', 'forma_pagamento_associada', 'grupo_encargo_associado', 'valor_total', 'data', 'descricao', 'cliente', 'forma_pagamento', 'grupo_encargo', 'valor_total_recebido', 'valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_descontos', 'valor_total_cobrado', 'valor_total_a_receber', 'link_recebimentos_conta',]
        else:
            return ['status', 'id', 'venda_associada', 'cliente_associado', 'forma_pagamento_associada', 'grupo_encargo_associado',]


    # trata as inlines que aparecem na página de conta a pagar
    def get_inline_instances(self, request, obj=None):
        
        self.inlines = []

        try:
            if obj.pk:
                self.inlines.insert(0, ParcelasContasReceberInline)
        except:
            pass

        return super(ContasReceberAdmin, self).get_inline_instances(request, obj)


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if obj.status:
            rowclass = 'success'

        return {'class': rowclass}



class ParcelasContasReceberAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ParcelasContasReceberResource
    model = ParcelasContasReceber
    list_display = ('id', 'conta_associada', 'vencimento', 'valor', 'num_parcelas', 'status')
    list_filter = (('contas_receber__cliente', SelectableFilter), 'status')
    readonly_fields = ('id', 'conta_associada', 'vencimento', 'valor', 'num_parcelas', 'status')
    date_hierarchy = 'vencimento'

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(ContasReceber, ContasReceberAdmin)
admin.site.register(ParcelasContasReceber, ParcelasContasReceberAdmin)
admin.site.register(Recebimento, RecebimentoAdmin)