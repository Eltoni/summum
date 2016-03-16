# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(null=True, blank=True, verbose_name='Data de entrega')),
                ('observacao', models.TextField(help_text='Descreva na área as informações relavantes da entrega.', blank=True, verbose_name='Observações')),
                ('posicao', geoposition.fields.GeopositionField(blank=True, verbose_name='Posição', max_length=42)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='pessoal.EnderecoEntregaCliente', null=True, verbose_name='Endereço')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(max_digits=20, verbose_name='Valor unitário (R$)', decimal_places=2)),
                ('valor_total', models.DecimalField(max_digits=20, verbose_name='Total (R$)', decimal_places=2)),
                ('desconto', models.DecimalField(null=True, max_digits=20, blank=True, verbose_name='Desconto (%)', decimal_places=0)),
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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('total', models.DecimalField(help_text='Valor total da venda.', max_digits=20, verbose_name='Total (R$)', decimal_places=2)),
                ('data_venda', models.DateTimeField(null=True, verbose_name='Data da venda')),
                ('data_pedido', models.DateTimeField(null=True, verbose_name='Data do pedido')),
                ('data_cancelamento', models.DateTimeField(null=True, verbose_name='Data do cancelamento')),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', null=True, help_text='Desconto sob o valor total da venda.', max_digits=20, blank=True, decimal_places=0)),
                ('status', models.BooleanField(help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', default=False, verbose_name='Cancelado?')),
                ('observacao', models.TextField(help_text='Descreva na área as informações relavantes da venda.', blank=True, verbose_name='Observações')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.', default=False, verbose_name='Pedido confirmado?')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='Vendedor')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda', to='venda.Venda'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(verbose_name='Venda', blank=True, to='venda.Venda', null=True),
        ),
    ]
