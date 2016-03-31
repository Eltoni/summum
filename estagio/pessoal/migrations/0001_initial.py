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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento], null=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, verbose_name='Estado', null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, verbose_name='Conta corrente', null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Foto', upload_to='fotos_pessoas', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', max_length=2)),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', null=True, max_length=14)),
                ('razao_social', models.CharField(blank=True, verbose_name='Razão social', null=True, max_length=255)),
                ('agencia', models.ForeignKey(blank=True, to='banco.Agencia', verbose_name='Agência', null=True)),
                ('banco', models.ForeignKey(blank=True, to='banco.Banco', verbose_name='Banco', null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, verbose_name='Estado', null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('cidade', models.ForeignKey(to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade')),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente')),
            ],
            options={
                'verbose_name_plural': 'Endereços de Entrega',
                'verbose_name': 'Endereço de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento], null=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, verbose_name='Estado', null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, verbose_name='Conta corrente', null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Foto', upload_to='fotos_pessoas', max_length=255)),
                ('tipo_pessoa', models.CharField(default='PF', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', max_length=2)),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', null=True, max_length=14)),
                ('razao_social', models.CharField(blank=True, verbose_name='Razão social', null=True, max_length=255)),
                ('agencia', models.ForeignKey(blank=True, to='banco.Agencia', verbose_name='Agência', null=True)),
                ('banco', models.ForeignKey(blank=True, to='banco.Banco', verbose_name='Banco', null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(blank=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento], null=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(blank=True, verbose_name='RG', max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], blank=True, verbose_name='Sexo', null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], blank=True, verbose_name='Estado civil', max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', max_length=50)),
                ('estado', models.CharField(blank=True, verbose_name='Estado', null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(blank=True, verbose_name='Telefone', max_length=30)),
                ('celular', models.CharField(blank=True, verbose_name='Celular', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='E-mail', max_length=100)),
                ('conta_banco', models.CharField(blank=True, verbose_name='Conta corrente', null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('foto', sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Foto', upload_to='fotos_pessoas', max_length=255)),
                ('salario', models.DecimalField(blank=True, max_digits=20, verbose_name='Salário', decimal_places=2, null=True)),
                ('agencia', models.ForeignKey(blank=True, to='banco.Agencia', verbose_name='Agência', null=True)),
                ('banco', models.ForeignKey(blank=True, to='banco.Banco', verbose_name='Banco', null=True)),
                ('cargo', models.ForeignKey(to='pessoal.Cargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cargo')),
                ('cidade', models.ForeignKey(to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Usuário', null=True)),
            ],
            options={
                'verbose_name_plural': 'Funcionários',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name': 'Funcionário',
            },
        ),
    ]
