# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import geoposition.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pessoal', '0001_initial'),
        ('movimento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(null=True, verbose_name='Data de entrega', blank=True)),
                ('observacao', models.TextField(help_text='Descreva na \xe1rea as informa\xe7\xf5es relavantes da entrega.', verbose_name='Observa\xe7\xf5es', blank=True)),
                ('posicao', geoposition.fields.GeopositionField(max_length=42, verbose_name='Posi\xe7\xe3o', blank=True)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Endere\xe7o', blank=True, to='pessoal.EnderecoEntregaCliente', null=True)),
            ],
            options={
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
                'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),),
            },
        ),
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
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='Vendedor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
                'permissions': (('pode_exportar_venda', 'Exportar Vendas'),),
            },
        ),
        migrations.AddField(
            model_name='itensvenda',
            name='vendas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda', to='venda.Venda'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(null=True, blank=True, to='venda.Venda', verbose_name='Venda'),
        ),
    ]
