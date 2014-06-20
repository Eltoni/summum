from import_export import resources
from models import Produtos

#classe usada pelo import_export
class ProdutosResource(resources.ModelResource):

    class Meta:
        model = Produtos
        #exclude = ('nome', 'estado')
