#-*- coding: UTF-8 -*-
from django import forms
from suit.widgets import NumberInput, AutosizedTextarea
from movimento.models import Produtos


class ProdutosForm(forms.ModelForm):

    class Meta(object):
        model = Produtos
        exclude = []
        widgets = {
            'preco': NumberInput(
                attrs={ 'class': 'input-small text-right', 
                        'placeholder': '0,00', 
                        'step': '0.01',
                        'min': '0.01',
            }),
            'preco_venda': NumberInput(
                attrs={ 'class': 'input-small text-right', 
                        'placeholder': '0,00', 
                        'step': '0.01',
                        'min': '0.01',
            }),
            'descricao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
        }