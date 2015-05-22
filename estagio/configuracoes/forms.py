#-*- coding: UTF-8 -*-
from django.forms import ModelForm
from suit.widgets import NumberInput
from models import *
from suit_redactor.widgets import RedactorWidget


class ParametrizacaoForm(ModelForm):

    class Meta:
        widgets = {
            'perc_valor_minimo_pagamento': NumberInput(attrs={'placeholder': '0%'}),
            #'email_abertura_caixa': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'email_abertura_caixa': RedactorWidget(editor_options={
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic']}),
        }

