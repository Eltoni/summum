#-*- coding: UTF-8 -*-
from django.forms import ModelForm, TextInput
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from django.forms import forms


class FormFields(ModelForm):
    u""" 
    Classe FormFields. 
    Criada para customizar as propriedades dos campos da inline de ItensCompra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Meta:
        widgets = {
            'quantidade': TextInput(attrs={'class': 'input-mini', 'placeholder': '0'}),
            'produto': LinkedSelect(attrs={'class': 'input-large'}),
            'valor_unitario': NumberInput(attrs={'class': 'input-small text-right'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'valor_total': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
        }



class FormFieldsMain(ModelForm):
    u""" 
    Classe FormFieldsMain. 
    Criada para customizar as propriedades dos campos da model Compra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Meta:
        widgets = {
            'total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00'}),
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
        }



class FormPagamento(ModelForm):
    u""" 
    Classe FormPagamento. 
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