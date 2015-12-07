#-*- coding: UTF-8 -*-
from movimento.models import *
from django import forms
from suit.widgets import NumberInput, AutosizedTextarea


class ProdutosForm(forms.ModelForm):

    class Meta:
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