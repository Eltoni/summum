#-*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm
from suit.widgets import NumberInput
from parametros_financeiros.models import *


class GrupoEncargoForm(ModelForm):

    class Meta:
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