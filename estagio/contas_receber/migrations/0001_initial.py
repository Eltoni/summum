# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('venda', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateField(verbose_name='Data')),
                ('valor_total', models.DecimalField(verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, help_text='Se desmarcado, indica que h\xe1 parcelas em aberto, caso contr\xe1rio, a conta foi fechada.', verbose_name='Conta fechada')),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente', null=True)),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
                ('vendas', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda', to='venda.Venda', null=True)),
            ],
            options={
                'verbose_name': 'Conta a Receber',
                'verbose_name_plural': 'Contas a Receber',
                'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),),
            },
        ),
        migrations.CreateModel(
            name='ParcelasContasReceber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vencimento', models.DateField(verbose_name='Vencimento')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('status', models.BooleanField(default=False, verbose_name='Status')),
                ('num_parcelas', models.IntegerField(verbose_name='N\xba Parcela')),
                ('contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Conta \xe0 receber', to='contas_receber.ContasReceber')),
            ],
            options={
                'verbose_name': 'Parcela de Conta \xe0 Receber',
                'verbose_name_plural': 'Parcelas de Contas \xe0 Receber',
            },
        ),
        migrations.CreateModel(
            name='Recebimento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data')),
                ('valor', models.DecimalField(verbose_name='Valor', max_digits=20, decimal_places=2)),
                ('juros', models.DecimalField(null=True, verbose_name='Juros', max_digits=20, decimal_places=2, blank=True)),
                ('multa', models.DecimalField(null=True, verbose_name='Multa', max_digits=20, decimal_places=2, blank=True)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto', max_digits=20, decimal_places=2, blank=True)),
                ('parcelas_contas_receber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento de parcela', to='contas_receber.ParcelasContasReceber')),
            ],
            options={
                'verbose_name': 'Recebimento',
                'verbose_name_plural': 'Recebimentos',
            },
        ),
    ]
