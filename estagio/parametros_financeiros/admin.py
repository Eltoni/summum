from django.contrib import admin
from models import *


class FormaPagamentoAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_export.html'
    export_template_name = 'export.html'

    model = FormaPagamento
    list_display = ('nome', 'quant_parcelas', 'prazo_entre_parcelas')


admin.site.register(FormaPagamento, FormaPagamentoAdmin)