#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from forms import *


class PagamentoAdmin(admin.ModelAdmin):
    form = PagamentoForm
    model = Pagamento
    list_display = ('id', 'data', 'valor')



class ContasPagarAdmin(admin.ModelAdmin):
    model = ContasPagar
    list_display = ('id', 'compras', 'data', 'descricao', 'status')



class ParcelasContasPagarAdmin(admin.ModelAdmin):
    model = ParcelasContasPagar
    list_display = ('id', 'contas_pagar', 'vencimento', 'valor', 'num_parcelas')



admin.site.register(ContasPagar, ContasPagarAdmin)
admin.site.register(ParcelasContasPagar, ParcelasContasPagarAdmin)
admin.site.register(Pagamento, PagamentoAdmin)