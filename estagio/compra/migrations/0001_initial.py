# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('total', models.DecimalField(verbose_name='Total (R$)', help_text='Valor total da compra.', max_digits=20, decimal_places=2)),
                ('data', models.DateTimeField(verbose_name='Data da compra', auto_now_add=True)),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, verbose_name='Desconto (%)', help_text='Desconto sob o valor total da compra.', decimal_places=0)),
                ('status', models.BooleanField(verbose_name='Cancelada?', help_text='Indica se o status da compra está ativo ou cancelada.', default=False)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da compra.')),
                ('pedido', models.CharField(blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(verbose_name='Pedido confirmado?', help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.', default=False)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedor', models.ForeignKey(to='pessoal.Fornecedor', verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Compra',
                'permissions': (('pode_exportar_compra', 'Exportar Compras'),),
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='ItensCompra',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0, verbose_name='Desconto (%)')),
                ('add_estoque', models.BooleanField(verbose_name='Adicionado ao estoque?', default=False)),
                ('compras', models.ForeignKey(to='compra.Compra', verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT)),
                ('produto', models.ForeignKey(to='movimento.Produtos', verbose_name='Produto', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
        ),
    ]
