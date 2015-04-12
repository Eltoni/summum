#-*- coding: UTF-8 -*-
from import_export import resources
from models import Compra
from decimal import Decimal

#classe usada pelo import_export
class CompraResource(resources.ModelResource):

    class Meta:
        model = Compra
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, compra):
        return '%s' % (compra.data.strftime('%d/%m/%Y'))

    def dehydrate_fornecedor(self, compra):
        return '%s' % (compra.fornecedor.nome)

    def dehydrate_forma_pagamento(self, compra):
        return '%s' % (compra.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, compra):
        return '%s' % (compra.grupo_encargo.nome)

    def dehydrate_total(self, compra):
        return '%s' % (Decimal(compra.total).quantize(Decimal("0.00")))