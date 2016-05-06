#-*- coding: UTF-8 -*-
from django.forms import forms, ModelForm, TextInput, CheckboxInput, HiddenInput, CharField
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea

from compra.models import *


class CompraForm(ModelForm):
    u""" 
    Classe CompraForm. 
    Criada para customizar as propriedades dos campos da model Compra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """
    status_apoio = CharField(widget=HiddenInput(attrs={'class' : 'hidden-form-row'}), required=False)

    class Media(object):
        js = (
            '/static/js/formata_campos_compra.js',
        )

    class Meta(object):
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
            'status': CheckboxInput(attrs={'class': 'status-compra'}),
        }

    def clean_desconto(self):
        return self.cleaned_data['desconto'] or 0


    def __init__(self, *args, **kwargs):
        super(CompraForm, self).__init__(*args, **kwargs)
        
        if self.instance.pedido == 'N' or self.instance.status or (self.instance.pedido == 'S' and self.instance.status_pedido):
            self.fields['status_apoio'].initial = 1

        try:
            grupo_encargo_padrao = GrupoEncargo.objects.get(padrao=1)
            self.fields['grupo_encargo'].initial = grupo_encargo_padrao.pk
        except (GrupoEncargo.DoesNotExist, KeyError) as e:
            pass



class ItensCompraForm(ModelForm):
    u""" 
    Classe ItensCompraForm. 
    Criada para customizar as propriedades dos campos da inline de ItensCompra
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    class Media(object):
        css = {
            'all': ('/static/css/itens_compra.css',)
        }

    class Meta(object):
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

        

class ItensCompraFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ItensCompraFormSet, self).__init__(*args, **kwargs)

        # checa se deve ser habilitado a possibilidade de deletar uma inline
        if not self.instance.pk or self.instance.pedido == 'N' or self.instance.status or (self.instance.pedido == 'S' and self.instance.status_pedido):
            self.can_delete = False


    def clean(self):

        """Verifica se pelo menos um item de compra foi inserido."""
        super(ItensCompraFormSet, self).clean()
        if any(self.errors):
            return

        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(_(u"Pelo menos um item de compra deve ser cadastrado."))