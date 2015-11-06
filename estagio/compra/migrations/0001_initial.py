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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)', help_text='Valor total da compra.')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da compra')),
                ('desconto', models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=0, verbose_name='Desconto (%)', help_text='Desconto sob o valor total da compra.')),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Indica se o status da compra está ativo ou cancelada.')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da compra.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, max_length=1, verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Fornecedor', verbose_name='Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
            ],
            options={
                'permissions': (('pode_exportar_compra', 'Exportar Compras'),),
                'verbose_name_plural': 'Compras',
                'verbose_name': 'Compra',
            },
        ),
        migrations.CreateModel(
            name='ItensCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor unitário (R$)')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('desconto', models.DecimalField(max_digits=20, null=True, decimal_places=0, verbose_name='Desconto (%)', blank=True)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='compra.Compra', verbose_name='Compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos', verbose_name='Produto')),
            ],
            options={
                'verbose_name_plural': 'Itens de Compra',
                'verbose_name': 'Item de Compra',
            },
        ),
    ]
