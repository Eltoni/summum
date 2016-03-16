# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data de geração')),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor total')),
                ('status', models.BooleanField(default=False, verbose_name='Conta fechada', help_text='Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('cliente', models.ForeignKey(verbose_name='Cliente', to='pessoal.Cliente', null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendas', models.ForeignKey(verbose_name='Venda', to='venda.Venda', null=True, on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Data de vencimento')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='Nº Parcela')),
                ('contas_receber', models.ForeignKey(verbose_name='Conta a receber', to='contas_receber.ContasReceber', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('data', models.DateTimeField(verbose_name='Data do recebimento')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor')),
                ('juros', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Juros', null=True)),
                ('multa', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Multa', null=True)),
                ('desconto', models.DecimalField(decimal_places=2, blank=True, max_digits=20, verbose_name='Desconto', null=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações')),
                ('parcelas_contas_receber', models.ForeignKey(verbose_name='Recebimento de parcela', to='contas_receber.ParcelasContasReceber', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'Recebimentos',
                'verbose_name': 'Recebimento',
            },
        ),
    ]
