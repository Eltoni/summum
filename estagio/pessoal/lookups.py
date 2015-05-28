from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.decorators import login_required
from localidade.models import Cidade

@login_required
class CidadeLookup(ModelLookup):
    form_class_selectable = 'selectable.AutoComboboxSelectWidget'
    field_related_name = 'nome'
    model = Cidade
    search_fields = ('pk__icontains', 'nome__icontains',)

    def format_item(self, item):
        return {
            'id': item.pk,
            'value': item.nome,
            'label': item.nome
        }


class CidadeChainedLookup(ModelLookup):
    model = Cidade
    search_fields = ('nome__icontains', )

    def get_query(self, request, term):
        results = super(CidadeChainedLookup, self).get_query(request, term)
        estado = request.GET.get('estado', '')
        if estado:
            results = results.filter(estado=estado)
            print (results)
        return results

    # def get_item_label(self, item):
    #     return "%s, %s" % (item.nome, item.estado)


registry.register(CidadeChainedLookup)
registry.register(CidadeLookup)