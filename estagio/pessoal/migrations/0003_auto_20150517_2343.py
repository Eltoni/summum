# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0002_auto_20150511_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='agencia',
            field=models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='banco',
            field=models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cnpj',
            field=models.CharField(max_length=14, unique=True, null=True, verbose_name='CNPJ'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='conta_banco',
            field=models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')]),
        ),
        migrations.AddField(
            model_name='cliente',
            name='razao_social',
            field=models.CharField(max_length=255, null=True, verbose_name='Raz\xe3o social', blank=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='sexo',
            field=models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')]),
        ),
        migrations.AddField(
            model_name='cliente',
            name='tipo_pessoa',
            field=models.CharField(default=b'PF', max_length=2, verbose_name='Tipo pessoa', choices=[(b'PF', 'Pessoa F\xedsica'), (b'PJ', 'Pessoa Jur\xeddica')]),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='agencia',
            field=models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='banco',
            field=models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='conta_banco',
            field=models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')]),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='rg',
            field=models.CharField(max_length=20, verbose_name='RG', blank=True),
        ),
        migrations.AddField(
            model_name='fornecedor',
            name='sexo',
            field=models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')]),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='agencia',
            field=models.CharField(max_length=7, null=True, verbose_name='Ag\xeancia', blank=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='banco',
            field=models.DecimalField(null=True, verbose_name='Banco', max_digits=3, decimal_places=0, blank=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='conta_banco',
            field=models.CharField(max_length=15, null=True, verbose_name='Conta Corrente', blank=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='estado_civil',
            field=models.CharField(blank=True, max_length=30, verbose_name='Estado Civil', choices=[(b'solteiro', 'Solteiro'), (b'casado', 'Casado'), (b'separado', 'Separado'), (b'viuvo', 'Viuvo'), (b'divorciado', 'Divorciado'), (b'marital', 'Marital'), (b'separado_judicialmente', 'Separado Judicialmente'), (b'separado_concensualmente', 'Separado Concensualmente'), (b'uniao_estavel', 'Uni\xe3o Est\xe1vel')]),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='sexo',
            field=models.CharField(blank=True, max_length=1, verbose_name='Sexo', choices=[(b'M', 'Masculino'), (b'F', 'Feminino')]),
        ),
    ]
