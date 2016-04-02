from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.decorators import login_required

from pessoal.models import Cliente

@login_required
class ClienteLookup(ModelLookup):
    form_class_selectable = 'selectable.AutoComboboxSelectWidget'
    field_related_name = 'nome'
    model = Cliente
    search_fields = ('pk__icontains', 'nome__icontains',)

    def format_item(self, item):
        return {
            'id': item.pk,
            'value': item.nome,
            'label': item.nome
        }

registry.register(ClienteLookup)