from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.decorators import login_required
from movimento.models import Marca, Categoria

@login_required
class CategoriasLookup(ModelLookup):
    form_class_selectable = 'selectable.AutoComboboxSelectWidget'
    field_related_name = 'nome'
    model = Categoria
    search_fields = ('pk__icontains', 'nome__icontains',)

    def format_item(self, item):
        return {
            'id': item.pk,
            'value': item.nome,
            'label': item.nome
        }


@login_required
class MarcaLookup(ModelLookup):
    form_class_selectable = 'selectable.AutoComboboxSelectWidget'
    field_related_name = 'nome'
    model = Marca
    search_fields = ('pk__icontains', 'nome__icontains',)

    def format_item(self, item):
        return {
            'id': item.pk,
            'value': item.nome,
            'label': item.nome
        }


registry.register(CategoriasLookup)
registry.register(MarcaLookup)