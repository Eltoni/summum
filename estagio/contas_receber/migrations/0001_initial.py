# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor total')),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(null=True, to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
                ('vendas', models.ForeignKey(null=True, to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda')),
            ],
            options={
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
                'verbose_name_plural': 'Contas a Receber',
                'verbose_name': 'Conta a Receber',
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ContasReceber', verbose_name='Conta a receber')),
            ],
            options={
                'permissions': (('pode_exportar_parcelascontasreceber', 'Exportar Parcelas de Contas a Receber'),),
                'verbose_name_plural': 'Parcelas de Contas a Receber',
                'verbose_name': 'Parcela de Conta a Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data do recebimento')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor')),
                ('juros', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Juros', blank=True)),
                ('multa', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Multa', blank=True)),
                ('desconto', models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name='Desconto', blank=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('parcelas_contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ParcelasContasReceber', verbose_name='Recebimento de parcela')),
            ],
            options={
                'verbose_name_plural': 'Recebimentos',
                'verbose_name': 'Recebimento',
            },
        ),
    ]
