#-*- coding: UTF-8 -*-
from django.forms import ModelForm, CheckboxInput
from suit.widgets import NumberInput, SuitDateWidget
from django.forms import forms
from contas_pagar.models import *


class ContasPagarForm(ModelForm):
    u""" 
    Classe ContasPagarForm. 
    Criada para customizar as propriedades dos campos da model ContasPagar
    
    Criada em 04/10/2014. 
    """

    def __init__(self, *args, **kwargs):
        super(ContasPagarForm, self).__init__(*args, **kwargs)
        try:
            grupo_encargo_padrao = GrupoEncargo.objects.get(padrao=1)
            self.fields['grupo_encargo'].initial = grupo_encargo_padrao.pk
        except GrupoEncargo.DoesNotExist and KeyError:
            pass

    class Meta:
        widgets = {
            'data': SuitDateWidget,
        }



class PagamentoForm(ModelForm):
    u""" 
    Classe PagamentoForm. 
    Criada para customizar as propriedades dos campos da model Pagamento
    
    Criada em 23/07/2014. 
    Última alteração em --.
    """

    class Meta:
        widgets = {
            'valor': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'juros': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'multa': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'parcelas_contas_pagar': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small'}),
        }



class ParcelasContasPagarForm(ModelForm):

    class Media:
        js = (
            '/static/js/formata_campos_contas_pagar.js',
            '/static/js/formata_parcelas_contas_pagar.js',
        )

    class Meta:
        widgets = {
            'status': CheckboxInput(attrs={'class': 'status-parcela'}),
            'vencimento': SuitDateWidget,
        }