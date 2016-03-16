# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('compra', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor total')),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('compras', models.ForeignKey(verbose_name='Compra', to='compra.Compra', null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedores', models.ForeignKey(verbose_name='Fornecedor', to='pessoal.Fornecedor', null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data do pagamento')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('juros', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Juros', null=True)),
                ('multa', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Multa', null=True)),
                ('desconto', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Desconto', null=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
            ],
        ),
        migrations.CreateModel(
            name='ParcelasContasPagar',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_pagar', models.ForeignKey(verbose_name='Conta a pagar', to='contas_pagar.ContasPagar', on_delete=django.db.models.deletion.PROTECT)),
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
            field=models.ForeignKey(verbose_name='Pagamento de parcela', to='contas_pagar.ParcelasContasPagar', on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
