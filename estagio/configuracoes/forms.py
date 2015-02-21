#-*- coding: UTF-8 -*-
from django.forms import ModelForm
from suit.widgets import NumberInput
from models import *


class ParametrizacaoForm(ModelForm):

    class Meta:
        widgets = {
            'perc_valor_minimo_pagamento': NumberInput(attrs={'placeholder': '0%'}),
        }

