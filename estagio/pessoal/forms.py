#-*- coding: UTF-8 -*-
from pessoal.models import *
from django import forms
from suit.widgets import LinkedSelect, NumberInput, AutosizedTextarea, SuitDateWidget
from localflavor.br.forms import BRStateChoiceField, BRPhoneNumberField, BRCPFField, BRZipCodeField, BRCNPJField
from django.forms import ModelForm, TextInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from pessoal.lookups import CidadeChainedLookup
from selectable.forms import AutoCompleteSelectField, AutoComboboxSelectWidget


class BaseCadastroPessoaForm(forms.ModelForm):
    cidade = AutoCompleteSelectField(
        lookup_class=CidadeChainedLookup,
        label='Cidade',
        required=True,
        widget=AutoComboboxSelectWidget
    )

    class Media:
        js = (
            '/static/js/mascaras_campos.js',
            '/static/js/consulta_cidades.js',
        )
        # css personalizado
        css = {
            'all': ('/static/css/formata_pessoal.css',)
        }
        
    class Meta:
        model = BaseCadastroPessoa
        exclude = []
        
        widgets = {
            'tipo_pessoa': forms.RadioSelect(),
            'sexo': forms.RadioSelect(),
            'data_nasc': SuitDateWidget,
            'observacao': AutosizedTextarea(attrs={'rows': 5, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'numero': TextInput(attrs={'class': 'input-mini'}),
            # 'nome': TextInput(attrs={'autocomplete':'off'}),     # 'autocomplete':'off' > Desabilita o Auto-complete do campo pelo navegador
        }

    def __init__(self, *args, **kwargs):
        super(BaseCadastroPessoaForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['cpf'] = BRCPFField(required=False, label=_(u"CPF"))
        self.fields['cep'] = BRZipCodeField(required=False)
        self.fields['telefone'] = BRPhoneNumberField(required=False)
        self.fields['celular'] = BRPhoneNumberField(required=False)

    # Método que permite salvar valores nulos para o campo CPF, já que o mesmo está setado como Unique=True mas não é de preenchimento obrigatório 
    # Também trata o valor para que seja salvo no banco
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = cpf.replace('.', '')
        cpf = cpf.replace('-', '')
        return cpf or None



class FornecedorForm(BaseCadastroPessoaForm):
    u""" 
    Classe FornecedorForm. 
    Subclasse de BaseCadastroPessoaForm
    Criada para aplicar as customizações do formulário do cadastro de fornecedor.
    
    Criada em 15/06/2014. 
    Última alteração em 20/08/2014.
    """

    class Media:
        js = (
            '/static/js/controle_campos_pf_pj.js',
            '/static/js/formata_campos.js',
            '/static/js/footable.js',
            '/static/js/footable.paginate.js',
        )

    def __init__(self, *args, **kwargs):
        super (FornecedorForm, self).__init__(*args,**kwargs)
        self.fields['cnpj'] = BRCNPJField(required=False, label=_(u"CNPJ"))
        self.fields['razao_social'] = BRCNPJField(required=False, label=_(u"Razão Social"))

    # Método que permite salvar valores nulos para o campo CNPJ, já que o mesmo está setado como Unique=True mas não é de preenchimento obrigatório
    # Também trata o valor para que seja salvo no banco
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        cnpj = cnpj.replace('/', '')
        return cnpj or None



class FuncionarioForm(BaseCadastroPessoaForm):
    u""" 
    Classe FuncionarioForm. 
    Subclasse de BaseCadastroPessoaForm
    Criada para aplicar as customizações do formulário do cadastro de funcionarios.
    
    Criada em 22/08/2014. 
    """

    class Media:
        js = (
            '/static/js/get_dados_usuario.js',
        )



class ClienteForm(BaseCadastroPessoaForm):

    class Media:
        js = (
            '/static/js/controle_campos_pf_pj.js',
            '/static/js/formata_campos.js',
            '/static/js/footable.js',
            '/static/js/footable.paginate.js',
        )

    def __init__(self, *args, **kwargs):
        super (ClienteForm, self).__init__(*args,**kwargs)
        self.fields['cnpj'] = BRCNPJField(required=False, label=_(u"CNPJ"))
        self.fields['razao_social'] = BRCNPJField(required=False, label=_(u"Razão Social"))

    # Método que permite salvar valores nulos para o campo CNPJ, já que o mesmo está setado como Unique=True mas não é de preenchimento obrigatório
    # Também trata o valor para que seja salvo no banco
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj = cnpj.replace('.', '')
        cnpj = cnpj.replace('-', '')
        cnpj = cnpj.replace('/', '')
        return cnpj or None



class EnderecoEntregaClienteForm(forms.ModelForm):
    cidade = AutoCompleteSelectField(
        lookup_class=CidadeChainedLookup,
        label='Cidade',
        required=True,
        widget=AutoComboboxSelectWidget
    )

    class Media:
        js = (
            '/static/js/consulta_cidades.js',
        )

    class Meta:
        model = EnderecoEntregaCliente
        exclude = []
        widgets = {
            'data_nasc': SuitDateWidget,
            'observacao': AutosizedTextarea(attrs={'rows': 1, 'class': 'input-xxlarge', 'placeholder': '...'}),
            'numero': TextInput(attrs={'class': 'input-mini'}),
            # 'nome': TextInput(attrs={'autocomplete':'off'}),     # 'autocomplete':'off' > Desabilita o Auto-complete do campo pelo navegador
        }


    def __init__(self, *args, **kwargs):
        super(EnderecoEntregaClienteForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")
        self.fields['estado'].widget.attrs['class'] = 'campo-estado'
        self.fields['cpf'] = BRCPFField(required=False, label=_(u"CPF"))
        self.fields['cep'] = BRZipCodeField(required=False)