#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from django.http import HttpResponseRedirect
from django.conf.urls import patterns
from views import retorna_recebimentos_parcela, retorna_recebimentos_conta
from salmonella.admin import SalmonellaMixin


class RecebimentoAdmin(admin.ModelAdmin):
    form = RecebimentoForm
    model = Recebimento
    list_display = ('id', 'parcelas_contas_receber', 'data', 'valor')
    date_hierarchy = 'data'

    def get_urls(self):
        urls = super(RecebimentoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'recebimentos_parcela/(?P<id_parcela>\d+)/$', self.admin_site.admin_view(retorna_recebimentos_parcela)),
            (r'recebimentos_conta/(?P<id_conta>\d+)/$', self.admin_site.admin_view(retorna_recebimentos_conta)),
        )
        return my_urls + urls


    def get_form(self, request, obj=None, **kwargs):
        form = super(RecebimentoAdmin, self).get_form(request, obj, **kwargs)
        try:
            parcela = request.GET.get('id_parcela', '')
            dados_recebimento = ParcelasContasReceber.objects.get(pk=parcela)
            form.base_fields['juros'].initial = Decimal(dados_recebimento.calculo_juros()).quantize(Decimal("0.00"))
            form.base_fields['multa'].initial = Decimal(dados_recebimento.calculo_multa()).quantize(Decimal("0.00"))
            form.base_fields['valor'].initial = Decimal(dados_recebimento.valor_a_receber()).quantize(Decimal("0.00"))
            form.base_fields['parcelas_contas_receber'].initial = parcela
        except ValueError:
            pass
        return form


    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber',]
        else:
            return []


    def response_add(self, request, obj):
        u""" Adição: Ao clicar em Salvar, redireciona o usuário para a página da conta a receber da parcela da qual estava """

        if '_save' in request.POST:
            return HttpResponseRedirect("../../contasreceber/%s" % (obj.parcelas_contas_receber.contas_receber))
        else:
            return super(RecebimentoAdmin, self).response_add(request, obj)


    def response_change(self, request, obj):
        u""" Edição: Ao clicar em Salvar, redireciona o usuário para a página da conta a receber da parcela da qual estava """

        if '_save' in request.POST:
            return HttpResponseRedirect("../../contasreceber/%s" % (obj.parcelas_contas_receber.contas_receber))
        else:
            return super(RecebimentoAdmin, self).response_change(request, obj)


    def save_model(self, request, obj, form, change):
        if not obj.juros:
            obj.juros = 0.00
        if not obj.multa:
            obj.multa = 0.00
        if not obj.desconto:
            obj.desconto = 0.00
            
        obj.save()



class ParcelasContasReceberInline(admin.TabularInline):
    u"""
    Inline das parcelas de uma conta à receber.
    """
    model = ParcelasContasReceber
    form = ParcelasContasReceberForm
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('id', 'num_parcelas', 'contas_receber', 'formata_data', 'valor', 'encargos_calculados', 'valor_total', 'link_recebimentos_parcela', 'valor_a_receber', 'link_recebimento')
    readonly_fields = ('id', 'num_parcelas', 'contas_receber', 'formata_data', 'encargos_calculados', 'valor_total', 'valor', 'valor_pago', 'valor_a_receber', 'link_recebimento', 'link_recebimentos_parcela')
    extra = 0
    can_delete = False

    def has_add_permission(self, request):
        return False



class ContasReceberAdmin(SalmonellaMixin, admin.ModelAdmin):
    model = ContasReceber
    form = ContasReceberForm
    list_display = ('id', 'venda_associada', 'data', 'descricao', 'status')
    list_filter = ('status', 'vendas',)
    date_hierarchy = 'data'
    salmonella_fields = ('cliente', 'forma_pagamento', 'grupo_encargo',)


    def get_form(self, request, obj=None, **kwargs):
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('status', 'id', 'venda_associada', 'valor_total', 'data', 'descricao', 'cliente', 'forma_pagamento', 'grupo_encargo')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-detalhe',),
                'fields': ('valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_cobrado', 'link_recebimentos_conta', 'valor_total_a_receber')
            }),
        )

        self.suit_form_tabs = (
            ('geral', 'Geral'),
        )

        self.suit_form_includes = []
        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='venda_associada' and x!='id' and x!='status'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='link_recebimentos_conta' and x!='valor_total_cobrado' and x!='valor_total_a_receber' and x!='valor_total_encargos' and x!='valor_total_juros' and x!='valor_total_multa'))
        
        else:
            insert_into_suit_form_tabs = tuple([('detalhe', 'Detalhes da Conta')])
            self.suit_form_tabs += insert_into_suit_form_tabs

            self.suit_form_includes = (
                ('admin/legenda_parcelas_contas_receber.html', '', 'geral'),
            )

        return super(ContasReceberAdmin, self).get_form(request, obj, **kwargs)


    def get_readonly_fields(self, request, obj=None):
        """ Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['status', 'id', 'venda_associada', 'valor_total', 'data', 'descricao', 'cliente', 'forma_pagamento', 'grupo_encargo', 'valor_total_recebido', 'valor_total_juros', 'valor_total_multa', 'valor_total_encargos', 'valor_total_cobrado', 'valor_total_a_receber', 'link_recebimentos_conta',]
        else:
            return ['status', 'id', 'venda_associada', ]


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



class ParcelasContasReceberAdmin(admin.ModelAdmin):
    model = ParcelasContasReceber
    list_display = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas', 'status')
    #readonly_fields = ('id', 'contas_receber', 'vencimento', 'valor', 'num_parcelas',)



admin.site.register(ContasReceber, ContasReceberAdmin)
admin.site.register(ParcelasContasReceber, ParcelasContasReceberAdmin)
admin.site.register(Recebimento, RecebimentoAdmin)