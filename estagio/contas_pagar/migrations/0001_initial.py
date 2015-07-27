# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('compra', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('data', models.DateField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', default=False)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('compras', models.ForeignKey(null=True, to='compra.Compra', verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedores', models.ForeignKey(null=True, to='pessoal.Fornecedor', verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Juros')),
                ('multa', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Multa')),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Desconto')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(to='contas_pagar.ContasPagar', verbose_name='Conta a pagar', on_delete=django.db.models.deletion.PROTECT)),
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
            field=models.ForeignKey(to='contas_pagar.ParcelasContasPagar', verbose_name='Pagamento de parcela', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
