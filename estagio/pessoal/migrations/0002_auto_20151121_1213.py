# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='conta_banco',
            field=models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta corrente'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado civil'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_pessoa',
            field=models.CharField(verbose_name='Tipo de pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, default='PF'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='conta_banco',
            field=models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta corrente'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado civil'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='tipo_pessoa',
            field=models.CharField(verbose_name='Tipo de pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')], max_length=2, default='PF'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='conta_banco',
            field=models.CharField(blank=True, null=True, max_length=15, verbose_name='Conta corrente'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='estado_civil',
            field=models.CharField(blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')], max_length=30, verbose_name='Estado civil'),
        ),
    ]
