from django.contrib import admin
from models import *
from forms import *


class FormaPagamentoAdmin(admin.ModelAdmin):

    model = FormaPagamento
    list_display = ('nome', 'quant_parcelas', 'prazo_entre_parcelas', 'status')
    list_filter = ('status',)
    search_fields = ['nome', 'descricao',]

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'descricao', 'quant_parcelas', 'prazo_entre_parcelas', 'tipo_prazo', 'carencia', 'tipo_carencia', 'status')
        }),
    )

    suit_form_tabs = (
        ('geral', 'Geral'),
    )


    def get_readonly_fields(self, request, obj=None):
        """ Define somente alguns campos da forma de pagamento como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['quant_parcelas', 'prazo_entre_parcelas', 'tipo_prazo', 'carencia', 'tipo_carencia',]
        else:
            return []


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if not obj.status:
            rowclass = 'error'

        return {'class': rowclass}



class GrupoEncargoAdmin(admin.ModelAdmin):

    model = GrupoEncargo
    form = GrupoEncargoForm
    list_display = ('nome', 'multa', 'juros', 'tipo_juros', 'status', 'padrao')
    list_filter = ('status',)
    search_fields = ['nome',]

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'multa', 'juros', 'tipo_juros', 'status', 'padrao')
        }),
    )

    suit_form_tabs = (
        ('geral', 'Geral'),
    )


    def get_readonly_fields(self, request, obj=None):
        """ Define somente alguns campos da forma de pagamento como somente leitura caso o registro seja salvo no BD """

        if obj:
            return ['multa', 'tipo_juros', 'juros',]
        else:
            return []


    def save_model(self, request, obj, form, change):
        if not obj.multa:
            obj.multa = 0
            
        if not obj.juros:
            obj.juros = 0

        obj.save()


    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if not obj.status:
            rowclass = 'error'

        return {'class': rowclass}


admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(GrupoEncargo, GrupoEncargoAdmin)