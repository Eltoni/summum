#-*- coding: UTF-8 -*-
from django.forms import ModelForm, CheckboxInput
from suit.widgets import NumberInput
from django.forms import forms
from models import *


class ContasPagarForm(ModelForm):
    u""" 
    Classe ContasPagarForm. 
    Criada para customizar as propriedades dos campos da model ContasPagar
    
    Criada em 04/10/2014. 
    """

    def __init__(self, *args, **kwargs):
        super(ContasPagarForm, self).__init__(*args, **kwargs)
        try:
            self.fields['fornecedores'].queryset = Fornecedor.objects.exclude(ativo=0) 
            self.fields['forma_pagamento'].queryset = FormaPagamento.objects.exclude(status=0) 
        except KeyError:
            pass



class PagamentoForm(ModelForm):
    u""" 
    Classe PagamentoForm. 
    Criada para customizar as propriedades dos campos da model Pagamento
    
    Criada em 23/07/2014. 
    Última alteração em --.
    """

    class Meta:
        widgets = {
            'valor': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'juros': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
        }



class ParcelasContasPagarForm(ModelForm):

    class Media:
        js = (
            '/static/js/formata_campos_contas_pagar.js',
        )

    class Meta:
        widgets = {
            'status': CheckboxInput(attrs={'class': 'status-parcela'}),
        }