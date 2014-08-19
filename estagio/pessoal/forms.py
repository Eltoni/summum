#-*- coding: UTF-8 -*-
from models import *
from django import forms
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from localflavor.br.forms import BRStateChoiceField, BRPhoneNumberField, BRCPFField, BRZipCodeField, BRCNPJField
from django.forms import ModelForm, TextInput
from django.utils.safestring import mark_safe
# from django.forms.widgets import HiddenInput
from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput, BRZipCodeInput, BRCPFInput


class BRPhoneNumberInput(BRPhoneNumberInput):
    mask = {
        'mask': '(99) 9999-99999',
    }



class BaseCadastroPessoaForm(forms.ModelForm):

    class Meta:
        model = BaseCadastroPessoa
        widgets = {
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'numero': TextInput(attrs={'class': 'input-mini'}),
            'nome': TextInput(attrs={'autocomplete':'off'}),     # 'autocomplete':'off' > Desabilita o Auto-complete do campo pelo navegador
            'telefone': BRPhoneNumberInput,
            'celular': BRPhoneNumberInput,
            'cep': BRZipCodeInput,
        }

    def __init__(self, *args, **kwargs):
        super(BaseCadastroPessoaForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['cpf'] = BRCPFField(required=False, label="CPF")
        #self.fields['cep'] = BRZipCodeField(required=False)
        #self.fields['telefone'] = BRPhoneNumberField(required=False)
        #self.fields['celular'] = BRPhoneNumberField(required=False)
        


# Personaliza o widget do RadioButton para ser mostrado horizontalmente
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % unicode(w).replace('<label ', '<label class="radio inline" ') for w in self])+'&#xa0;')



class FornecedorForm(forms.ModelForm):

    class Media:
        # java script personalizado
        js = (
            '/static/js/controle_campos_pf_pj.js',
        )

        # css personalizado
        css = {
            'all': ('/static/css/main.css',)
        }

    class Meta:
        model = Fornecedor

        widgets = {
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'numero': TextInput(attrs={'class': 'input-mini'}),
            'tipo_pessoa': forms.RadioSelect(renderer=HorizontalRadioRenderer),
        }

    def __init__(self, *args, **kwargs):
        super (FornecedorForm, self).__init__(*args,**kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['cpf'] = BRCPFField(required=False, label="CPF")
        self.fields['cnpj'] = BRCNPJField(required=False, label="CNPJ")
        self.fields['razao_social'] = BRCNPJField(required=False, label="Razão Social")
