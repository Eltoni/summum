#-*- coding: UTF-8 -*-
from models import *
from django import forms
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
            'numero': TextInput(attrs={'class': 'input-mini'}),
            'nome': TextInput(attrs={'autocomplete':'off'}),     # 'autocomplete':'off' > Desabilita o Auto-complete do campo pelo navegador
            'telefone': BRPhoneNumberInput,
            'celular': BRPhoneNumberInput,
            'cep': BRZipCodeInput,
        }

    def __init__(self, *args, **kwargs):
        super(BaseCadastroPessoaForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        #self.fields['telefone'] = BRPhoneNumberField(required=False)
        #self.fields['celular'] = BRPhoneNumberField(required=False)
        self.fields['cpf'] = BRCPFField(required=False)
        #self.fields['cep'] = BRZipCodeField(required=False)
        


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))



class FornecedorForm(forms.ModelForm):

    class Meta:
        model = Fornecedor

        widgets = {
            'numero': TextInput(attrs={'class': 'input-mini'}),
            'tipo_pessoa': forms.RadioSelect(renderer=HorizontalRadioRenderer),
        }

    def __init__(self, *args, **kwargs):
        super (FornecedorForm, self).__init__(*args,**kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['cnpj'] = BRCNPJField(required=False)
        self.fields['cpf'] = BRCPFField(required=False)

        # if self.fields['cnpj'] is not None:
        #     self.fields['cnpj'].widget = HiddenInput()
        #     self.fields['cnpj'].label = ""
            
        # if self.fields['tipo_pessoa'] != 'PF':
        #     self.fields["cnpj"].widget = HiddenInput()
        #     del self.fields['cnpj', 'razao_social']
        #     self.fields.pop('cnpj')
