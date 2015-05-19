#-*- coding: UTF-8 -*-
from django.forms import ModelForm, TextInput, CheckboxInput
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from django.forms import forms
from django.forms.models import BaseInlineFormSet
from models import *
from django.utils.translation import ugettext_lazy as _


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
            '/static/js/formata_campos_venda_entrega.js',
        )

    class Meta:
        widgets = {
            'total': NumberInput(attrs={'readonly':'readonly', 'class': 'input-small text-right', 'placeholder': '0,00'}),
            'desconto': NumberInput(
                attrs={ 'class': 'input-small text-right desconto', 
                        'placeholder': '0%', 
                        'min': '0', 
                        'max': '100', 
                        'title': 'Informe porcentagem entre 0% e 100%.', 
                        'oninvalid': "this.setCustomValidity('Desconto inválido.')", 
                        'oninput': "this.setCustomValidity('')"
                }),
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'status': CheckboxInput(attrs={'class': 'status-venda'}),
        }

    def clean_desconto(self):
        return self.cleaned_data['desconto'] or 0


    def __init__(self, *args, **kwargs):
        super(VendaForm, self).__init__(*args, **kwargs)

        try:
            grupo_encargo_padrao = GrupoEncargo.objects.get(padrao=1)
            self.fields['grupo_encargo'].initial = grupo_encargo_padrao.pk
        except GrupoEncargo.DoesNotExist and KeyError:
            pass

            

class ItensVendaForm(ModelForm):
    u""" 
    Classe ItensVendaForm. 
    Criada para customizar as propriedades dos campos da inline de ItensVenda
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media:
        css = {
            'all': ('/static/css/itens_venda.css',)
        }

    class Meta:
        widgets = {
            'quantidade': NumberInput(
                attrs={ 'readonly':'readonly', 
                        'class': 'input-mini quantidade-ic', 
                        'placeholder': '0', 
                        'min': '0'
                }),
            'valor_unitario': NumberInput(
                attrs={ 'readonly':'readonly', 
                        'class': 'input-small text-right valor-unitario-ic', 
                        'step': '0.01'
                }),
            'desconto': NumberInput(
                attrs={ 'readonly':'readonly', 
                        'class': 'input-small text-right desconto', 
                        'placeholder': '0%', 
                        'min': '0', 
                        'max': '100', 
                        'title': 'Informe porcentagem entre 0% e 100%.', 
                        'oninvalid': "this.setCustomValidity('Desconto inválido.')", 
                        'oninput': "this.setCustomValidity('')"
                }),
            'valor_total': NumberInput(
                attrs={ 'readonly':'readonly', 
                        'class': 'input-small text-right valor-total-ic', 
                        'placeholder': '0,00', 
                        'step': '0.01'
                }),
        }

    def clean_desconto(self):
        return self.cleaned_data['desconto'] or 0



class ItensVendaFormSet(BaseInlineFormSet):

    def clean(self):
        """Verifica se pelo menos um item de venda foi inserido."""
        super(ItensVendaFormSet, self).clean()
        if any(self.errors):
            return

        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(_(u"Pelo menos um item de venda deve ser cadastrado."))



class EntregaVendaForm(ModelForm):

    class Meta:
        widgets = {
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'endereco': LinkedSelect(attrs={'class': 'input-xxlarge endereco-entrega-field'}),
        }

    def __init__(self, *args, **kwargs):
        super(EntregaVendaForm, self).__init__(*args, **kwargs)
        
        if self.instance.pk:
            entrega_venda = EntregaVenda.objects.filter(pk=self.instance.pk).values_list('venda__cliente__pk')
        try:
            self.fields['endereco'].queryset = EnderecoEntregaCliente.objects.filter(cliente=entrega_venda)
        except:
            pass