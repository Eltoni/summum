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
            name='ItensVenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unit\xe1rio (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto (%)', max_digits=20, decimal_places=0, blank=True)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto', to='movimento.Produtos')),
            ],
            options={
                'verbose_name': 'Item de Venda',
                'verbose_name_plural': 'Itens de Venda',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total', models.DecimalField(help_text='Valor total da venda.', verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da venda')),
                ('desconto', models.DecimalField(decimal_places=0, max_digits=20, blank=True, help_text='Desconto sob o valor total da venda.', null=True, verbose_name='Desconto (%)')),
                ('status', models.BooleanField(default=False, help_text='Marcando o Checkbox, a venda ser\xe1 cancelada e os itens financeiros estornados.', verbose_name='Cancelada?')),
                ('observacao', models.TextField(help_text='Descreva na \xe1rea as informa\xe7\xf5es relavantes da venda.', verbose_name='Observa\xe7\xf5es', blank=True)),
                ('pedido', models.CharField(blank=True, max_length=1, verbose_name='Pedido?', choices=[('S', 'Sim'), ('N', 'N\xe3o')])),
                ('status_pedido', models.BooleanField(default=False, help_text='Marcando o Checkbox, os itens financeiros ser\xe3o gerados e o estoque movimentado.', verbose_name='Pedido confirmado?')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente?', to='pessoal.Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='itensvenda',
            name='vendas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda', to='venda.Venda'),
            preserve_default=True,
        ),
    ]
