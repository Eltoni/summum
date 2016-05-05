#-*- coding: UTF-8 -*-
from django import forms
from django.forms import TextInput
from django.forms.models import BaseInlineFormSet
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from localflavor.br.forms import BRStateChoiceField, BRPhoneNumberField, BRCPFField, BRZipCodeField
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget

from banco.models import Agencia
from banco.lookups import CidadeChainedLookup


class AgenciaForm(forms.ModelForm):
    cidade = AutoCompleteSelectField(
        lookup_class=CidadeChainedLookup,
        label='Cidade',
        required=False,
        widget=AutoComboboxSelectWidget
    )

    class Media(object):
        js = (
            '/static/js/formata_campos_banco.js',
            '/static/js/inline_endereco_banco.js',
        )
        # css personalizado
        css = {
            'all': ('/static/css/formata_banco.css',)
        }
        
    class Meta(object):
        model = Agencia
        exclude = []
        
        widgets = {
            'numero': TextInput(attrs={'class': 'input-mini'}),
            'agencia': TextInput(attrs={'class': 'input-mini'}),
            'nome': TextInput(attrs={'class': 'input-small'}),
            'endereco': TextInput(attrs={'class': 'input-small'}),
            'bairro': TextInput(attrs={'class': 'input-small'}),
        }

    def __init__(self, *args, **kwargs):
        super(AgenciaForm, self).__init__(*args, **kwargs)
        self.fields['cidade'].widget.attrs['class'] = 'input-small campo-cidade'
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['estado'].widget.attrs['class'] = 'input-small campo-estado'
        self.fields['cep'] = BRZipCodeField(required=False)
        self.fields['cep'].widget.attrs['class'] = 'input-mini campo-cep'
        self.fields['contato'] = BRPhoneNumberField(required=False)
        self.fields['contato'].widget.attrs['class'] = 'input-small campo-contato'



class AgenciaFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(AgenciaFormSet, self).__init__(*args, **kwargs)

        # checa se deve ser habilitado a possibilidade de deletar uma inline
        if not self.instance.pk:
            self.can_delete = False