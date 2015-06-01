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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20, help_text='Valor total da compra.')),
                ('data', models.DateTimeField(verbose_name='Data da compra', auto_now_add=True)),
                ('desconto', models.DecimalField(null=True, decimal_places=0, max_digits=20, verbose_name='Desconto (%)', blank=True, help_text='Desconto sob o valor total da compra.')),
                ('status', models.BooleanField(default=False, verbose_name='Cancelada?', help_text='Indica se o status da compra está ativo ou cancelada.')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da compra.')),
                ('pedido', models.CharField(verbose_name='Pedido?', blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')])),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.')),
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', decimal_places=2, max_digits=20)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', null=True, decimal_places=0, max_digits=20, blank=True)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(to='compra.Compra', verbose_name='Compra', on_delete=django.db.models.deletion.PROTECT)),
                ('produto', models.ForeignKey(to='movimento.Produtos', verbose_name='Produto', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
        ),
    ]
