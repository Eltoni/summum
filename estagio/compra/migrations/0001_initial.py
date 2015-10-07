# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('total', models.DecimalField(help_text='Valor total da compra.', max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da compra')),
                ('desconto', models.DecimalField(help_text='Desconto sob o valor total da compra.', max_digits=20, verbose_name='Desconto (%)', null=True, blank=True, decimal_places=0)),
                ('status', models.BooleanField(help_text='Indica se o status da compra está ativo ou cancelada.', verbose_name='Cancelada?', default=False)),
                ('observacao', models.TextField(blank=True, help_text='Descreva na área as informações relavantes da compra.', verbose_name='Observações')),
                ('pedido', models.CharField(blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.', verbose_name='Pedido confirmado?', default=False)),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento')),
                ('fornecedor', models.ForeignKey(verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Fornecedor')),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo')),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor unitário (R$)')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('desconto', models.DecimalField(blank=True, max_digits=20, decimal_places=0, verbose_name='Desconto (%)', null=True)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT, to='compra.Compra')),
                ('produto', models.ForeignKey(verbose_name='Produto', on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos')),
            ],
            options={
                'verbose_name_plural': 'Itens de Compra',
                'verbose_name': 'Item de Compra',
            },
        ),
    ]
