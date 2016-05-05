#-*- coding: UTF-8 -*-
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from caixa.models import Caixa


class CaixaForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CaixaForm, self).__init__(*args, **kwargs)
        try:
            ultimo_valor_fechamento = Caixa.objects.all().values_list('valor_fechamento').order_by('-data_fechamento')[0][0]
            self.fields['valor_inicial'].initial = ultimo_valor_fechamento
        except KeyError:
            pass

    class Media(object):
        js = (
            '/static/js/formata_caixa.js',
        )