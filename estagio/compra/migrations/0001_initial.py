# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('total', models.DecimalField(help_text='Valor total da compra.', decimal_places=2, verbose_name='Total (R$)', max_digits=20)),
                ('data_compra', models.DateTimeField(null=True, verbose_name='Data da compra')),
                ('data_pedido', models.DateTimeField(null=True, verbose_name='Data do pedido')),
                ('data_cancelamento', models.DateTimeField(null=True, verbose_name='Data do cancelamento')),
                ('desconto', models.DecimalField(blank=True, verbose_name='Desconto (%)', null=True, decimal_places=0, help_text='Desconto sob o valor total da compra.', max_digits=20)),
                ('status', models.BooleanField(help_text='Indica se o status da compra está ativo ou cancelada.', verbose_name='Cancelado?', default=False)),
                ('observacao', models.TextField(blank=True, help_text='Descreva na área as informações relavantes da compra.', verbose_name='Observações')),
                ('pedido', models.CharField(max_length=1, blank=True, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.', verbose_name='Pedido confirmado?', default=False)),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor', to='pessoal.Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(decimal_places=2, verbose_name='Valor unitário (R$)', max_digits=20)),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Total (R$)', max_digits=20)),
                ('desconto', models.DecimalField(null=True, blank=True, decimal_places=0, verbose_name='Desconto (%)', max_digits=20)),
                ('add_estoque', models.BooleanField(verbose_name='Adicionado ao estoque?', default=False)),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra', to='compra.Compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto', to='movimento.Produtos')),
            ],
            options={
                'verbose_name_plural': 'Itens de Compra',
                'verbose_name': 'Item de Compra',
            },
        ),
    ]
