from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.decorators import login_required
from localidade.models import Cidade


class CidadeChainedLookup(ModelLookup):
    model = Cidade
    search_fields = ('nome__icontains', )

    def get_query(self, request, term):
        results = super(CidadeChainedLookup, self).get_query(request, term)
        estado = request.GET.get('estado', '')
        if estado:
            results = results.filter(estado=estado)
        return results

    # def get_item_label(self, item):
    #     return "%s, %s" % (item.nome, item.estado)


registry.register(CidadeChainedLookup)