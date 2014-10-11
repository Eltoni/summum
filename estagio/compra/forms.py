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



class CompraForm(ModelForm):
    u""" 
    Classe CompraForm. 
    Criada para customizar as propriedades dos campos da model Compra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media:
        js = (
            '/static/js/formata_campos_compra.js',
        )

    class Meta:
        widgets = {
            'total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right desconto', 'placeholder': '0%', 'min': '0', 'max': '100'}),
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'fornecedor': Select(attrs={'required': 'required'}),
            'forma_pagamento': Select(attrs={'required': 'required'}),
            'status': CheckboxInput(attrs={'class': 'status-compra'}),
        }


    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        try:
            self.fields['fornecedor'].queryset = Fornecedor.objects.exclude(ativo=0) 
            self.fields['forma_pagamento'].queryset = FormaPagamento.objects.exclude(status=0) 
        except KeyError:
            pass



class ItensCompraForm(ModelForm):
    u""" 
    Classe ItensCompraForm. 
    Criada para customizar as propriedades dos campos da inline de ItensCompra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media:
        js = (
            '/static/js/formata_campos.js',
            '/static/js/controle_campos_compra.js',
        )

    class Meta:
        widgets = {
            'quantidade': TextInput(attrs={'class': 'input-mini quantidade-ic', 'placeholder': '0'}),
            'produto': Select(attrs={'class': 'input-large'}),
            'valor_unitario': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'step': '0.01'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right desconto', 'placeholder': '0%', 'min': '0', 'max': '100'}),
            'valor_total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right valor-total-ic', 'placeholder': '0,00', 'step': '0.01'}),
        }


    def __init__(self, *args, **kwargs):
        super(ItensCompraForm, self).__init__(*args, **kwargs)
        try:
            self.fields['produto'].queryset = Produtos.objects.exclude(status=0) 
        except KeyError:
            pass