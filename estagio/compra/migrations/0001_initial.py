# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('total', models.DecimalField(verbose_name='Total (R$)', help_text='Valor total da compra.', decimal_places=2, max_digits=20)),
                ('data_compra', models.DateTimeField(null=True, verbose_name='Data da compra')),
                ('data_pedido', models.DateTimeField(null=True, verbose_name='Data do pedido')),
                ('data_cancelamento', models.DateTimeField(null=True, verbose_name='Data do cancelamento')),
                ('desconto', models.DecimalField(null=True, help_text='Desconto sob o valor total da compra.', max_digits=20, verbose_name='Desconto (%)', blank=True, decimal_places=0)),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Indica se o status da compra está ativo ou cancelada.')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da compra.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Fornecedor', verbose_name='Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
            ],
            options={
                'permissions': (('pode_exportar_compra', 'Exportar Compras'),),
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='ItensCompra',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto (%)', blank=True, decimal_places=0, max_digits=20)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compra.Compra', verbose_name='Compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
        ),
    ]
