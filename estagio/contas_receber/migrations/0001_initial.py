# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('venda', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('data', models.DateField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', default=False)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(null=True, to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendas', models.ForeignKey(null=True, to='venda.Venda', verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(to='contas_receber.ContasReceber', verbose_name='Conta a receber', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Parcela de Conta a Receber',
                'permissions': (('pode_exportar_parcelascontasreceber', 'Exportar Parcelas de Contas a Receber'),),
                'verbose_name_plural': 'Parcelas de Contas a Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('data', models.DateTimeField(verbose_name='Data', auto_now_add=True)),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Juros')),
                ('multa', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Multa')),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=2, verbose_name='Desconto')),
                ('parcelas_contas_receber', models.ForeignKey(to='contas_receber.ParcelasContasReceber', verbose_name='Recebimento de parcela', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
