# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import sorl.thumbnail.fields
import django.db.models.deletion
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
                'verbose_name_plural': 'Cargos',
                'verbose_name': 'Cargo',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', blank=True)),
                ('cpf', models.CharField(null=True, max_length=11, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], null=True, max_length=1, verbose_name='Sexo', blank=True)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(null=True, max_length=2, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(max_digits=3, null=True, decimal_places=0, verbose_name='Banco', blank=True)),
                ('agencia', models.CharField(null=True, max_length=7, verbose_name='Agência', blank=True)),
                ('conta_banco', models.CharField(null=True, max_length=15, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, default='PF', verbose_name='Tipo de Pessoa')),
                ('cnpj', models.CharField(null=True, max_length=14, unique=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(null=True, max_length=255, verbose_name='Razão social', blank=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
            ],
            options={
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
                'verbose_name_plural': 'Clientes',
                'verbose_name': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(null=True, max_length=2, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente', verbose_name='Cliente')),
            ],
            options={
                'verbose_name_plural': 'Endereços de Entrega',
                'verbose_name': 'Endereço de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', blank=True)),
                ('cpf', models.CharField(null=True, max_length=11, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], null=True, max_length=1, verbose_name='Sexo', blank=True)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(null=True, max_length=2, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(max_digits=3, null=True, decimal_places=0, verbose_name='Banco', blank=True)),
                ('agencia', models.CharField(null=True, max_length=7, verbose_name='Agência', blank=True)),
                ('conta_banco', models.CharField(null=True, max_length=15, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, default='PF', verbose_name='Tipo de Pessoa')),
                ('cnpj', models.CharField(null=True, max_length=14, unique=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(null=True, max_length=255, verbose_name='Razão social', blank=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
            ],
            options={
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
                'verbose_name_plural': 'Fornecedores',
                'verbose_name': 'Fornecedor',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento', blank=True)),
                ('cpf', models.CharField(null=True, max_length=11, unique=True, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], null=True, max_length=1, verbose_name='Sexo', blank=True)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(null=True, max_length=2, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(max_digits=3, null=True, decimal_places=0, verbose_name='Banco', blank=True)),
                ('agencia', models.CharField(null=True, max_length=7, verbose_name='Agência', blank=True)),
                ('conta_banco', models.CharField(null=True, max_length=15, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('salario', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Salário', blank=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cargo', verbose_name='Cargo')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
                ('usuario', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Usuário')),
            ],
            options={
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name_plural': 'Funcionários',
                'verbose_name': 'Funcionário',
            },
        ),
    ]
