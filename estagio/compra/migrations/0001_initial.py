# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, help_text='Valor total da compra.', max_digits=20)),
                ('data_compra', models.DateTimeField(db_index=True, verbose_name='Data da compra', null=True)),
                ('data_pedido', models.DateTimeField(db_index=True, verbose_name='Data do pedido', null=True)),
                ('data_cancelamento', models.DateTimeField(db_index=True, verbose_name='Data do cancelamento', null=True)),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', max_digits=20, help_text='Desconto sob o valor total da compra.', decimal_places=0, blank=True, null=True)),
                ('status', models.BooleanField(verbose_name='Cancelado?', db_index=True, help_text='Indica se o status da compra está ativo ou cancelada.', default=False)),
                ('observacao', models.TextField(verbose_name='Observações', help_text='Descreva na área as informações relavantes da compra.', blank=True)),
                ('pedido', models.CharField(db_index=True, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?', blank=True, max_length=1)),
                ('status_pedido', models.BooleanField(verbose_name='Pedido confirmado?', db_index=True, help_text='Caso confirmado, os itens financeiros serão gerados e o estoque movimentado.', default=False)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('fornecedor', models.ForeignKey(to='pessoal.Fornecedor', verbose_name='Fornecedor', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(decimal_places=2, verbose_name='Valor unitário (R$)', max_digits=20)),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Total (R$)', max_digits=20)),
                ('desconto', models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Desconto (%)', blank=True, null=True)),
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
