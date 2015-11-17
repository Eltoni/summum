#-*- coding: UTF-8 -*-
from django.contrib import admin
from venda.models import *
from venda.forms import *
from venda.views import get_valor_unitario, get_endereco_entrega_cliente, overview_vendas
from django.http import HttpResponseRedirect
from configuracoes.models import Parametrizacao
from salmonella.admin import SalmonellaMixin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from venda.export import VendaResource, EntregaVendaResource
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter
from django.conf.urls import patterns
import datetime
from django.utils.timezone import utc
import copy
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from movimento.models import Produtos
from django.utils.html import format_html
import pandas as pd


class EntregaVendaAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EntregaVendaResource
    model = EntregaVenda
    actions = None

    list_display = ('id_venda', 'link_venda', 'endereco', 'data', 'posicao', 'posicao_mapa')
    search_fields = ['id',]
    date_hierarchy = 'data'
    list_filter = (('data', DateRangeFilter),)
    # readonly_fields = ('data',)

    def posicao_mapa(self, instance):
        if instance.posicao is not None:
            return '<img src="http://maps.googleapis.com/maps/api/staticmap?center=%(latitude)s,%(longitude)s&zoom=%(zoom)s&size=%(width)sx%(height)s&maptype=roadmap&markers=%(latitude)s,%(longitude)s&sensor=false&visual_refresh=true&scale=%(scale)s" width="%(width)s" height="%(height)s">' % {
                'latitude': instance.posicao.latitude,
                'longitude': instance.posicao.longitude,
                'zoom': 15,
                'width': 100,
                'height': 100,
                'scale': 2
            }
    posicao_mapa.allow_tags = True
    posicao_mapa.short_description = _(u"Posição no mapa")


    def id_venda(object, instance):
        
        return "<a href=\"/%s/%s/%s/#info_entrega\">%s</a>" % (instance._meta.app_label, instance.venda._meta.model_name, instance.venda, instance.id,)
    id_venda.allow_tags = True
    id_venda.short_description = _(u"ID")


    def link_venda(object, instance):

        return "<a href=\"/%s/%s/%s/#info_entrega\">%s</a>" % (instance._meta.app_label, instance.venda._meta.model_name, instance.venda, instance.venda,)
    link_venda.allow_tags = True
    link_venda.short_description = _(u"Venda")


    def has_add_permission(self, request, obj=None):
        return False



class EntregaVendaInline(admin.StackedInline):
    form = EntregaVendaForm
    model = EntregaVenda
    suit_classes = 'suit-tab suit-tab-info_entrega'
    fields = ('status', 'endereco', 'data', 'observacao', 'posicao', 'venda')
    list_display = ('endereco', 'cidade', 'data', 'posicao', 'venda',)

    fieldsets = (
                (None, {
                        "fields" : ("status",)
                }),
                ("Detalhes", {
                        #"classes" : ("collapse",),
                        "fields" : ("endereco", "data", 'observacao', 'posicao', 'venda')
                })
    )


class EntregaVendaAddInline(EntregaVendaInline):
    fieldsets = ((None, {
                        "fields" : ("status",)
                }),)



