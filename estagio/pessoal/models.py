#-*- coding: UTF-8 -*-
from django.db import models
from localidade.models import Cidade
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey 


class BaseCadastroPessoa(models.Model):
    u""" 
    Classe BaseCadastroPessoa. 
    Criada para servir de base para as outras models de cadastros de pessoas no sistema. Todas as outras herdam dessa classe.
    
    Criada em 15/06/2014. 
    Última alteração em 16/06/2014.
    """

    nome = models.CharField(max_length=255)
    data_nasc = models.DateField(blank=True, null=True, verbose_name=u'Data de nascimento')
    ativo = models.BooleanField()
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=15) 
    bairro = models.CharField(max_length=50)
    complemento = models.CharField(max_length=50, blank=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    cidade = ChainedForeignKey(Cidade, chained_field="estado", chained_model_field="estado", show_all=False, auto_choose=True)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=30, blank=True)
    celular = models.CharField(max_length=30, blank=True) 
    email = models.EmailField(max_length=100, blank=True, verbose_name=u'e-mail')
    data = models.DateTimeField(auto_now_add=True, verbose_name=u'Data do cadastro')
    observacao = models.TextField(blank=True, verbose_name=u'observações')

    class Meta:
        abstract = True



class Cliente(BaseCadastroPessoa):
    rg = models.CharField(max_length=20, blank=True, verbose_name=u'RG')
    cpf = models.CharField(max_length=11, unique=True, verbose_name=u'CPF')

    def __unicode__(self):
        return u'%s' % (self.nome)

    # class Meta:
        # verbose_name = u'Meta de polo'
        # verbose_name_plural = "Metas dos polos"
        # unique_together = ("polo", "periodo_metas")



class Fornecedor(BaseCadastroPessoa):
    TIPO_PESSOA_CHOICES = (
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    )
    tipo_pessoa = models.CharField(choices=TIPO_PESSOA_CHOICES, max_length=2, blank=False, null=False, default='PF')
    cpf = models.CharField(max_length=11, unique=True, verbose_name=u'CPF')
    cnpj = models.CharField(max_length=14) 
    razao_social = models.CharField(max_length=255, blank=True) 

    class Meta:
        verbose_name = u'Fornecedor'
        verbose_name_plural = "Fornecedores"

    def __unicode__(self):
        return u'%s' % (self.nome)



class Cargo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = u'Cargo'
        verbose_name_plural = "Cargos"

    def __unicode__(self):
        return u'%s' % (self.nome)



class Funcionario(BaseCadastroPessoa):
    rg = models.CharField(max_length=20, blank=True, verbose_name=u'RG')
    cpf = models.CharField(max_length=11, unique=True, verbose_name=u'CPF')
    salario = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True) 
    cargo = models.ForeignKey(Cargo)
    usuario = models.ForeignKey(User, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = u'Funcionário'
        verbose_name_plural = "Funcionários"

    def __unicode__(self):
        return u'%s' % (self.nome)
