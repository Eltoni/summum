#-*- coding: UTF-8 -*-
from import_export import resources
from models import ContasReceber
from decimal import Decimal

#classe usada pelo import_export
class ContasReceberResource(resources.ModelResource):

    class Meta:
        model = ContasReceber
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, contasreceber):
        return '%s' % (contasreceber.data.strftime('%d/%m/%Y'))

    def dehydrate_cliente(self, contasreceber):
        return '%s' % (contasreceber.cliente.nome)

    def dehydrate_forma_pagamento(self, contasreceber):
        return '%s' % (contasreceber.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, contasreceber):
        return '%s' % (contasreceber.grupo_encargo.nome)

    def dehydrate_valor_total(self, contasreceber):
        return '%s' % (Decimal(contasreceber.valor_total).quantize(Decimal("0.00")))