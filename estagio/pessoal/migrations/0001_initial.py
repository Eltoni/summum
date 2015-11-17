# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
from django.conf import settings
import pessoal.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, max_length=11, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('estado_civil', models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, null=True, max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, decimal_places=0, max_digits=3, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, null=True, max_length=7, verbose_name='Agência')),
                ('conta_banco', models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta Corrente')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', max_length=255, verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Pessoa')),
                ('cnpj', models.CharField(unique=True, null=True, max_length=14, verbose_name='CNPJ')),
                ('razao_social', models.CharField(blank=True, null=True, max_length=255, verbose_name='Razão social')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
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
                ('estado', models.CharField(blank=True, null=True, max_length=2, verbose_name='Estado')),
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
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, max_length=11, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('estado_civil', models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, null=True, max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, decimal_places=0, max_digits=3, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, null=True, max_length=7, verbose_name='Agência')),
                ('conta_banco', models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta Corrente')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', max_length=255, verbose_name='Foto')),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, verbose_name='Tipo de Pessoa')),
                ('cnpj', models.CharField(unique=True, null=True, max_length=14, verbose_name='CNPJ')),
                ('razao_social', models.CharField(blank=True, null=True, max_length=255, verbose_name='Razão social')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, max_length=11, verbose_name='CPF')),
                ('rg', models.CharField(blank=True, max_length=20, verbose_name='RG')),
                ('sexo', models.CharField(blank=True, null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Sexo')),
                ('estado_civil', models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado Civil')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=15, verbose_name='Número')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(blank=True, max_length=50, verbose_name='Complemento')),
                ('estado', models.CharField(blank=True, null=True, max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(blank=True, max_length=30, verbose_name='Telefone')),
                ('celular', models.CharField(blank=True, max_length=30, verbose_name='Celular')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('banco', models.DecimalField(blank=True, null=True, decimal_places=0, max_digits=3, verbose_name='Banco')),
                ('agencia', models.CharField(blank=True, null=True, max_length=7, verbose_name='Agência')),
                ('conta_banco', models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta Corrente')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do Cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', max_length=255, verbose_name='Foto')),
                ('salario', models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=20, verbose_name='Salário')),
                ('cargo', models.ForeignKey(verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cargo')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
                ('usuario', models.OneToOneField(null=True, verbose_name='Usuário', blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
            },
        ),
    ]
