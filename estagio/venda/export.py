#-*- coding: UTF-8 -*-
from import_export import resources
from models import Venda
from decimal import Decimal

#classe usada pelo import_export
class VendaResource(resources.ModelResource):

    class Meta:
        model = Venda
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, venda):
        return '%s' % (venda.data.strftime('%d/%m/%Y'))

    def dehydrate_cliente(self, venda):
        return '%s' % (venda.cliente.nome)

    def dehydrate_forma_pagamento(self, venda):
        return '%s' % (venda.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, venda):
        return '%s' % (venda.grupo_encargo.nome)

    def dehydrate_total(self, venda):
        return '%s' % (Decimal(venda.total).quantize(Decimal("0.00")))