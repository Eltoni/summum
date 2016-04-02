#-*- coding: UTF-8 -*-
from import_export import resources
from decimal import Decimal

from venda.models import Venda, EntregaVenda

#classe usada pelo import_export
class VendaResource(resources.ModelResource):

    class Meta:
        model = Venda
        #exclude = ('nome', 'estado')

    def dehydrate_data_venda(self, venda):
        try:
            return '%s' % (venda.data_venda.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_data_pedido(self, venda):
        try:
            return '%s' % (venda.data_pedido.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_data_cancelamento(self, venda):
        try:
            return '%s' % (venda.data_cancelamento.strftime('%d/%m/%Y às %H:%M'))
        except:
            pass

    def dehydrate_status_pedido(self, venda):
        if venda.status_pedido:
            return 'Sim'
        else:
            return 'Não'

    def dehydrate_cliente(self, venda):
        return '%s' % (venda.cliente.nome)

    def dehydrate_forma_pagamento(self, venda):
        return '%s' % (venda.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, venda):
        return '%s' % (venda.grupo_encargo.nome)

    def dehydrate_total(self, venda):
        return '%s' % (Decimal(venda.total).quantize(Decimal("0.00")))



class EntregaVendaResource(resources.ModelResource):

    class Meta:
        model = EntregaVenda
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, entregavenda):
        return '%s' % (entregavenda.data.strftime('%d/%m/%Y às %H:%M'))

    def dehydrate_endereco(self, entregavenda):
        return '%s, %s, %s, %s - %s' % (entregavenda.endereco.endereco, entregavenda.endereco.numero, entregavenda.endereco.bairro, entregavenda.endereco.cidade, entregavenda.endereco.estado)
