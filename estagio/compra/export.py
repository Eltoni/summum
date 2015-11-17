#-*- coding: UTF-8 -*-
from import_export import resources
from compra.models import Compra
from decimal import Decimal

#classe usada pelo import_export
class CompraResource(resources.ModelResource):

    class Meta:
        model = Compra
        #exclude = ('nome', 'estado')

    def dehydrate_data_compra(self, compra):
        try:
            return '%s' % (compra.data_compra.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_data_pedido(self, compra):
        try:
            return '%s' % (compra.data_pedido.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_data_cancelamento(self, compra):
        try:
            return '%s' % (compra.data_cancelamento.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_status_pedido(self, compra):
        if compra.status_pedido:
            return 'Sim'
        else:
            return 'Não'

    def dehydrate_fornecedor(self, compra):
        return '%s' % (compra.fornecedor.nome)

    def dehydrate_forma_pagamento(self, compra):
        return '%s' % (compra.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, compra):
        return '%s' % (compra.grupo_encargo.nome)

    def dehydrate_total(self, compra):
        return '%s' % (Decimal(compra.total).quantize(Decimal("0.00")))