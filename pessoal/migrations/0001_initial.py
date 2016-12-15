# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pessoal.models
from django.conf import settings
import sorl.thumbnail.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('banco', '0001_initial'),
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', blank=True, null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado civil', blank=True, max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', blank=True, null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('conta_banco', models.CharField(verbose_name='Conta corrente', blank=True, null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to='fotos_pessoas', verbose_name='Foto', blank=True, max_length=255)),
                ('tipo_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', default='PF', max_length=2)),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', null=True, max_length=14)),
                ('razao_social', models.CharField(verbose_name='Razão social', blank=True, null=True, max_length=255)),
                ('agencia', models.ForeignKey(to='banco.Agencia', verbose_name='Agência', blank=True, null=True)),
                ('banco', models.ForeignKey(to='banco.Banco', verbose_name='Banco', blank=True, null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=True)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', blank=True, null=True, max_length=2)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', blank=True, null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado civil', blank=True, max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', blank=True, null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('conta_banco', models.CharField(verbose_name='Conta corrente', blank=True, null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to='fotos_pessoas', verbose_name='Foto', blank=True, max_length=255)),
                ('tipo_pessoa', models.CharField(choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], verbose_name='Tipo de pessoa', default='PF', max_length=2)),
                ('cnpj', models.CharField(unique=True, verbose_name='CNPJ', null=True, max_length=14)),
                ('razao_social', models.CharField(verbose_name='Razão social', blank=True, null=True, max_length=255)),
                ('agencia', models.ForeignKey(to='banco.Agencia', verbose_name='Agência', blank=True, null=True)),
                ('banco', models.ForeignKey(to='banco.Banco', verbose_name='Banco', blank=True, null=True)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('data_nasc', models.DateField(verbose_name='Data de nascimento', null=True, validators=[pessoal.models.valida_data_nascimento], blank=True)),
                ('cpf', models.CharField(unique=True, verbose_name='CPF', null=True, max_length=11)),
                ('rg', models.CharField(verbose_name='RG', blank=True, max_length=20)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], verbose_name='Sexo', blank=True, null=True, max_length=1)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], verbose_name='Estado civil', blank=True, max_length=30)),
                ('endereco', models.CharField(verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(verbose_name='Número', max_length=15)),
                ('bairro', models.CharField(verbose_name='Bairro', max_length=50)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', blank=True, null=True, max_length=2)),
                ('cep', models.CharField(verbose_name='CEP', max_length=9)),
                ('telefone', models.CharField(verbose_name='Telefone', blank=True, max_length=30)),
                ('celular', models.CharField(verbose_name='Celular', blank=True, max_length=30)),
                ('email', models.EmailField(verbose_name='E-mail', blank=True, max_length=100)),
                ('conta_banco', models.CharField(verbose_name='Conta corrente', blank=True, null=True, max_length=15)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to='fotos_pessoas', verbose_name='Foto', blank=True, max_length=255)),
                ('salario', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Salário', blank=True, null=True)),
                ('agencia', models.ForeignKey(to='banco.Agencia', verbose_name='Agência', blank=True, null=True)),
                ('banco', models.ForeignKey(to='banco.Banco', verbose_name='Banco', blank=True, null=True)),
                ('cargo', models.ForeignKey(to='pessoal.Cargo', verbose_name='Cargo', on_delete=django.db.models.deletion.PROTECT)),
                ('cidade', models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete=django.db.models.deletion.PROTECT, null=True, blank=True)),
            ],
            options={
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcionários'),),
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
    ]
