# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import pessoal.models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0001_initial'),
        ('localidade', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
            options={
                'verbose_name_plural': 'Cargos',
                'verbose_name': 'Cargo',
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(blank=True, max_length=1, null=True, verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado civil', choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, null=True, verbose_name='Estado', max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, null=True, verbose_name='Conta corrente', max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', verbose_name='Foto', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', max_length=2, verbose_name='Tipo de pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')])),
                ('cnpj', models.CharField(unique=True, null=True, verbose_name='CNPJ', max_length=14)),
                ('razao_social', models.CharField(blank=True, null=True, verbose_name='Razão social', max_length=255)),
                ('agencia', models.ForeignKey(blank=True, null=True, to='banco.Agencia')),
                ('banco', models.ForeignKey(blank=True, null=True, to='banco.Banco')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name_plural': 'Clientes',
                'verbose_name': 'Cliente',
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
            },
        ),
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, null=True, verbose_name='Estado', max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(blank=True, max_length=1, null=True, verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado civil', choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, null=True, verbose_name='Estado', max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, null=True, verbose_name='Conta corrente', max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', verbose_name='Foto', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', max_length=2, verbose_name='Tipo de pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')])),
                ('cnpj', models.CharField(unique=True, null=True, verbose_name='CNPJ', max_length=14)),
                ('razao_social', models.CharField(blank=True, null=True, verbose_name='Razão social', max_length=255)),
                ('agencia', models.ForeignKey(blank=True, null=True, to='banco.Agencia')),
                ('banco', models.ForeignKey(blank=True, null=True, to='banco.Banco')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
            ],
            options={
                'verbose_name_plural': 'Fornecedores',
                'verbose_name': 'Fornecedor',
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, null=True, validators=[pessoal.models.valida_data_nascimento], verbose_name='Data de nascimento')),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(blank=True, max_length=1, null=True, verbose_name='Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado civil', choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')])),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, null=True, verbose_name='Estado', max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, null=True, verbose_name='Conta corrente', max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, upload_to='fotos_pessoas', verbose_name='Foto', max_length=255)),
                ('salario', models.DecimalField(blank=True, null=True, max_digits=20, verbose_name='Salário', decimal_places=2)),
                ('agencia', models.ForeignKey(blank=True, null=True, to='banco.Agencia')),
                ('banco', models.ForeignKey(blank=True, null=True, to='banco.Banco')),
                ('cargo', models.ForeignKey(verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cargo')),
                ('cidade', models.ForeignKey(verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade')),
                ('usuario', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'Funcionários',
                'verbose_name': 'Funcionário',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
            },
        ),
    ]
