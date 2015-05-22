# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import smart_selects.db_fields
import pessoal.models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, null=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(max_length=11, unique=True, null=True, verbose_name='CPF')),
                ('rg', models.CharField(max_length=20, verbose_name='RG', blank=True)),
                ('sexo', models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')])),
                ('endereco', models.CharField(max_length=50, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=50, verbose_name='Complemento', blank=True)),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(max_length=30, verbose_name='Telefone', blank=True)),
                ('celular', models.CharField(max_length=30, verbose_name='Celular', blank=True)),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail', blank=True)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True)),
                ('agencia', models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True)),
                ('conta_banco', models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observa\xe7\xf5es', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to=b'fotos_pessoas', max_length=255, verbose_name='Foto', blank=True)),
                ('tipo_pessoa', models.CharField(default=b'PF', max_length=2, verbose_name='Tipo pessoa', choices=[(b'PF', 'Pessoa F\xedsica'), (b'PJ', 'Pessoa Jur\xeddica')])),
                ('cnpj', models.CharField(max_length=14, unique=True, null=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(max_length=255, null=True, verbose_name='Raz\xe3o social', blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'estado', on_delete=django.db.models.deletion.PROTECT, chained_field=b'estado', verbose_name='Cidade', auto_choose=True, to='localidade.Cidade')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=50, verbose_name='Complemento', blank=True)),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('observacao', models.TextField(verbose_name='Observa\xe7\xf5es', blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'estado', on_delete=django.db.models.deletion.PROTECT, chained_field=b'estado', verbose_name='Cidade', auto_choose=True, to='localidade.Cidade')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente')),
            ],
            options={
                'verbose_name': 'Endere\xe7o de Entrega',
                'verbose_name_plural': 'Endere\xe7os de Entrega',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, null=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(max_length=11, unique=True, null=True, verbose_name='CPF')),
                ('rg', models.CharField(max_length=20, verbose_name='RG', blank=True)),
                ('sexo', models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')])),
                ('endereco', models.CharField(max_length=50, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=50, verbose_name='Complemento', blank=True)),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(max_length=30, verbose_name='Telefone', blank=True)),
                ('celular', models.CharField(max_length=30, verbose_name='Celular', blank=True)),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail', blank=True)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True)),
                ('agencia', models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True)),
                ('conta_banco', models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observa\xe7\xf5es', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to=b'fotos_pessoas', max_length=255, verbose_name='Foto', blank=True)),
                ('tipo_pessoa', models.CharField(default=b'PF', max_length=2, verbose_name='Tipo pessoa', choices=[(b'PF', 'Pessoa F\xedsica'), (b'PJ', 'Pessoa Jur\xeddica')])),
                ('cnpj', models.CharField(max_length=14, unique=True, null=True, verbose_name='CNPJ')),
                ('razao_social', models.CharField(max_length=255, null=True, verbose_name='Raz\xe3o social', blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'estado', on_delete=django.db.models.deletion.PROTECT, chained_field=b'estado', verbose_name='Cidade', auto_choose=True, to='localidade.Cidade')),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('data_nasc', models.DateField(blank=True, null=True, verbose_name='Data de nascimento', validators=[pessoal.models.valida_data_nascimento])),
                ('cpf', models.CharField(max_length=11, unique=True, null=True, verbose_name='CPF')),
                ('rg', models.CharField(max_length=20, verbose_name='RG', blank=True)),
                ('sexo', models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')])),
                ('estado_civil', models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')])),
                ('endereco', models.CharField(max_length=50, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=50, verbose_name='Complemento', blank=True)),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('telefone', models.CharField(max_length=30, verbose_name='Telefone', blank=True)),
                ('celular', models.CharField(max_length=30, verbose_name='Celular', blank=True)),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail', blank=True)),
                ('banco', models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True)),
                ('agencia', models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True)),
                ('conta_banco', models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('observacao', models.TextField(verbose_name='Observa\xe7\xf5es', blank=True)),
                ('foto', sorl.thumbnail.fields.ImageField(upload_to=b'fotos_pessoas', max_length=255, verbose_name='Foto', blank=True)),
                ('salario', models.DecimalField(null=True, verbose_name='Sal\xe1rio', max_digits=20, decimal_places=2, blank=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cargo', to='pessoal.Cargo')),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'estado', on_delete=django.db.models.deletion.PROTECT, chained_field=b'estado', verbose_name='Cidade', auto_choose=True, to='localidade.Cidade')),
                ('usuario', models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio')),
            ],
            options={
                'verbose_name': 'Funcion\xe1rio',
                'verbose_name_plural': 'Funcion\xe1rios',
                'permissions': (('pode_exportar_funcionario', 'Exportar Funcion\xe1rios'),),
            },
        ),
    ]
