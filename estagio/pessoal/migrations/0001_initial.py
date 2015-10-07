# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import sorl.thumbnail.fields
import pessoal.models


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Cargos',
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
                'verbose_name': 'Cargo',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', null=True)),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF', null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, max_digits=3, decimal_places=0, verbose_name='Banco', null=True)),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(default='PF', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo pessoa')),
                ('cnpj', models.CharField(max_length=14, unique=True, verbose_name='CNPJ', null=True)),
                ('razao_social', models.CharField(blank=True, max_length=255, verbose_name='Razão social', null=True)),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name_plural': 'Clientes',
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
                'verbose_name': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
                ('cliente', models.ForeignKey(verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente')),
            ],
            options={
                'verbose_name_plural': 'Endereços de Entrega',
                'verbose_name': 'Endereço de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', null=True)),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF', null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, max_digits=3, decimal_places=0, verbose_name='Banco', null=True)),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(default='PF', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo pessoa')),
                ('cnpj', models.CharField(max_length=14, unique=True, verbose_name='CNPJ', null=True)),
                ('razao_social', models.CharField(blank=True, max_length=255, verbose_name='Razão social', null=True)),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name_plural': 'Fornecedores',
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
                'verbose_name': 'Fornecedor',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', null=True)),
                ('cpf', models.CharField(max_length=11, unique=True, verbose_name='CPF', null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, max_digits=3, decimal_places=0, verbose_name='Banco', null=True)),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('salario', models.DecimalField(blank=True, max_digits=20, decimal_places=2, verbose_name='Salário', null=True)),
                ('cargo', models.ForeignKey(verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cargo')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
                ('usuario', models.OneToOneField(verbose_name='Usuário', null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Funcionários',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name': 'Funcionário',
            },
        ),
    ]
