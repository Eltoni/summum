# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('compras', models.ForeignKey(to='compra.Compra', on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra', null=True)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento')),
                ('fornecedores', models.ForeignKey(to='pessoal.Fornecedor', on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor', null=True)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo')),
            ],
            options={
                'verbose_name_plural': 'Contas a Pagar',
                'permissions': (('pode_exportar_contaspagar', 'Exportar Contas a Pagar'),),
                'verbose_name': 'Conta a Pagar',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data do pagamento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('juros', models.DecimalField(blank=True, max_digits=20, verbose_name='Juros', decimal_places=2, null=True)),
                ('multa', models.DecimalField(blank=True, max_digits=20, verbose_name='Multa', decimal_places=2, null=True)),
                ('desconto', models.DecimalField(blank=True, max_digits=20, verbose_name='Desconto', decimal_places=2, null=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(to='contas_pagar.ContasPagar', on_delete=django.db.models.deletion.PROTECT, verbose_name='Conta a pagar')),
            ],
            options={
                'verbose_name_plural': 'Parcelas de Contas a Pagar',
                'permissions': (('pode_exportar_parcelascontaspagar', 'Exportar Parcelas de Contas a Pagar'),),
                'verbose_name': 'Parcela de Conta a Pagar',
            },
        ),
        migrations.AddField(
            model_name='pagamento',
            name='parcelas_contas_pagar',
            field=models.ForeignKey(to='contas_pagar.ParcelasContasPagar', on_delete=django.db.models.deletion.PROTECT, verbose_name='Pagamento de parcela'),
        ),
    ]
