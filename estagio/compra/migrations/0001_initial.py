# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('total', models.DecimalField(max_digits=20, verbose_name='Total (R$)', decimal_places=2, help_text='Valor total da compra.')),
                ('data_compra', models.DateTimeField(verbose_name='Data da compra', null=True)),
                ('data_pedido', models.DateTimeField(verbose_name='Data do pedido', null=True)),
                ('data_cancelamento', models.DateTimeField(verbose_name='Data do cancelamento', null=True)),
                ('desconto', models.DecimalField(blank=True, verbose_name='Desconto (%)', null=True, help_text='Desconto sob o valor total da compra.', decimal_places=0, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Indica se o status da compra está ativo ou cancelada.')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da compra.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.')),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento')),
                ('fornecedor', models.ForeignKey(to='pessoal.Fornecedor', on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor')),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo')),
            ],
            options={
                'verbose_name_plural': 'Compras',
                'permissions': (('pode_exportar_compra', 'Exportar Compras'),),
                'verbose_name': 'Compra',
            },
        ),
        migrations.CreateModel(
            name='ItensCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', decimal_places=2, max_digits=20)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(blank=True, max_digits=20, verbose_name='Desconto (%)', decimal_places=0, null=True)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(to='compra.Compra', on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra')),
                ('produto', models.ForeignKey(to='movimento.Produtos', on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto')),
            ],
            options={
                'verbose_name_plural': 'Itens de Compra',
                'verbose_name': 'Item de Compra',
            },
        ),
    ]
