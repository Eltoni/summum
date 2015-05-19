#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *
from django.http import HttpResponseRedirect
from configuracoes.models import Parametrizacao
from salmonella.admin import SalmonellaMixin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from export import VendaResource, EntregaVendaResource
from daterange_filter.filter import DateRangeFilter
from selectable_filter.filter import SelectableFilter


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
    can_delete = False
    suit_classes = 'suit-tab suit-tab-geral'
    fields = ('produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total')
    salmonella_fields = ('produto',)
    template = "admin/venda/edit_inline/tabular.html"  # Chama o template personalizado para realizar da inline para fazer todo o tratamento necessário para a tela de vendas


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
            return ['produto', 'quantidade', 'valor_unitario', 'desconto', 'valor_total',]
        else:
            return []



class VendaAdmin(ExportMixin, SalmonellaMixin, admin.ModelAdmin):
    resource_class = VendaResource
    form = VendaForm
    model = Venda
    actions = None

    list_display = ('id', 'data', 'total', 'status')
    search_fields = ['id', 'cliente']
    date_hierarchy = 'data'
    list_filter = (('cliente', SelectableFilter), ('data', DateRangeFilter), 'status', 'forma_pagamento')
    readonly_fields = ('data',)
    salmonella_fields = ('cliente', 'forma_pagamento', 'grupo_encargo',)
    

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
                'fields': ('total', 'desconto', 'status')
            }),
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields': ('cliente', 'forma_pagamento', 'grupo_encargo', 'data')
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
            insert_into_suit_form_tabs = tuple([('info_entrega', _(u"Informações de entrega"))])
            self.suit_form_tabs += insert_into_suit_form_tabs

            sit_entrega = EntregaVenda.objects.filter(venda=obj.pk).exists()
            if sit_entrega:
                self.inlines = self.inlines + [EntregaVendaInline,]
            else:
                self.inlines = self.inlines + [EntregaVendaAddInline,]

            if obj.pedido == 'N':
                self.fieldsets[2][1]['fields'] = tuple(x for x in self.fieldsets[2][1]['fields'] if (x!='status_pedido'))

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
            return ['total', 'data', 'desconto', 'cliente', 'forma_pagamento', 'pedido', 'status_pedido', 'grupo_encargo', 'status',]
        else:
            return ['data', 'pedido', 'status_pedido']


    def response_add(self, request, obj):
        u""" Trata a adição da venda dependendo do botão clicado ao salvá-la 
             Criada em 18/11/2014.
        """

        if '_addpedido' in request.POST:
            obj.pedido = 'S'
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            obj.pedido = 'N'
            obj.save()
            return super(VendaAdmin, self).response_add(request, obj)


    def response_change(self, request, obj):
        u""" Trata a alteração da venda dependendo do botão clicado ao salvá-la 
             Criada em 18/11/2014.
        """

        if '_addconfirmapedido' in request.POST:
            obj.status_pedido = True
            obj.status = False
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))

        if '_addcancelavenda' in request.POST:
            obj.botao_acionado = '_addcancelavenda'
            obj.save()
            return HttpResponseRedirect("../%s" % (obj.pk))
        else:
            return super(VendaAdmin, self).response_change(request, obj)


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if obj.status:
            rowclass = 'error'

        return {'class': rowclass}


admin.site.register(Venda, VendaAdmin)
admin.site.register(EntregaVenda, EntregaVendaAdmin)