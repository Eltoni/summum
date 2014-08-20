#-*- coding: UTF-8 -*-
from models import *
from django import forms
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea
from localflavor.br.forms import BRStateChoiceField, BRPhoneNumberField, BRCPFField, BRZipCodeField, BRCNPJField
from django.forms import ModelForm, TextInput
from django.utils.safestring import mark_safe


class BaseCadastroPessoaForm(forms.ModelForm):
    u""" 
    Classe BaseCadastroPessoaForm. 
    Criada para aplicar as customizações dos formulários da página administrativa do sistema.
    Serve de base para todas as outras classes da aplicação Pessoal.
    
    Criada em 15/06/2014. 
    Última alteração em 20/08/2014.
    """

    class Meta:
        model = BaseCadastroPessoa
        widgets = {
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'numero': TextInput(attrs={'class': 'input-mini'}),
            # 'nome': TextInput(attrs={'autocomplete':'off'}),     # 'autocomplete':'off' > Desabilita o Auto-complete do campo pelo navegador
        }

    def __init__(self, *args, **kwargs):
        super(BaseCadastroPessoaForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['cpf'] = BRCPFField(required=False, label="CPF")
        self.fields['cep'] = BRZipCodeField(required=False)
        self.fields['telefone'] = BRPhoneNumberField(required=False)
        self.fields['celular'] = BRPhoneNumberField(required=False)

    # Método que permite salvar valores nulos para o campo CPF, já que o mesmo está setado como Unique=True mas não é de preenchimento obrigatório 
    def clean_cpf(self):
        return self.cleaned_data['cpf'] or None
        


# Personaliza o widget do RadioButton para ser mostrado horizontalmente
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % unicode(w).replace('<label ', '<label class="radio inline" ') for w in self])+'&#xa0;')



class FornecedorForm(BaseCadastroPessoaForm):
    u""" 
    Classe FornecedorForm. 
    Subclasse de BaseCadastroPessoaForm
    Criada para aplicar as customizações do formulário do cadastro de fornecedor.
    
    Criada em 15/06/2014. 
    Última alteração em 20/08/2014.
    """

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
            'tipo_pessoa': forms.RadioSelect(renderer=HorizontalRadioRenderer),
        }

    def __init__(self, *args, **kwargs):
        super (FornecedorForm, self).__init__(*args,**kwargs)
        self.fields['cnpj'] = BRCNPJField(required=False, label="CNPJ")
        self.fields['razao_social'] = BRCNPJField(required=False, label="Razão Social")

    # Método que permite salvar valores nulos para o campo CNPJ, já que o mesmo está setado como Unique=True mas não é de preenchimento obrigatório
    def clean_cnpj(self):
        return self.cleaned_data['cnpj'] or None