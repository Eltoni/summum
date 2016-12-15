#-*- coding: UTF-8 -*-
from django.forms import ModelForm, ChoiceField
from django.utils.translation import ugettext_lazy as _
from suit.widgets import NumberInput
from suit_redactor.widgets import RedactorWidget
from schedule.models import Calendar


class ParametrizacaoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParametrizacaoForm, self).__init__(*args, **kwargs)
        self.fields['evento_calendario'] = ChoiceField(choices=[ (o[0], o[1]) for o in Calendar.objects.values_list('slug', 'name') ])
        self.fields['evento_calendario'].help_text = _(u"Defina o calendário de eventos que aparecerão no dashboard do sistema.")

    class Media(object):
        js = (
            '/static/js/suit_redactor/pt_br.js',
        )

    class Meta(object):
        widgets = {
            'email_abertura_caixa': RedactorWidget(editor_options={
                'lang': 'pt_br',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic']
                }),
            'periodo_venc_pedido_compra': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'periodo_venc_pedido_venda': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'quantidade_inlines_venda': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'quantidade_inlines_compra': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'intervalo_dias_entrega_venda': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'qtde_minima_produtos_em_estoque': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'perc_valor_minimo_recebimento': NumberInput(
                attrs={ 'class': 'input-medium', 
                        'placeholder': '0%', 
                        'min': '0'
                }),
        }

