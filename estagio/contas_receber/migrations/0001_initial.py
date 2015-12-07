# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('cliente', models.ForeignKey(null=True, to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
                ('vendas', models.ForeignKey(null=True, to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda')),
            ],
            options={
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
                'verbose_name': 'Conta a Receber',
                'verbose_name_plural': 'Contas a Receber',
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ContasReceber', verbose_name='Conta a receber')),
            ],
            options={
                'permissions': (('pode_exportar_parcelascontasreceber', 'Exportar Parcelas de Contas a Receber'),),
                'verbose_name': 'Parcela de Conta a Receber',
                'verbose_name_plural': 'Parcelas de Contas a Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data do recebimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(null=True, verbose_name='Juros', blank=True, decimal_places=2, max_digits=20)),
                ('multa', models.DecimalField(null=True, verbose_name='Multa', blank=True, decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto', blank=True, decimal_places=2, max_digits=20)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('parcelas_contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contas_receber.ParcelasContasReceber', verbose_name='Recebimento de parcela')),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
