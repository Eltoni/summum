#-*- coding: UTF-8 -*-
from parametros_financeiros.models import *
from django import forms
from suit.widgets import NumberInput
from django.forms import ModelForm


class GrupoEncargoForm(ModelForm):

    class Meta:
        widgets = {
            'juros': NumberInput(
                attrs={ 'placeholder': '0%', 
                        'min': '0'
                }),
            'multa': NumberInput(
                attrs={ 'placeholder': '0%', 
                        'min': '0'
                }),
        }