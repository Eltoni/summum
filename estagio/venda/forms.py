#-*- coding: UTF-8 -*-
from django.forms import ModelForm, TextInput, CheckboxInput, HiddenInput, CharField
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea, SuitSplitDateTimeWidget
from django.forms import forms
from django.forms.models import BaseInlineFormSet
from venda.models import *
from django.utils.translation import ugettext_lazy as _
import pandas as pd


class VendaForm(ModelForm):
    u""" 
    Classe VendaForm. 
    Criada para customizar as propriedades dos campos da model Venda
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """
    status_apoio = CharField(widget=HiddenInput(attrs={'class' : 'hidden-form-row'}), required=False)

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

        if self.instance.pedido == 'N' or self.instance.status or (self.instance.pedido == 'S' and self.instance.status_pedido):
            self.fields['status_apoio'].initial = 1

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

    def __init__(self, *args, **kwargs):
        super(ItensVendaFormSet, self).__init__(*args, **kwargs)

        # checa se deve ser habilitado a possibilidade de deletar uma inline
        if not self.instance.pk or self.instance.pedido == 'N' or self.instance.status or (self.instance.pedido == 'S' and self.instance.status_pedido):
            self.can_delete = False


    def clean(self):

        # Condição para validar os itens de compra somente se o objeto não existir, ou se este for um pedido ainda não confirmado, ou registro não está cancelado
        # print(self.instance.pk and (self.instance.status or self.instance.pedido == 'N' or (self.instance.pedido == 'S' and self.instance.status_pedido)))
        if self.instance.pk and (self.instance.status or self.instance.pedido == 'N' or (self.instance.pedido == 'S' and self.instance.status_pedido)):
            return

        list_p = []
        for form in self.forms:
            try:
                if form.cleaned_data:
                    delete = form.cleaned_data.get('DELETE')
                    if not delete and not form.instance.remove_estoque:
                        list_p.append((('produto__pk', form.instance.produto.pk), ('produto__nome', form.instance.produto.nome), ('produto__quantidade', form.instance.produto.quantidade), ('quantidade', form.instance.quantidade)))
            except AttributeError:
                pass

        # Checa se quantidades dos itens inseridas no formulário existem em estoque
        if list_p:
            list_p = [ dict(i) for i in list_p ]
            df = pd.DataFrame(list_p).groupby(['produto__pk', 'produto__nome', 'produto__quantidade'], as_index=False).sum().values.tolist()

            list_p = [ x for x in (list((i for i in d if d[3] > d[2])) for d in df) if x ]

        # Retorna mesnagem de erro nas linhas em que os produtos não contém quantidades suficientes em estoque
        if list_p:
            for form in self.forms:
                try:
                    if form.cleaned_data:
                        delete = form.cleaned_data.get('DELETE')
                        if not delete and not form.instance.remove_estoque:
                            if form.instance.produto.pk in [ i[0] for i in list_p ]:
                                form.add_error('quantidade', 'Total de itens em estoque: %s' % [ i[2] for i in list_p if i[0] == form.instance.produto.pk ][0])
                except AttributeError:
                    pass

            raise forms.ValidationError(_(u"Quantidade de produtos informada ultrapassa limite de unidades em estoque."))


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
            'data': SuitSplitDateTimeWidget,
        }

    def __init__(self, *args, **kwargs):
        super(EntregaVendaForm, self).__init__(*args, **kwargs)
        
        if self.instance.pk:
            entrega_venda = EntregaVenda.objects.filter(pk=self.instance.pk).values_list('venda__cliente__pk')
        try:
            self.fields['endereco'].queryset = EnderecoEntregaCliente.objects.filter(cliente=entrega_venda)
        except:
            pass