#-*- coding: UTF-8 -*-
from import_export import resources
from contas_pagar.models import ContasPagar
from decimal import Decimal

#classe usada pelo import_export
class ContasPagarResource(resources.ModelResource):

    class Meta:
        model = ContasPagar
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, contaspagar):
        return '%s' % (contaspagar.data.strftime('%d/%m/%Y'))

    def dehydrate_fornecedores(self, contaspagar):
        return '%s' % (contaspagar.fornecedores.nome)

    def dehydrate_forma_pagamento(self, contaspagar):
        return '%s' % (contaspagar.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, contaspagar):
        return '%s' % (contaspagar.grupo_encargo.nome)

    def dehydrate_valor_total(self, contaspagar):
        return '%s' % (Decimal(contaspagar.valor_total).quantize(Decimal("0.00")))