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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Valor total', max_digits=20)),
                ('status', models.BooleanField(verbose_name='Conta fechada', db_index=True, help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.', default=False)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT, null=True)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendas', models.ForeignKey(to='venda.Venda', verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT, null=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('vencimento', models.DateField(db_index=True, verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=False)),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(to='contas_receber.ContasReceber', verbose_name='Conta a receber', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data do recebimento')),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', max_digits=20)),
                ('juros', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Juros', blank=True, null=True)),
                ('multa', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Multa', blank=True, null=True)),
                ('desconto', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Desconto', blank=True, null=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True)),
                ('parcelas_contas_receber', models.ForeignKey(to='contas_receber.ParcelasContasReceber', verbose_name='Recebimento de parcela', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
