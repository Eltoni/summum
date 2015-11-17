# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Valor total', max_digits=20)),
                ('status', models.BooleanField(help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', verbose_name='Conta fechada', default=False)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo')),
                ('vendas', models.ForeignKey(to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, null=True, verbose_name='Venda')),
            ],
            options={
                'verbose_name_plural': 'Contas a Receber',
                'verbose_name': 'Conta a Receber',
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(to='contas_receber.ContasReceber', on_delete=django.db.models.deletion.PROTECT, verbose_name='Conta a receber')),
            ],
            options={
                'verbose_name_plural': 'Parcelas de Contas a Receber',
                'verbose_name': 'Parcela de Conta a Receber',
                'permissions': (('pode_exportar_parcelascontasreceber', 'Exportar Parcelas de Contas a Receber'),),
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('data', models.DateTimeField(verbose_name='Data do recebimento', auto_now_add=True)),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('juros', models.DecimalField(blank=True, decimal_places=2, verbose_name='Juros', null=True, max_digits=20)),
                ('multa', models.DecimalField(blank=True, decimal_places=2, verbose_name='Multa', null=True, max_digits=20)),
                ('desconto', models.DecimalField(blank=True, decimal_places=2, verbose_name='Desconto', null=True, max_digits=20)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('parcelas_contas_receber', models.ForeignKey(to='contas_receber.ParcelasContasReceber', on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento de parcela')),
            ],
            options={
                'verbose_name_plural': 'Recebimentos',
                'verbose_name': 'Recebimento',
            },
        ),
    ]
