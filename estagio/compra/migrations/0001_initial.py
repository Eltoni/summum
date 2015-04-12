# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
        ('pessoal', '__first__'),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(help_text='Valor total da compra.', verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da compra')),
                ('desconto', models.DecimalField(decimal_places=0, max_digits=20, blank=True, help_text='Desconto sob o valor total da compra.', null=True, verbose_name='Desconto (%)')),
                ('status', models.BooleanField(default=False, help_text='Marcando o Checkbox, a compra ser\xe1 cancelada e o financeiro acertado.', verbose_name='Cancelada?')),
                ('observacao', models.TextField(help_text='Descreva na \xe1rea as informa\xe7\xf5es relavantes da compra.', verbose_name='Observa\xe7\xf5es', blank=True)),
                ('pedido', models.CharField(blank=True, max_length=1, verbose_name='Pedido?', choices=[('S', 'Sim'), ('N', 'N\xe3o')])),
                ('status_pedido', models.BooleanField(default=False, help_text='Marcando o Checkbox, os itens financeiros ser\xe3o gerados e o estoque movimentado.', verbose_name='Pedido confirmado?')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Fornecedor', to='pessoal.Fornecedor')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ItensCompra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.IntegerField()),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unit\xe1rio (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto (%)', max_digits=20, decimal_places=0, blank=True)),
                ('add_estoque', models.BooleanField(default=False, verbose_name='Adicionado ao estoque?')),
                ('compras', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Compra', to='compra.Compra')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto', to='movimento.Produtos')),
            ],
            options={
                'verbose_name': 'Item de Compra',
                'verbose_name_plural': 'Itens de Compra',
            },
            bases=(models.Model,),
        ),
    ]
