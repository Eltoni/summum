# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('compra', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('data', models.DateField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('compras', models.ForeignKey(to='compra.Compra', null=True, verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedores', models.ForeignKey(to='pessoal.Fornecedor', null=True, verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Conta a Pagar',
                'permissions': (('pode_exportar_contaspagar', 'Exportar Contas a Pagar'),),
                'verbose_name_plural': 'Contas a Pagar',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('juros', models.DecimalField(verbose_name='Juros', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('multa', models.DecimalField(verbose_name='Multa', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('desconto', models.DecimalField(verbose_name='Desconto', null=True, decimal_places=2, max_digits=20, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(to='contas_pagar.ContasPagar', verbose_name='Conta à pagar', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Parcela de Conta à Pagar',
                'verbose_name_plural': 'Parcelas de Contas à Pagar',
            },
        ),
        migrations.AddField(
            model_name='pagamento',
            name='parcelas_contas_pagar',
            field=models.ForeignKey(to='contas_pagar.ParcelasContasPagar', verbose_name='Pagamento de parcela', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
