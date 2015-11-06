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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor total')),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('compras', models.ForeignKey(null=True, to='compra.Compra', on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('fornecedores', models.ForeignKey(null=True, to='pessoal.Fornecedor', on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
            ],
            options={
                'permissions': (('pode_exportar_contaspagar', 'Exportar Contas a Pagar'),),
                'verbose_name_plural': 'Contas a Pagar',
                'verbose_name': 'Conta a Pagar',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do pagamento')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('juros', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Juros', blank=True)),
                ('multa', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Multa', blank=True)),
                ('desconto', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Desconto', blank=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_pagar.ContasPagar', verbose_name='Conta a pagar')),
            ],
            options={
                'permissions': (('pode_exportar_parcelascontaspagar', 'Exportar Parcelas de Contas a Pagar'),),
                'verbose_name_plural': 'Parcelas de Contas a Pagar',
                'verbose_name': 'Parcela de Conta a Pagar',
            },
        ),
        migrations.AddField(
            model_name='pagamento',
            name='parcelas_contas_pagar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_pagar.ParcelasContasPagar', verbose_name='Pagamento de parcela'),
        ),
    ]
