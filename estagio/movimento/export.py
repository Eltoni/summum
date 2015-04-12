#-*- coding: UTF-8 -*-
from import_export import resources
from models import Produtos
from decimal import Decimal

#classe usada pelo import_export
class ProdutosResource(resources.ModelResource):

    class Meta:
        model = Produtos
        #exclude = ('nome', 'estado')

    def dehydrate_preco(self, produtos):
        return '%s' % (Decimal(produtos.preco).quantize(Decimal("0.00")))

    def dehydrate_preco_venda(self, produtos):
        return '%s' % (Decimal(produtos.preco_venda).quantize(Decimal("0.00")))