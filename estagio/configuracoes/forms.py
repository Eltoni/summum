#-*- coding: UTF-8 -*-
from django.forms import ModelForm, ModelChoiceField, ChoiceField
from suit.widgets import NumberInput
from configuracoes.models import *
from suit_redactor.widgets import RedactorWidget
from schedule.models import Calendar


class ParametrizacaoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParametrizacaoForm, self).__init__(*args, **kwargs)
        self.fields['evento_calendario'] = ChoiceField(choices=[ (o[0], o[1]) for o in Calendar.objects.values_list('slug', 'name') ])

    class Media:
        js = (
            '/static/js/suit_redactor/pt_br.js',
        )

    class Meta:
        widgets = {
            'perc_valor_minimo_recebimento': NumberInput(attrs={'placeholder': '0%'}),
            'email_abertura_caixa': RedactorWidget(editor_options={
                'lang': 'pt_br',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic']
            }),
        }

