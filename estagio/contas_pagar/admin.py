#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.conf.urls import patterns
from views import retorna_pagamentos_parcela, retorna_pagamentos_conta
from salmonella.admin import SalmonellaMixin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from export import ContasPagarResource
from daterange_filter.filter import DateRangeFilter


class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm
    model = Pagamento
    list_display = ('id', 'parcelas_contas_pagar', 'data', 'valor')
    date_hierarchy = 'data'

    def get_urls(self):
        urls = super(PagamentoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'pagamentos_parcela/(?P<id_parcela>\d+)/$', self.admin_site.admin_view(retorna_pagamentos_parcela)),
            (r'pagamentos_conta/(?P<id_conta>\d+)/$', self.admin_site.admin_view(retorna_pagamentos_conta)),
        )
        return my_urls + urls


    def get_form(self, request, obj=None, **kwargs):
        form = super(PagamentoAdmin, self).get_form(request, obj, **kwargs)
        try:
            parcela = request.GET.get('id_parcela', '')
            dados_pagamento = ParcelasContasPagar.objects.get(pk=parcela)
            form.base_fields['juros'].initial = Decimal(dados_pagamento.calculo_juros()).quantize(Decimal("0.00"))
            form.base_fields['multa'].initial = Decimal(dados_pagamento.calculo_multa()).quantize(Decimal("0.00"))
            form.base_fields['valor'].initial = Decimal(dados_pagamento.valor_a_pagar()).quantize(Decimal("0.00"))
            form.base_fields['parcelas_contas_pagar'].initial = parcela
        except ValueError:
            pass
        return form


    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar',]
        else:
            return []


    def response_add(self, request, obj):
        u""" Adição: Ao clicar em Salvar, redireciona o usuário para a página da conta a pagar da parcela da qual estava """

        if '_save' in request.POST:
            return HttpResponseRedirect("../../contaspagar/%s" % (obj.parcelas_contas_pagar.contas_pagar))
        else:
            return super(PagamentoAdmin, self).response_add(request, obj)


    def response_change(self, request, obj):
        u""" Edição: Ao clicar em Salvar, redireciona o usuário para a página da conta a pagar da parcela da qual estava """

        if '_save' in request.POST:
            return HttpResponseRedirect("../../contaspagar/%s" % (obj.parcelas_contas_pagar.contas_pagar))
        else:
            return super(PagamentoAdmin, self).response_change(request, obj)


    def save_model(self, request, obj, form, change):
        if not obj.juros:
            obj.juros = 0.00
        if not obj.multa:
            obj.multa = 0.00
        if not obj.desconto:
            obj.desconto = 0.00
            
        obj.save()



class ParcelasContasPagarInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à pagar.
    """
    model = ParcelasContasPagar
    form = ParcelasContasPagarForm
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('id', 'num_parcelas', 'contas_pagar', 'formata_data', 'valor', 'encargos_calculados', 'valor_total', 'link_pagamentos_parcela', 'valor_a_pagar', 'link_pagamento')
    readonly_fields = ('id', 'num_parcelas', 'contas_pagar', 'formata_data', 'encargos_calculados', 'valor_total', 'valor', 'valor_pago', 'valor_a_pagar', 'link_pagamento', 'link_pagamentos_parcela')
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class ContasPagarAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = ContasPagarResource
    model = ContasPagar
    form = ContasPagarForm
    list_display = ('id', 'compra_associada', 'data', 'descricao', 'status')
    list_filter = (('data', DateRangeFilter), 'status', 'compras',)
    date_hierarchy = 'data'
    salmonella_fields = ('fornecedores', 'forma_pagamento', 'grupo_encargo',)


    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status', 'id', 'compra_associada', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento', 'grupo_encargo')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhe',),
                'fields': ('valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_cobrado', 'link_pagamentos_conta', 'valor_total_a_pagar')
            }),
        )

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
        )

        self.suit_form_includes = []
        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='compra_associada' and x!='id' and x!='status'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='link_pagamentos_conta' and x!='valor_total_cobrado' and x!='valor_total_a_pagar' and x!='valor_total_encargos' and x!='valor_total_juros' and x!='valor_total_multa'))
        
        else:
            insert_into_suit_form_tabs = tuple([('detalhe', _(u"Detalhes da Conta"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

            self.suit_form_includes = (
                ('admin/legenda_parcelas_contas_pagar.html', '', 'geral'),
            )

        return super(ContasPagarAdmin, self).get_form(request, obj, **kwargs)



    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'compra_associada', 'valor_total', 'data', 'descricao', 'fornecedores', 'forma_pagamento', 'grupo_encargo', 'valor_total_pago', 'valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_cobrado', 'valor_total_a_pagar', 'link_pagamentos_conta',]
        else:
            return ['status', 'id', 'compra_associada', ]


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



class ParcelasContasPagarAdmin(admin.ModelAdmin):
    model = ParcelasContasPagar
    list_display = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas', 'status')
    #readonly_fields = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas',)



admin.site.register(ContasPagar, ContasPagarAdmin)
admin.site.register(ParcelasContasPagar, ParcelasContasPagarAdmin)
admin.site.register(Pagamento, PagamentoAdmin)