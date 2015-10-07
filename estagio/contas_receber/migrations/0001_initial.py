# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor total')),
                ('status', models.BooleanField(help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', verbose_name='Conta fechada', default=False)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(verbose_name='Cliente', null=True, on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente')),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo')),
                ('vendas', models.ForeignKey(verbose_name='Venda', null=True, on_delete=django.db.models.deletion.PROTECT, to='venda.Venda')),
            ],
            options={
                'verbose_name_plural': 'Contas a Receber',
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
                'verbose_name': 'Conta a Receber',
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(verbose_name='Conta a receber', on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ContasReceber')),
            ],
            options={
                'verbose_name_plural': 'Parcelas de Contas a Receber',
                'permissions': (('pode_exportar_parcelascontasreceber', 'Exportar Parcelas de Contas a Receber'),),
                'verbose_name': 'Parcela de Conta a Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('juros', models.DecimalField(blank=True, max_digits=20, decimal_places=2, verbose_name='Juros', null=True)),
                ('multa', models.DecimalField(blank=True, max_digits=20, decimal_places=2, verbose_name='Multa', null=True)),
                ('desconto', models.DecimalField(blank=True, max_digits=20, decimal_places=2, verbose_name='Desconto', null=True)),
                ('parcelas_contas_receber', models.ForeignKey(verbose_name='Recebimento de parcela', on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ParcelasContasReceber')),
            ],
            options={
                'verbose_name_plural': 'Recebimentos',
                'verbose_name': 'Recebimento',
            },
        ),
    ]
