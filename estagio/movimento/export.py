#-*- coding: UTF-8 -*-
from import_export import resources
from decimal import Decimal
from movimento.models import Produtos

#classe usada pelo import_export
class ProdutosResource(resources.ModelResource):

    class Meta(object):
        model = Produtos
        #exclude = ('nome', 'estado')

    def dehydrate_preco(self, produtos):
        return '%s' % (Decimal(produtos.preco).quantize(Decimal("0.00")))

    def dehydrate_preco_venda(self, produtos):
        return '%s' % (Decimal(produtos.preco_venda).quantize(Decimal("0.00")))