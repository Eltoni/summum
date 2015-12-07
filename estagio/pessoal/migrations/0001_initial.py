# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pessoal.models
from django.conf import settings
import sorl.thumbnail.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
            options={
                'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),),
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(null=True, verbose_name='Data de nascimento', blank=True, validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(null=True, verbose_name='Estado', blank=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', blank=True, decimal_places=0, max_digits=3)),
                ('agencia', models.CharField(null=True, verbose_name='Agência', blank=True, max_length=7)),
                ('conta_banco', models.CharField(null=True, verbose_name='Conta corrente', blank=True, max_length=15)),
                ('data', models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, upload_to='fotos_pessoas', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', max_length=2)),
                ('cnpj', models.CharField(unique=True, null=True, verbose_name='CNPJ', max_length=14)),
                ('razao_social', models.CharField(null=True, verbose_name='Razão social', blank=True, max_length=255)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
            ],
            options={
                'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),),
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(null=True, verbose_name='Estado', blank=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Endereço de Entrega',
                'verbose_name_plural': 'Endereços de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(null=True, verbose_name='Data de nascimento', blank=True, validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(null=True, verbose_name='Estado', blank=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', blank=True, decimal_places=0, max_digits=3)),
                ('agencia', models.CharField(null=True, verbose_name='Agência', blank=True, max_length=7)),
                ('conta_banco', models.CharField(null=True, verbose_name='Conta corrente', blank=True, max_length=15)),
                ('data', models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, upload_to='fotos_pessoas', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', max_length=2)),
                ('cnpj', models.CharField(unique=True, null=True, verbose_name='CNPJ', max_length=14)),
                ('razao_social', models.CharField(null=True, verbose_name='Razão social', blank=True, max_length=255)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
            ],
            options={
                'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),),
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(null=True, verbose_name='Data de nascimento', blank=True, validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(unique=True, null=True, verbose_name='CPF', max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(null=True, choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(null=True, verbose_name='Estado', blank=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', blank=True, decimal_places=0, max_digits=3)),
                ('agencia', models.CharField(null=True, verbose_name='Agência', blank=True, max_length=7)),
                ('conta_banco', models.CharField(null=True, verbose_name='Conta corrente', blank=True, max_length=15)),
                ('data', models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(verbose_name='Foto', blank=True, upload_to='fotos_pessoas', max_length=255)),
                ('salario', models.DecimalField(null=True, verbose_name='Salário', blank=True, decimal_places=2, max_digits=20)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cargo', verbose_name='Cargo')),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade')),
                ('usuario', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Usuário')),
            ],
            options={
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
    ]
