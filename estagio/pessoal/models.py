#-*- coding: UTF-8 -*-
from django.db import models
from localidade.models import Cidade
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey 
from django.core.exceptions import ValidationError
import datetime
from datetime import date
from sorl.thumbnail import ImageField
from django.utils.translation import ugettext_lazy as _


class BaseCadastroPessoa(models.Model):
    u""" 
    Classe BaseCadastroPessoa. 
    Criada para servir de base para as outras models de cadastros de pessoas no sistema. Todas as outras herdam dessa classe.
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    # faz a validação da data de nascimento para que o usuário fique impedido de informar data maior ou igual a hoje, e seja maior de 18 anos
    def valida_data_nascimento(value):
        # verifica se data é menor que hoje
        if value >= datetime.date.today():
            raise ValidationError(_(u"Data de nascimento deve ser menor que hoje!"))
        # verifica se pessoa é maior de 18 anos
        dias_no_ano = 365.2425    
        if int((date.today() - value).days / dias_no_ano) < 18:
            raise ValidationError(_(u"Cliente deve ser maior de 18 anos!"))


    nome = models.CharField(max_length=255, verbose_name=_(u"Nome"))
    data_nasc = models.DateField(validators=[valida_data_nascimento], blank=True, null=True, verbose_name=_(u"Data de nascimento"))
    cpf = models.CharField(max_length=11, null=True, unique=True, verbose_name=_(u"CPF"))
    status = models.BooleanField(default=True, verbose_name=_(u"Status"))
    endereco = models.CharField(max_length=50, verbose_name=_(u"Endereço"))
    numero = models.CharField(max_length=15, verbose_name=_(u"Número")) 
    bairro = models.CharField(max_length=50, verbose_name=_(u"Bairro"))
    complemento = models.CharField(max_length=50, blank=True, verbose_name=_(u"Complemento"))
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name=_(u"Estado"))
    cidade = ChainedForeignKey(Cidade, on_delete=models.PROTECT, chained_field="estado", chained_model_field="estado", show_all=False, auto_choose=True, verbose_name=_(u"Cidade"))
    cep = models.CharField(max_length=9, verbose_name=_(u"CEP"))
    telefone = models.CharField(max_length=30, blank=True, verbose_name=_(u"Telefone"))
    celular = models.CharField(max_length=30, blank=True, verbose_name=_(u"Celular")) 
    email = models.EmailField(max_length=100, blank=True, verbose_name=_(u"E-mail"))
    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"))
    foto = ImageField(upload_to='fotos_pessoas', max_length=255, blank=True, verbose_name=_(u"Foto"))

    class Meta:
        abstract = True



class Cliente(BaseCadastroPessoa):
    rg = models.CharField(max_length=20, blank=True, verbose_name=_(u"RG"))

    def __unicode__(self):
        return u'%s' % (self.nome)


    def status_financeiro(obj):
        u""" 
            Método que checa se determinado cliente tem alguma parcela que esteja em aberto e vencida.
            Caso haja, o cliente é classificado como inadimplente com a empresa.
         """
        from contas_receber.models import ParcelasContasReceber

        hoje = date.today()
        status = ParcelasContasReceber.objects.filter(vencimento__lt=hoje, status=False, contas_receber__cliente=obj.pk).select_related('contas_receber__contasreceber').exists()
        
        if status:
            return '<span style="color: #FF0000;"><b>Inadimplente</b></span>'
        else:
            return '<span style="color: #3E3CBF;"><b>Adimplente</b></span>'

    status_financeiro.allow_tags = True
    status_financeiro.short_description = _(u"Status financeiro")



class Fornecedor(BaseCadastroPessoa):
    TIPO_PESSOA_CHOICES = (
        ('PF', _(u"Pessoa Física")),
        ('PJ', _(u"Pessoa Jurídica")),
    )
    tipo_pessoa = models.CharField(choices=TIPO_PESSOA_CHOICES, max_length=2, blank=False, null=False, default='PF', verbose_name=_(u"Tipo pessoa"))
    cnpj = models.CharField(max_length=14, null=True, unique=True, verbose_name=_(u"CNPJ")) 
    razao_social = models.CharField(max_length=255, blank=True, null=True, verbose_name=_(u"Razão social")) 

    class Meta:
        verbose_name = _(u"Fornecedor")
        verbose_name_plural = _(u"Fornecedores")

    def __unicode__(self):
        return u'%s' % (self.nome)

    def status_financeiro(obj):
        u""" 
            Método que checa se determinado cliente tem alguma parcela que esteja em aberto e vencida.
            Caso haja, o cliente é classificado como inadimplente com a empresa.
         """
        from contas_pagar.models import ParcelasContasPagar

        hoje = date.today()
        status = ParcelasContasPagar.objects.filter(vencimento__lt=hoje, status=False, contas_pagar__fornecedores=obj.pk).select_related('contas_pagar__contaspagar').exists()
        
        if status:
            return '<span style="color: #FF0000;"><b>Inadimplente</b></span>'
        else:
            return '<span style="color: #3E3CBF;"><b>Adimplente</b></span>'

    status_financeiro.allow_tags = True
    status_financeiro.short_description = _(u"Status financeiro")



class Cargo(models.Model):
    nome = models.CharField(max_length=100, verbose_name=_(u"Nome"))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição"))

    class Meta:
        verbose_name = _(u"Cargo")
        verbose_name_plural = _(u"Cargos")

    def __unicode__(self):
        return u'%s' % (self.nome)



class Funcionario(BaseCadastroPessoa):
    rg = models.CharField(max_length=20, blank=True, verbose_name=_(u"RG"))
    salario = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Salário")) 
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, verbose_name=_(u"Cargo"))
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, unique=True, verbose_name=_(u"Usuário"))

    class Meta:
        verbose_name = _(u"Funcionário")
        verbose_name_plural = _(u"Funcionários")

    def __unicode__(self):
        return u'%s' % (self.nome)
