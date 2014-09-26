from django.contrib import admin
from models import *


class FormaPagamentoAdmin(admin.ModelAdmin):

    model = FormaPagamento
    list_display = ('nome', 'quant_parcelas', 'prazo_entre_parcelas', 'status')

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'descricao', 'quant_parcelas', 'prazo_entre_parcelas', 'tipo_prazo', 'carencia', 'tipo_carencia', 'observacao', 'status')
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


admin.site.register(FormaPagamento, FormaPagamentoAdmin)