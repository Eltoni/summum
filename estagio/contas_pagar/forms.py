#-*- coding: UTF-8 -*-
from django.forms import ModelForm, CheckboxInput
from django.forms import forms, TextInput
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import AdminSplitDateTime
from suit.widgets import NumberInput, SuitSplitDateTimeWidget, AutosizedTextarea
import pytz

from decimal import Decimal
from datetime import datetime

from contas_pagar.models import *
from parametros_financeiros.models import GrupoEncargo


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
            'data': SuitSplitDateTimeWidget,
            'valor_total': NumberInput(
                attrs={ 'class': 'input-small text-right', 
                        'placeholder': '0,00', 
                        'step': '0.01',
                        'min': '0.01',
            }),
            'descricao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
        }



class PagamentoForm(ModelForm):
    u""" 
    Classe PagamentoForm. 
    Criada para customizar as propriedades dos campos da model Pagamento
    
    Criada em 23/07/2014. 
    Última alteração em --.
    """

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        
        try:
            self.fields['data'].required = False
        except KeyError:
            pass


    class Meta:
        model = Pagamento
        exclude = []
        widgets = {
            'data': AdminSplitDateTime(attrs={'readonly': 'readonly'}),
            'valor': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'juros': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'multa': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'parcelas_contas_pagar': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small'}),
            'observacao': forms.Textarea(attrs={'rows': 1, 'cols': 100}),
        }


    def save(self, commit=True):
        instance = super(PagamentoForm, self).save(commit=False)
        zero = Decimal(0.00).quantize(Decimal("0.00"))

        if 'valor' in self.fields:
            instance.valor = self.cleaned_data['valor'] or zero
            
        if 'juros' in self.fields:
            instance.juros = self.cleaned_data['juros'] or zero

        if 'multa' in self.fields:
            instance.multa = self.cleaned_data['multa'] or zero

        if 'desconto' in self.fields:
            instance.desconto = self.cleaned_data['desconto'] or zero

        if 'data' in self.fields:
            instance.data = self.cleaned_data['data'] or datetime.utcnow().replace(tzinfo=pytz.utc)
            
        if commit:
            instance.save()
        return instance



class ParcelasContasPagarForm(ModelForm):

    class Media:
        js = (
            '/static/js/formata_parcelas_contas_pagar.js',
        )

    class Meta:
        widgets = {
            'status': CheckboxInput(attrs={'class': 'status-parcela'}),
        }