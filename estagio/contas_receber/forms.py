#-*- coding: UTF-8 -*-
from django.forms import ModelForm, CheckboxInput
from suit.widgets import NumberInput
from django.forms import forms
from models import *


class ContasReceberForm(ModelForm):
    u""" 
    Classe ContasReceberForm. 
    Criada para customizar as propriedades dos campos da model ContasReceber
    
    Criada em 04/10/2014. 
    """

    def __init__(self, *args, **kwargs):
        super(ContasReceberForm, self).__init__(*args, **kwargs)
        try:
            self.fields['cliente'].queryset = Cliente.objects.exclude(ativo=0) 
            self.fields['forma_pagamento'].queryset = FormaPagamento.objects.exclude(status=0) 
        except KeyError:
            pass



class RecebimentoForm(ModelForm):
    u""" 
    Classe RecebimentoForm. 
    Criada para customizar as propriedades dos campos da model Recebimento
    
    Criada em 06/10/2014. 
    Última alteração em --.
    """

    class Meta:
        widgets = {
            'valor': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'juros': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
        }



class ParcelasContasReceberForm(ModelForm):

    class Media:
        js = (
            '/static/js/formata_campos_contas_receber.js',
        )

    class Meta:
        widgets = {
            'status': CheckboxInput(attrs={'class': 'status-parcela'}),
        }