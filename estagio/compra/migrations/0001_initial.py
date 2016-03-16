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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('total', models.DecimalField(help_text='Valor total da compra.', max_digits=20, verbose_name='Total (R$)', decimal_places=2)),
                ('data_compra', models.DateTimeField(null=True, verbose_name='Data da compra')),
                ('data_pedido', models.DateTimeField(null=True, verbose_name='Data do pedido')),
                ('data_cancelamento', models.DateTimeField(null=True, verbose_name='Data do cancelamento')),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', null=True, help_text='Desconto sob o valor total da compra.', max_digits=20, blank=True, decimal_places=0)),
                ('status', models.BooleanField(help_text='Indica se o status da compra está ativo ou cancelada.', default=False, verbose_name='Cancelado?')),
                ('observacao', models.TextField(help_text='Descreva na área as informações relavantes da compra.', blank=True, verbose_name='Observações')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.', default=False, verbose_name='Pedido confirmado?')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor', to='pessoal.Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(max_digits=20, verbose_name='Valor unitário (R$)', decimal_places=2)),
                ('valor_total', models.DecimalField(max_digits=20, verbose_name='Total (R$)', decimal_places=2)),
                ('desconto', models.DecimalField(null=True, max_digits=20, blank=True, verbose_name='Desconto (%)', decimal_places=0)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra', to='compra.Compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto', to='movimento.Produtos')),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
        ),
    ]
