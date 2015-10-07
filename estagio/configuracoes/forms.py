#-*- coding: UTF-8 -*-
from django.forms import ModelForm
from suit.widgets import NumberInput
from configuracoes.models import *
from suit_redactor.widgets import RedactorWidget


class ParametrizacaoForm(ModelForm):

    class Media:
        js = (
            '/static/js/suit_redactor/pt_br.js',
        )

    class Meta:
        widgets = {
            'perc_valor_minimo_pagamento': NumberInput(attrs={'placeholder': '0%'}),
            'email_abertura_caixa': RedactorWidget(editor_options={
                'lang': 'pt_br',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic']
            }),
        }

