# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pessoal.models
import django.db.models.deletion
from django.conf import settings
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', max_length=11, null=True)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(verbose_name='Sexo', null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, blank=True)),
                ('estado_civil', models.CharField(verbose_name='Estado Civil', blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', null=True, max_length=2, blank=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(verbose_name='Banco', null=True, decimal_places=0, max_digits=3, blank=True)),
                ('agencia', models.CharField(verbose_name='Agência', null=True, max_length=7, blank=True)),
                ('conta_banco', models.CharField(verbose_name='Conta Corrente', null=True, max_length=15, blank=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, max_length=255, upload_to='fotos_pessoas')),
                ('tipo_pessoa', models.CharField(default='PF', verbose_name='Tipo pessoa', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')])),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', max_length=14, null=True)),
                ('razao_social', models.CharField(verbose_name='Razão social', null=True, max_length=255, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', null=True, max_length=2, blank=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', max_length=11, null=True)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(verbose_name='Sexo', null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, blank=True)),
                ('estado_civil', models.CharField(verbose_name='Estado Civil', blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', null=True, max_length=2, blank=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(verbose_name='Banco', null=True, decimal_places=0, max_digits=3, blank=True)),
                ('agencia', models.CharField(verbose_name='Agência', null=True, max_length=7, blank=True)),
                ('conta_banco', models.CharField(verbose_name='Conta Corrente', null=True, max_length=15, blank=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, max_length=255, upload_to='fotos_pessoas')),
                ('tipo_pessoa', models.CharField(default='PF', verbose_name='Tipo pessoa', max_length=2, choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')])),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', max_length=14, null=True)),
                ('razao_social', models.CharField(verbose_name='Razão social', null=True, max_length=255, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', max_length=11, null=True)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(verbose_name='Sexo', null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, blank=True)),
                ('estado_civil', models.CharField(verbose_name='Estado Civil', blank=True, max_length=30, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', null=True, max_length=2, blank=True)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(verbose_name='Banco', null=True, decimal_places=0, max_digits=3, blank=True)),
                ('agencia', models.CharField(verbose_name='Agência', null=True, max_length=7, blank=True)),
                ('conta_banco', models.CharField(verbose_name='Conta Corrente', null=True, max_length=15, blank=True)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, max_length=255, upload_to='fotos_pessoas')),
                ('salario', models.DecimalField(verbose_name='Salário', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('cargo', models.ForeignKey(to='pessoal.Cargo', verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
                ('usuario', models.OneToOneField(null=True, verbose_name='Usuário', blank=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name_plural': 'Funcionários',
            },
        ),
    ]
