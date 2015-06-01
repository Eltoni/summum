# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('data', models.DateField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', null=True, verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendas', models.ForeignKey(to='venda.Venda', null=True, verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Conta a Receber',
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
                'verbose_name_plural': 'Contas a Receber',
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(to='contas_receber.ContasReceber', verbose_name='Conta à receber', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Parcela de Conta à Receber',
                'verbose_name_plural': 'Parcelas de Contas à Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('valor', models.DecimalField(verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('juros', models.DecimalField(verbose_name='Juros', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('multa', models.DecimalField(verbose_name='Multa', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('desconto', models.DecimalField(verbose_name='Desconto', null=True, decimal_places=2, max_digits=20, blank=True)),
                ('parcelas_contas_receber', models.ForeignKey(to='contas_receber.ParcelasContasReceber', verbose_name='Recebimento de parcela', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
