#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from django.http import HttpResponseRedirect
from configuracoes.models import Parametrizacao
from salmonella.admin import SalmonellaMixin
from app_global.widgets import NoAddingRelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from export import CompraResource
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter


class ItensCompraInline(SalmonellaMixin, admin.TabularInline):
    form = ItensCompraForm
    formset = ItensCompraFormSet
    model = ItensCompra
    can_delete = False
    fields = ('produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total')
    salmonella_fields = ('produto',)
    template = "admin/compra/edit_inline/tabular.html"  # Chama o template personalizado para realizar da inline para fazer todo o tratamento necessário para a tela de compras


    def get_formset(self, request, obj=None, **kwargs): 
        u""" Altera a quantidade de inlines definida como padrão caso o registro seja salvo no BD """

        if obj: 
            kwargs['extra'] = 0
        else:
            try:
                quantidade = Parametrizacao.objects.get().quantidade_inlines_compra
            except:
                quantidade = 5

            if quantidade:
                kwargs['extra'] = int(quantidade)
            else: 
                kwargs['extra'] = 5

        return super(ItensCompraInline, self).get_formset(request, obj, **kwargs) 


    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total',]
        else:
            return []



class CompraAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = CompraResource
    inlines = [ 
        ItensCompraInline,
    ]
    form = CompraForm
    model = Compra
    actions = None

    list_display = ('id', 'data', 'total', 'status')
    search_fields = ['id', 'fornecedor__nome']
    date_hierarchy = 'data'
    list_filter = (('fornecedor', SelectableFilter), ('data', DateRangeFilter), 'status', 'forma_pagamento')
    readonly_fields = ('data',)
    salmonella_fields = ('fornecedor', 'forma_pagamento', 'grupo_encargo',)
    # raw_id_fields = ('fornecedor',)

    def get_form(self, request, obj=None, **kwargs):
        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
            ('info_adicionais', _(u"Informações adicionais"))
        )

        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('total', 'desconto', 'status')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('fornecedor', 'forma_pagamento', 'grupo_encargo', 'data')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-info_adicionais',),
                'fields': ('observacao', 'pedido', 'status_pedido',)
            }),
        )

        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='data'))
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='pedido' and x!='status_pedido'))

        else:
            if obj.pedido == 'N':
                self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='status_pedido'))

        return super(CompraAdmin, self).get_form(request, obj, **kwargs)


    def has_delete_permission(self, request, obj=None):
        u""" Somente o usuário admin pode deletar uma compra. """
        if request.user.is_superuser:
            return True

        else:
            return False

    
    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da compra como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['total', 'data', 'desconto', 'fornecedor', 'forma_pagamento', 'pedido', 'status_pedido', 'grupo_encargo', 'status',]
        else:
            return ['data', 'pedido', 'status_pedido']


    def save_itens_compra(self, obj):
        u""" executa o método save para todos os registros de itens de uma compra.
             Criada em 18/11/2014.
         """

        for item in ItensCompra.objects.filter(compras=obj):
            item.save()


    def response_add(self, request, obj):
        u""" Trata a adição da compra dependendo do botão clicado ao salvá-la 
             Criada em 14/11/2014.
        """

        if '_addpedido' in request.POST:
            obj.pedido = 'S'
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            obj.pedido = 'N'
            obj.save()
            self.save_itens_compra(obj.pk)
            return super(CompraAdmin, self).response_add(request, obj)


    def response_change(self, request, obj):
        u""" Trata a alteração da compra dependendo do botão clicado ao salvá-la 
             Criada em 14/11/2014.
        """

        if '_addconfirmapedido' in request.POST:
            obj.status_pedido = True
            obj.status = False
            obj.save()
            self.save_itens_compra(obj.pk)
            return HttpResponseRedirect("../%s" % (obj.pk))

        if '_addcancelacompra' in request.POST:
            obj.botao_acionado = '_addcancelacompra'
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            return super(CompraAdmin, self).response_change(request, obj)


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if obj.status:
            rowclass = 'error'

        return {'class': rowclass}


admin.site.register(Compra, CompraAdmin)