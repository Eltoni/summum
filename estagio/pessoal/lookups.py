from selectable.base import ModelLookup
from selectable.registry import registry
from selectable.decorators import login_required
from localidade.models import Cidade
from banco.models import Agencia, Banco

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
            return results
        return results.none()   # retorna queryset vazia

    # def get_item_label(self, item):
    #     return "%s, %s" % (item.nome, item.estado)



class BancoChainedLookup(ModelLookup):
    model = Banco
    search_fields = ('nome__icontains', 'banco__icontains')

    def get_item_label(self, item):
        return u'%s (%s)' % (item.nome, item.banco)



class AgenciaChainedLookup(ModelLookup):
    model = Agencia
    search_fields = ('nome__icontains', 'agencia__icontains')

    def get_query(self, request, term):
        results = super(AgenciaChainedLookup, self).get_query(request, term)
        banco = request.GET.get('banco', '')
        # print(dir(request.GET))
        # print('body: ', request.GET.setlist)
        if banco:
            results = results.filter(banco=banco)
            return results
        return results.none()

    def get_item_label(self, item):
        return u'%s (%s)' % (item.agencia, item.nome)


registry.register(CidadeLookup)
registry.register(CidadeChainedLookup)
registry.register(BancoChainedLookup)
registry.register(AgenciaChainedLookup)

