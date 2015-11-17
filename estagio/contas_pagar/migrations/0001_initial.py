# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '__first__'),
        ('compra', '__first__'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Conta fechada', default=False, help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra', null=True, to='compra.Compra')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('fornecedores', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor', null=True, to='pessoal.Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data do pagamento', auto_now_add=True)),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(verbose_name='Juros', max_digits=20, decimal_places=2, blank=True, null=True)),
                ('multa', models.DecimalField(verbose_name='Multa', max_digits=20, decimal_places=2, blank=True, null=True)),
                ('desconto', models.DecimalField(verbose_name='Desconto', max_digits=20, decimal_places=2, blank=True, null=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Conta a pagar', to='contas_pagar.ContasPagar')),
            ],
            options={
                'verbose_name': 'Parcela de Conta a Pagar',
                'permissions': (('pode_exportar_parcelascontaspagar', 'Exportar Parcelas de Contas a Pagar'),),
                'verbose_name_plural': 'Parcelas de Contas a Pagar',
            },
        ),
        migrations.AddField(
            model_name='pagamento',
            name='parcelas_contas_pagar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Pagamento de parcela', to='contas_pagar.ParcelasContasPagar'),
        ),
    ]
