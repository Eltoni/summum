#-*- coding: UTF-8 -*-
from django.forms import ModelForm, TextInput, CheckboxInput
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from django.forms import forms
from models import *


class Select(LinkedSelect):
    u"""
    Sobrescrita classe LinkedSelect do django suit
    """

    def __init__(self, attrs=None, choices=()):
        super(LinkedSelect, self).__init__(attrs, choices)



class VendaForm(ModelForm):
    u""" 
    Classe VendaForm. 
    Criada para customizar as propriedades dos campos da model Venda
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media:
        js = (
            '/static/js/formata_campos_venda.js',
        )

    class Meta:
        widgets = {
            'total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right desconto', 'placeholder': '0%', 'min': '0', 'max': '100'}),
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'cliente': Select(attrs={'required': 'required'}),
            'forma_pagamento': Select(attrs={'required': 'required'}),
            'status': CheckboxInput(attrs={'class': 'status-venda'}),
        }


    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)
        try:
            self.fields['cliente'].queryset = Cliente.objects.exclude(ativo=0) 
            self.fields['forma_pagamento'].queryset = FormaPagamento.objects.exclude(status=0) 
        except KeyError:
            pass



class ItensVendaForm(ModelForm):
    u""" 
    Classe ItensVendaForm. 
    Criada para customizar as propriedades dos campos da inline de ItensVenda
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media:
        js = (
            '/static/js/formata_campos.js',
            '/static/js/controle_campos_compra.js',
        )
        css = {
            'all': ('/static/css/itens_venda.css',)
        }

    class Meta:
        widgets = {
            'quantidade': NumberInput(attrs={'class': 'input-mini quantidade-ic', 'placeholder': '0', 'min': '0'}),
            'produto': Select(attrs={'class': 'input-large'}),
            'valor_unitario': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'step': '0.01'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right desconto', 'placeholder': '0%', 'min': '0', 'max': '100'}),
            'valor_total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right valor-total-ic', 'placeholder': '0,00', 'step': '0.01'}),
        }


    def __init__(self, *args, **kwargs):
        super(ItensVendaForm, self).__init__(*args, **kwargs)
        try:
            self.fields['produto'].queryset = Produtos.objects.exclude(status=0) 
        except KeyError:
            pass