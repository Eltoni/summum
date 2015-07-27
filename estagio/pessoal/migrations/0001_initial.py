# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import sorl.thumbnail.fields
import django.db.models.deletion
import pessoal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Cargo',
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(verbose_name='CPF', max_length=11, unique=True, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=0, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(verbose_name='Tipo pessoa', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], default='PF')),
                ('cnpj', models.CharField(verbose_name='CNPJ', max_length=14, unique=True, null=True)),
                ('razao_social', models.CharField(blank=True, max_length=255, verbose_name='Razão social', null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Cliente',
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Endereço de Entrega',
                'verbose_name_plural': 'Endereços de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(verbose_name='CPF', max_length=11, unique=True, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=0, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(verbose_name='Tipo pessoa', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], default='PF')),
                ('cnpj', models.CharField(verbose_name='CNPJ', max_length=14, unique=True, null=True)),
                ('razao_social', models.CharField(blank=True, max_length=255, verbose_name='Razão social', null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
                'verbose_name_plural': 'Fornecedores',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(verbose_name='CPF', max_length=11, unique=True, null=True)),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', null=True)),
                ('estado_civil', models.CharField(blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado Civil')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=0, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, max_length=7, verbose_name='Agência', null=True)),
                ('conta_banco', models.CharField(blank=True, max_length=15, verbose_name='Conta Corrente', null=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='fotos_pessoas', verbose_name='Foto')),
                ('salario', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Salário')),
                ('cargo', models.ForeignKey(to='pessoal.Cargo', verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
                ('usuario', models.OneToOneField(blank=True, null=True, verbose_name='Usuário', to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name_plural': 'Funcionários',
            },
        ),
    ]