class ItensVendaInline(SalmonellaMixin, admin.TabularInline):
    form = ItensVendaForm
    formset = ItensVendaFormSet
    model = ItensVenda
    # can_delete = False
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total')
    salmonella_fields = ('produto',)
    template = "admin/edit_inline/tabular.html"  # Chama o template personalizado para realizar da inline para fazer todo o tratamento necessário para a tela de vendas


    def get_formset(self, request, obj=None, **kwargs): 
        u""" Altera a quantidade de inlines definida como padrão caso o registro seja salvo no BD """

        if obj: 
            kwargs['extra'] = 0
        else:
            try:
                quantidade = Parametrizacao.objects.get().quantidade_inlines_venda
            except:
                quantidade = 5

            if quantidade:
                kwargs['extra'] = int(quantidade)
            else: 
                kwargs['extra'] = 5

        return super(ItensVendaInline, self).get_formset(request, obj, **kwargs) 


    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da inline como somente leitura caso o registro seja salvo no BD """

        if obj:
            if obj.pedido == 'N' or obj.status or (obj.pedido == 'S' and obj.status_pedido):
                return ['produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total',]
            return []
        else:
            return []



class VendaAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = VendaResource
    form = VendaForm
    model = Venda
    actions = None

    list_display = ('id', 'formata_data_venda', 'cliente', 'forma_pagamento', 'total', 'pedido', 'status_pedido', 'status')
    search_fields = ['id', 'cliente']
    date_hierarchy = 'data_venda'
    list_filter = (('cliente', SelectableFilter), ('data_venda', DateRangeFilter), 'forma_pagamento', 'status', 'pedido', 'status_pedido')
    readonly_fields = ('data_venda', 'vendedor', 'vendedor_associado')
    salmonella_fields = ('cliente', 'forma_pagamento', 'grupo_encargo',)
    
    suit_js_includes = [
            'js/inline_venda.js',
    ]

    data = datetime.datetime.utcnow().replace(tzinfo=utc)

    def get_urls(self):
        urls = super(VendaAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^get_valor_unitario/(?P<id>\d+)/$', self.admin_site.admin_view(get_valor_unitario)),
            (r'^get_endereco_entrega_cliente/(?P<id>\d+)/$', self.admin_site.admin_view(get_endereco_entrega_cliente)),
            (r'^overview/$', self.admin_site.admin_view(overview_vendas)),
            (r'^(\d+)/copia_novo_pedido/$', self.admin_site.admin_view(self.copia_novo_pedido))
        )
        return my_urls + urls


    def copia_novo_pedido(self, request, id):
        if not self.has_add_permission(request):
            raise PermissionDenied

        # Checar se existe quantidade suficiente em estoque. Passar uma lista na mensagem de erro abaixo com os itens insuficientes em estoque.
        quant_itens = list(ItensVenda.objects.filter(vendas__pk=id).values('pk', 'quantidade', 'produto__pk', 'produto__nome', 'produto__quantidade'))
        quant_itens = pd.DataFrame(quant_itens).groupby(['produto__pk', 'produto__nome', 'produto__quantidade'], as_index=False).sum().values.tolist()

        list_p_limite = ""
        for l in quant_itens:
            if l[4] > l[2]:
                list_p_limite += "<li>[" + str(l[0]) + "] " + l[1] + " - Contém " + str(l[2]) + " itens em estoque.</li>"

        if list_p_limite:
            messages.add_message(request, messages.ERROR, format_html(_(u"<b>Erro ao copiar registro como novo pedido.</b><br>Os produtos relacionados abaixo não possuem quantidade de itens suficiente em estoque: <ul>" + list_p_limite + "</ul>")))
            return HttpResponseRedirect('..')

        # Copia a venda
        obj = Venda.objects.get(pk=id)
        novo_pedido = copy.copy(obj)
        novo_pedido.id = None
        novo_pedido.data_venda = None
        novo_pedido.data_cancelamento = None
        novo_pedido.status = False
        novo_pedido.pedido = 'S'
        novo_pedido.status_pedido = False
        novo_pedido.data_pedido = self.data
        novo_pedido.save()

        # Copia os itens de venda
        itens = ItensVenda.objects.filter(vendas__pk=id)
        for i in itens:
            item_obj = ItensVenda.objects.get(pk=str(i))
            novo_item = copy.copy(item_obj)
            novo_item.id = None
            novo_item.vendas = novo_pedido
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
        url = reverse("admin:venda_venda_change", args=[novo_pedido.id])

        return HttpResponseRedirect(url)


    def get_form(self, request, obj=None, **kwargs):
        self.inlines = [ 
            ItensVendaInline,
            #EntregaVendaInline,
        ]

        self.suit_form_tabs = (
            ('geral', _(u"Geral")),
            ('info_adicionais', _(u"Informações adicionais")),
            #('info_entrega', _(u"Informações de Entrega")),
        )
        
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('total', 'desconto', 'status', 'data_cancelamento')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('cliente', 'forma_pagamento', 'grupo_encargo', 'data_venda', 'conta_associada')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-info_adicionais',),
                'fields': ('observacao', 'pedido', 'status_pedido', 'data_pedido', 'vendedor_associado', 'status_apoio')
            }),
        )

        if obj is None:
            self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='status' and x!='data_cancelamento'))
            self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='data_venda' and x!='conta_associada'))
            self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='pedido' and x!='status_pedido' and x!='vendedor' and x!='vendedor_associado'))

        else:
            insert_into_suit_form_tabs = tuple([('info_entrega', _(u"Informações de entrega"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

            sit_entrega = EntregaVenda.objects.filter(venda=obj.pk).exists()
            if sit_entrega:
                self.inlines = self.inlines + [EntregaVendaInline,]
            else:
                self.inlines = self.inlines + [EntregaVendaAddInline,]

            if not obj.status:
                self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='data_cancelamento'))

            if obj.pedido == 'N':
                self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='status_pedido'))

            if obj.pedido == 'S' and not obj.status_pedido:
                self.fieldsets[1][1]['fields'] = tuple(x for x in self.fieldsets[1][1]['fields'] if (x!='data_venda'))

        return super(VendaAdmin, self).get_form(request, obj, **kwargs)


    def has_delete_permission(self, request, obj=None):
        u""" Somente o usuário admin pode deletar uma venda. """
        if request.user.is_superuser:
            return True

        else:
            return False

    
    def get_readonly_fields(self, request, obj=None):
        u""" Define todos os campos da venda como somente leitura caso o registro seja salvo no BD """

        if obj:
            if obj.pedido == 'N' or obj.status or (obj.pedido == 'S' and obj.status_pedido):
                return ['total', 'data_venda', 'data_pedido', 'data_cancelamento', 'desconto', 'cliente', 'forma_pagamento', 'pedido', 'status_pedido', 'grupo_encargo', 'status', 'vendedor', 'vendedor_associado', 'formata_data_venda', 'conta_associada']
            return ['data_venda', 'data_pedido', 'data_cancelamento', 'pedido', 'status_pedido', 'status', 'vendedor', 'vendedor_associado', 'formata_data_venda', 'conta_associada']
        else:
            return ['data_venda', 'data_pedido', 'data_cancelamento', 'pedido', 'status_pedido', 'formata_data_venda', 'conta_associada']


    def response_add(self, request, obj):
        u""" Trata a adição da venda dependendo do botão clicado ao salvá-la 
             Criada em 18/11/2014.
        """

        if '_addpedido' in request.POST:
            obj.pedido = 'S'
            obj.data_pedido = self.data
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            obj.pedido = 'N'
            obj.data_venda = self.data
            obj.save()
            return super(VendaAdmin, self).response_add(request, obj)


    def response_change(self, request, obj):
        u""" Trata a alteração da venda dependendo do botão clicado ao salvá-la 
             Criada em 18/11/2014.
        """

        if '_addconfirmapedido' in request.POST:
            obj.status_pedido = True
            obj.status = False
            obj.data_venda = self.data
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))

        if '_addcancelavenda' in request.POST:
            obj.botao_acionado = '_addcancelavenda'
            obj.data_cancelamento = self.data
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            return super(VendaAdmin, self).response_change(request, obj)


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if obj.status:
            rowclass = 'error'

        return {'class': rowclass}


    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        
        obj.save()


admin.site.register(Venda, VendaAdmin)
admin.site.register(EntregaVenda, EntregaVendaAdmin)