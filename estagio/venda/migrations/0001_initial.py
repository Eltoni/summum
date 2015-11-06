# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
        ('pessoal', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(null=True, verbose_name='Data de entrega', blank=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da entrega.')),
                ('posicao', geoposition.fields.GeopositionField(blank=True, max_length=42, verbose_name='Posição')),
                ('endereco', models.ForeignKey(null=True, to='pessoal.EnderecoEntregaCliente', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Endereço')),
            ],
            options={
                'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),),
                'verbose_name_plural': 'Entregas',
                'verbose_name': 'Entrega',
            },
        ),
        migrations.CreateModel(
            name='ItensVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor unitário (R$)')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('desconto', models.DecimalField(max_digits=20, null=True, decimal_places=0, verbose_name='Desconto (%)', blank=True)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos', verbose_name='Produto')),
            ],
            options={
                'verbose_name_plural': 'Itens de Venda',
                'verbose_name': 'Item de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)', help_text='Valor total da venda.')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da venda')),
                ('desconto', models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=0, verbose_name='Desconto (%)', help_text='Desconto sob o valor total da venda.')),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da venda.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, max_length=1, verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente', verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo')),
                ('vendedor', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.DO_NOTHING, blank=True, verbose_name='Vendedor')),
            ],
            options={
                'permissions': (('pode_exportar_venda', 'Exportar Vendas'),),
                'verbose_name_plural': 'Vendas',
                'verbose_name': 'Venda',
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
