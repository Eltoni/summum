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

registry.register(CidadeLookup)