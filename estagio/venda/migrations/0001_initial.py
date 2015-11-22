# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import geoposition.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(null=True, verbose_name='Data de entrega', blank=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da entrega.')),
                ('posicao', geoposition.fields.GeopositionField(verbose_name='Posição', blank=True, max_length=42)),
                ('endereco', models.ForeignKey(null=True, to='pessoal.EnderecoEntregaCliente', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Endereço')),
            ],
            options={
                'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),),
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
            },
        ),
        migrations.CreateModel(
            name='ItensVenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(null=True, verbose_name='Desconto (%)', blank=True, decimal_places=0, max_digits=20)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos', verbose_name='Produto')),
            ],
            options={
                'verbose_name': 'Item de Venda',
                'verbose_name_plural': 'Itens de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('total', models.DecimalField(verbose_name='Total (R$)', help_text='Valor total da venda.', decimal_places=2, max_digits=20)),
                ('data_venda', models.DateTimeField(null=True, verbose_name='Data da venda')),
                ('data_pedido', models.DateTimeField(null=True, verbose_name='Data do pedido')),
                ('data_cancelamento', models.DateTimeField(null=True, verbose_name='Data do cancelamento')),
                ('desconto', models.DecimalField(null=True, help_text='Desconto sob o valor total da venda.', max_digits=20, verbose_name='Desconto (%)', blank=True, decimal_places=0)),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da venda.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente', verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
                ('vendedor', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, verbose_name='Vendedor')),
            ],
            options={
                'permissions': (('pode_exportar_venda', 'Exportar Vendas'),),
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
            },
        ),
        migrations.AddField(
            model_name='itensvenda',
            name='vendas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venda.Venda', verbose_name='Venda'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(null=True, to='venda.Venda', blank=True, verbose_name='Venda'),
        ),
    ]
