#-*- coding: UTF-8 -*-
from django.db import models
from localidade.models import Cidade
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from datetime import date
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

# faz a validação da data de nascimento para que o usuário fique impedido de informar data maior ou igual a hoje, e seja maior de 18 anos
def valida_data_nascimento(value):
    # verifica se data é menor que hoje
    if value >= datetime.date.today():
        raise ValidationError(_(u"Data de nascimento deve ser menor que hoje!"))
    # verifica se pessoa é maior de 18 anos
    dias_no_ano = 365.2425    
    if int((date.today() - value).days / dias_no_ano) < 18:
        raise ValidationError(_(u"Cliente deve ser maior de 18 anos!"))


class BaseCadastroPessoa(models.Model):
    u""" 
    Classe BaseCadastroPessoa. 
    Criada para servir de base para as outras models de cadastros de pessoas no sistema. Todas as outras herdam dessa classe.
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    ESTADO_CIVIL_CHOICES = (
        ('solteiro', _(u"Solteiro")),
        ('casado', _(u"Casado")),
        ('separado', _(u"Separado")),
        ('viuvo', _(u"Viuvo")),
        ('divorciado', _(u"Divorciado")),
        ('marital', _(u"Marital")),
        ('separado_judicialmente', _(u"Separado Judicialmente")),
        ('separado_concensualmente', _(u"Separado Concensualmente")),
        ('uniao_estavel', _(u"União Estável")),
    )
    SEXO_CHOICES = (
        ('M', _(u"Masculino")),
        ('F', _(u"Feminino")),
    )

    nome = models.CharField(max_length=255, verbose_name=_(u"Nome"))
    data_nasc = models.DateField(validators=[valida_data_nascimento], blank=True, null=True, verbose_name=_(u"Data de nascimento"))
    cpf = models.CharField(max_length=11, null=True, unique=True, verbose_name=_(u"CPF"))
    rg = models.CharField(max_length=20, blank=True, verbose_name=_(u"RG"))
    sexo = models.CharField(max_length=1, blank=True, null=True, choices=SEXO_CHOICES, verbose_name=_(u"Sexo")) 
    estado_civil = models.CharField(max_length=30, blank=True, choices=ESTADO_CIVIL_CHOICES, verbose_name=_(u"Estado Civil")) 
    endereco = models.CharField(max_length=50, verbose_name=_(u"Endereço"))
    numero = models.CharField(max_length=15, verbose_name=_(u"Número")) 
    bairro = models.CharField(max_length=50, verbose_name=_(u"Bairro"))
    complemento = models.CharField(max_length=50, blank=True, verbose_name=_(u"Complemento"))
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name=_(u"Estado"))
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, verbose_name=_(u"Cidade"))
    cep = models.CharField(max_length=9, verbose_name=_(u"CEP"))
    telefone = models.CharField(max_length=30, blank=True, verbose_name=_(u"Telefone"))
    celular = models.CharField(max_length=30, blank=True, verbose_name=_(u"Celular")) 
    email = models.EmailField(max_length=100, blank=True, verbose_name=_(u"E-mail"))
    banco = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True, verbose_name=_(u"Banco"))
    agencia = models.CharField(max_length=7, null=True, blank=True, verbose_name=_(u"Agência"))
    conta_banco = models.CharField(max_length=15, null=True, blank=True, verbose_name=_(u"Conta Corrente")) 
    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data do Cadastro"))
    status = models.BooleanField(default=True, verbose_name=_(u"Status"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"))
    foto = ImageField(upload_to='fotos_pessoas', max_length=255, blank=True, verbose_name=_(u"Foto"))

    class Meta:
        abstract = True

    def formata_data_nascimento(obj):
        u""" Retorna a idade baseada na data de nascimento cadastrada para a pessoa """
        
        if obj.data_nasc:
            idade = int((date.today() - obj.data_nasc).days / 365.2425)
            return format_html('<span style="color: #000000;">{0}</span>', '%s anos' % (idade))
        return '-'
    formata_data_nascimento.allow_tags = True
    formata_data_nascimento.short_description = 'Idade'



@python_2_unicode_compatible
class Cliente(BaseCadastroPessoa):
    TIPO_PESSOA_CHOICES = (
        ('PF', _(u"Pessoa Física")),
        ('PJ', _(u"Pessoa Jurídica")),
    )
    tipo_pessoa = models.CharField(choices=TIPO_PESSOA_CHOICES, max_length=2, blank=False, null=False, default='PF', verbose_name=_(u"Tipo de Pessoa"))
    cnpj = models.CharField(max_length=14, null=True, unique=True, verbose_name=_(u"CNPJ")) 
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u"Razão social")) 
    
    class Meta:
        verbose_name = _(u"Cliente")
        verbose_name_plural = _(u"Clientes")
        permissions = ((u"pode_exportar_cliente", _(u"Exportar Clientes")),)

    def __str__(self):
        return u'%s' % (self.nome)


    def status_financeiro(obj):
        u""" 
            Método que checa se determinado cliente tem alguma parcela que esteja em aberto e vencida.
            Caso haja, o cliente é classificado como inadimplente com a empresa.
         """
        from contas_receber.models import ParcelasContasReceber

        hoje = date.today()
        status = ParcelasContasReceber.objects.filter(vencimento__lt=hoje, status=False, contas_receber__cliente=obj.pk).select_related('contas_receber__contasreceber').exists()
        url = reverse('admin:pessoal_cliente_changelist')
        if status:
            return format_html('<a href="{0}detalhes_financeiros/{1}"><span style="color: #FF0000;"><b>{2}</b></span></a>', url, obj.pk, _(u"Inadimplente"))
        else:
            return format_html('<a href="{0}detalhes_financeiros/{1}"><span style="color: #3E3CBF;"><b>{2}</b></span></a>', url, obj.pk, _(u"Adimplente"))

    status_financeiro.allow_tags = True
    status_financeiro.short_description = _(u"Status financeiro")


    def save(self, *args, **kwargs):

        if self.pk:
            super(Cliente, self).save(*args, **kwargs)

        else:
            super(Cliente, self).save(*args, **kwargs)
            endereco_cliente = EnderecoEntregaCliente(status=True, 
                                                      endereco=self.endereco, 
                                                      numero=self.numero,
                                                      bairro=self.bairro, 
                                                      complemento=self.complemento, 
                                                      estado=self.estado, 
                                                      cidade=self.cidade,
                                                      cep=self.cep,
                                                      cliente=self
                                                      )
            endereco_cliente.save()   



@python_2_unicode_compatible
class Fornecedor(BaseCadastroPessoa):
    TIPO_PESSOA_CHOICES = (
        ('PF', _(u"Pessoa Física")),
        ('PJ', _(u"Pessoa Jurídica")),
    )
    tipo_pessoa = models.CharField(choices=TIPO_PESSOA_CHOICES, max_length=2, blank=False, null=False, default='PF', verbose_name=_(u"Tipo de Pessoa"))
    cnpj = models.CharField(max_length=14, null=True, unique=True, verbose_name=_(u"CNPJ")) 
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u"Razão social")) 

    class Meta:
        verbose_name = _(u"Fornecedor")
        verbose_name_plural = _(u"Fornecedores")
        permissions = ((u"pode_exportar_fornecedor", _(u"Exportar Fornecedores")),)

    def __str__(self):
        return u'%s' % (self.nome)

    def status_financeiro(obj):
        u""" 
            Método que checa se determinado cliente tem alguma parcela que esteja em aberto e vencida.
            Caso haja, o cliente é classificado como inadimplente com a empresa.
         """
        from contas_pagar.models import ParcelasContasPagar

        hoje = date.today()
        status = ParcelasContasPagar.objects.filter(vencimento__lt=hoje, status=False, contas_pagar__fornecedores=obj.pk).select_related('contas_pagar__contaspagar').exists()
        url = reverse('admin:pessoal_cliente_changelist')
        if status:
            return format_html('<span style="color: #FF0000;"><b>{0}</b></span>',  _(u"Inadimplente"))
        else:
            return format_html('<span style="color: #3E3CBF;"><b>{0}</b></span>',  _(u"Adimplente"))

    status_financeiro.allow_tags = True
    status_financeiro.short_description = _(u"Status financeiro")



@python_2_unicode_compatible
class Cargo(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name=_(u"Nome"))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição"))

    class Meta:
        verbose_name = _(u"Cargo")
        verbose_name_plural = _(u"Cargos")
        permissions = ((u"pode_exportar_cargo", _(u"Exportar Cargos")),)

    def __str__(self):
        return u'%s' % (self.nome)



@python_2_unicode_compatible
class Funcionario(BaseCadastroPessoa):
    salario = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Salário")) 
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name=_(u"Cargo"))
    usuario = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, unique=True, verbose_name=_(u"Usuário"))

    class Meta:
        verbose_name = _(u"Funcionário")
        verbose_name_plural = _(u"Funcionários")
        permissions = ((u"pode_exportar_funcionario", _(u"Exportar Funcionários")),)

    def __str__(self):
        return u'%s' % (self.nome)



@python_2_unicode_compatible
class EnderecoEntregaCliente(models.Model):
    status = models.BooleanField(default=True, verbose_name=_(u"Status"))
    endereco = models.CharField(max_length=50, verbose_name=_(u"Endereço"))
    numero = models.CharField(max_length=15, verbose_name=_(u"Número")) 
    bairro = models.CharField(max_length=50, verbose_name=_(u"Bairro"))
    complemento = models.CharField(max_length=50, blank=True, verbose_name=_(u"Complemento"))
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name=_(u"Estado"))
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, verbose_name=_(u"Cidade"))
    cep = models.CharField(max_length=9, verbose_name=_(u"CEP"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"))
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, verbose_name=_(u"Cliente"))

    class Meta:
        verbose_name = _(u"Endereço de Entrega")
        verbose_name_plural = _(u"Endereços de Entrega")

    def __str__(self):
        return u'%s, %s, %s, %s - %s' % (self.endereco, self.numero, self.bairro, self.cidade, self.estado)