#-*- coding: UTF-8 -*-
from django.forms import ModelForm
from suit.widgets import NumberInput


class GrupoEncargoForm(ModelForm):

    class Meta(object):
        widgets = {
            'juros': NumberInput(
                attrs={ 'placeholder': '0%', 
                        'min': '0',
                        'max': '100',
                        'step': '0.0001'
                }),
            'multa': NumberInput(
                attrs={ 'placeholder': '0%', 
                        'min': '0',
                        'max': '100',
                        'step': '0.0001'
                }),
        }