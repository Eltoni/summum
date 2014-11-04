#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *


class CaixaAdmin(admin.ModelAdmin):
    model = Caixa
    list_display = ('id', 'data', 'valor_fechamento', 'status')



class MovimentosCaixaAdmin(admin.ModelAdmin):
    model = MovimentosCaixa
    list_display = ('id', 'caixa', 'pagamento_associado', 'recebimento_associado', 'tipo_mov', 'valor')
    readonly_fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')
    fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')



admin.site.register(Caixa, CaixaAdmin)
admin.site.register(MovimentosCaixa, MovimentosCaixaAdmin)