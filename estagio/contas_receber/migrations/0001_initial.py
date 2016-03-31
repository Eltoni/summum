# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', null=True)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo')),
                ('vendas', models.ForeignKey(to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda', null=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(to='contas_receber.ContasReceber', on_delete=django.db.models.deletion.PROTECT, verbose_name='Conta a receber')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data do recebimento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('juros', models.DecimalField(blank=True, max_digits=20, verbose_name='Juros', decimal_places=2, null=True)),
                ('multa', models.DecimalField(blank=True, max_digits=20, verbose_name='Multa', decimal_places=2, null=True)),
                ('desconto', models.DecimalField(blank=True, max_digits=20, verbose_name='Desconto', decimal_places=2, null=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('parcelas_contas_receber', models.ForeignKey(to='contas_receber.ParcelasContasReceber', on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento de parcela')),
            ],
            options={
                'verbose_name_plural': 'Recebimentos',
                'verbose_name': 'Recebimento',
            },
        ),
    ]
