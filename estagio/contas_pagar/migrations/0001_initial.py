# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('compras', models.ForeignKey(null=True, to='compra.Compra', on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('fornecedores', models.ForeignKey(null=True, to='pessoal.Fornecedor', on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
            ],
            options={
                'permissions': (('pode_exportar_contaspagar', 'Exportar Contas a Pagar'),),
                'verbose_name': 'Conta a Pagar',
                'verbose_name_plural': 'Contas a Pagar',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data do pagamento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(null=True, verbose_name='Juros', blank=True, decimal_places=2, max_digits=20)),
                ('multa', models.DecimalField(null=True, verbose_name='Multa', blank=True, decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto', blank=True, decimal_places=2, max_digits=20)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_pagar.ContasPagar', verbose_name='Conta a pagar')),
            ],
            options={
                'permissions': (('pode_exportar_parcelascontaspagar', 'Exportar Parcelas de Contas a Pagar'),),
                'verbose_name': 'Parcela de Conta a Pagar',
                'verbose_name_plural': 'Parcelas de Contas a Pagar',
            },
        ),
        migrations.AddField(
            model_name='pagamento',
            name='parcelas_contas_pagar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_pagar.ParcelasContasPagar', verbose_name='Pagamento de parcela'),
        ),
    ]
