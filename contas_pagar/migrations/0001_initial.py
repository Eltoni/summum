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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Valor total', max_digits=20)),
                ('status', models.BooleanField(verbose_name='Conta fechada', db_index=True, help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', default=False)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('compras', models.ForeignKey(to='compra.Compra', verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT, null=True)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedores', models.ForeignKey(to='pessoal.Fornecedor', verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT, null=True)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data do pagamento')),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('juros', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Juros', blank=True, null=True)),
                ('multa', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Multa', blank=True, null=True)),
                ('desconto', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Desconto', blank=True, null=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('vencimento', models.DateField(db_index=True, verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(to='contas_pagar.ContasPagar', verbose_name='Conta a pagar', on_delete=django.db.models.deletion.PROTECT)),
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
            field=models.ForeignKey(to='contas_pagar.ParcelasContasPagar', verbose_name='Pagamento de parcela', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
