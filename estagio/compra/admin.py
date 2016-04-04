#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from salmonella.admin import SalmonellaMixin
from import_export.admin import ExportMixin
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter

import datetime
import copy

from compra.models import *
from compra.forms import *
from compra.views import get_valor_unitario
from compra.export import CompraResource
from configuracoes.models import Parametrizacao
from app_global.widgets import NoAddingRelatedFieldWidgetWrapper


class ItensCompraInline(SalmonellaMixin, admin.TabularInline):
    form = ItensCompraForm
    formset = ItensCompraFormSet
    model = ItensCompra
    # can_delete = False
    fields = ('produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total')
    salmonella_fields = ('produto',)
    template = "admin/edit_inline/tabular.html"  # Chama o template personalizado para realizar da inline para fazer todo o tratamento necessário para a tela de compras


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
            if obj.pedido == 'N' or obj.status or (obj.pedido == 'S' and obj.status_pedido):
                return ['produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total',]
            return []
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

    list_display = ('id', 'formata_data_compra', 'fornecedor', 'forma_pagamento', 'total', 'pedido', 'status_pedido', 'status')
    search_fields = ['id', 'fornecedor__nome']
    date_hierarchy = 'data_compra'
    list_filter = (('fornecedor', SelectableFilter), ('data_compra', DateRangeFilter), 'forma_pagamento', 'status', 'pedido', 'status_pedido')
    readonly_fields = ('data_compra',)
    salmonella_fields = ('fornecedor', 'forma_pagamento', 'grupo_encargo',)
    # raw_id_fields = ('fornecedor',)

    suit_js_includes = [
            'js/inline_compra.js',
    ]

    data = datetime.datetime.utcnow().replace(tzinfo=utc)

    def get_urls(self):
        urls = super(CompraAdmin, self).get_urls()
        my_urls = [
            url(r'^get_valor_unitario/(?P<id>\d+)/$', self.admin_site.admin_view(get_valor_unitario)),
            url(r'^(\d+)/change/copia_novo_pedido/$', self.admin_site.admin_view(self.copia_novo_pedido))
        ]
        return my_urls + urls


    def copia_novo_pedido(self, request, id):
        if not self.has_add_permission(request):
            raise PermissionDenied

        # Copia a compra
        obj = Compra.objects.get(pk=id)
        novo_pedido = copy.copy(obj)
        novo_pedido.id = None
        novo_pedido.data_compra = None
        novo_pedido.data_cancelamento = None
        novo_pedido.status = False
        novo_pedido.pedido = 'S'
        novo_pedido.status_pedido = False
        novo_pedido.observacao = _(u"Copiado originalmente como novo pedido através de registro n° %(compra)s.") % {'compra': id}
        novo_pedido.data_pedido = self.data
        novo_pedido.save()

        # Copia os itens de compra
        itens = ItensCompra.objects.filter(compras__pk=id)
        for i in itens:
            item_obj = ItensCompra.objects.get(pk=str(i))
            novo_item = copy.copy(item_obj)
            novo_item.id = None
            novo_item.compras = novo_pedido
            novo_item.save()

        # Registra o log da ação
        LogEntry.objects.log_action(
            user_id         = request.user.pk, 
            content_type_id = ContentType.objects.get_for_model(novo_pedido).pk,
            object_id       = novo_pedido.pk,
            object_repr     = force_text(novo_pedido), 
            action_flag     = ADDITION
        )

        # Constrói a url de retorno
        url = reverse("admin:compra_compra_change", args=[novo_pedido.id])

        return HttpResponseRedirect(url)

    
    def get_form(self, request, obj=None, **kwargs):
        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
            ('info_adicionais', _(u"Informações adicionais"))
        )

        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('total', 'desconto', 'status', 'data_cancelamento')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('fornecedor', 'forma_pagamento', 'grupo_encargo', 'data_compra', 'conta_associada')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-info_adicionais',),
                'fields': ('observacao', 'pedido', 'status_pedido', 'data_pedido', 'status_apoio')
            }),
        )

        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status' and x!='data_cancelamento'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='data_compra' and x!='conta_associada'))
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='pedido' and x!='status_pedido' and x!='data_pedido'))

        else:
            if not obj.status:
                self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='data_cancelamento'))

            if obj.pedido == 'N':
                self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='status_pedido' and x!='data_pedido'))

            if obj.pedido == 'S' and not obj.status_pedido:
                # self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status'))
                self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='data_compra'))

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
            if obj.pedido == 'N' or obj.status or (obj.pedido == 'S' and obj.status_pedido):
                return ['total', 'data_compra', 'data_pedido', 'data_cancelamento', 'desconto', 'fornecedor', 'forma_pagamento', 'pedido', 'status_pedido', 'grupo_encargo', 'status', 'formata_data_compra', 'conta_associada']
            return ['data_compra', 'data_pedido', 'data_cancelamento', 'status', 'pedido', 'status_pedido', 'formata_data_compra', 'conta_associada']
        else:
            return ['data_compra', 'data_pedido', 'data_cancelamento', 'status', 'pedido', 'status_pedido', 'formata_data_compra', 'conta_associada']


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
            obj.data_pedido = self.data
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            obj.pedido = 'N'
            obj.data_compra = self.data
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
            obj.data_compra = self.data
            obj.save()
            self.save_itens_compra(obj.pk)
            return HttpResponseRedirect("../%s" % (obj.pk))

        if '_addcancelacompra' in request.POST:
            obj.botao_acionado = '_addcancelacompra'
            obj.data_cancelamento = self.data
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