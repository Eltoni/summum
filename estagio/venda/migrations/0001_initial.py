# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(blank=True, verbose_name='Data de entrega', null=True)),
                ('observacao', models.TextField(blank=True, help_text='Descreva na área as informações relavantes da entrega.', verbose_name='Observações')),
                ('posicao', geoposition.fields.GeopositionField(blank=True, max_length=42, verbose_name='Posição')),
                ('endereco', models.ForeignKey(verbose_name='Endereço', null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to='pessoal.EnderecoEntregaCliente')),
            ],
            options={
                'verbose_name_plural': 'Entregas',
                'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),),
                'verbose_name': 'Entrega',
            },
        ),
        migrations.CreateModel(
            name='ItensVenda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Valor unitário (R$)')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('desconto', models.DecimalField(blank=True, max_digits=20, decimal_places=0, verbose_name='Desconto (%)', null=True)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(verbose_name='Produto', on_delete=django.db.models.deletion.PROTECT, to='movimento.Produtos')),
            ],
            options={
                'verbose_name_plural': 'Itens de Venda',
                'verbose_name': 'Item de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('total', models.DecimalField(help_text='Valor total da venda.', max_digits=20, decimal_places=2, verbose_name='Total (R$)')),
                ('data', models.DateTimeField(auto_now_add=True, verbose_name='Data da venda')),
                ('desconto', models.DecimalField(help_text='Desconto sob o valor total da venda.', max_digits=20, verbose_name='Desconto (%)', null=True, blank=True, decimal_places=0)),
                ('status', models.BooleanField(help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', verbose_name='Cancelada?', default=False)),
                ('observacao', models.TextField(blank=True, help_text='Descreva na área as informações relavantes da venda.', verbose_name='Observações')),
                ('pedido', models.CharField(blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.', verbose_name='Pedido confirmado?', default=False)),
                ('cliente', models.ForeignKey(verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT, to='pessoal.Cliente')),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.FormaPagamento')),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT, to='parametros_financeiros.GrupoEncargo')),
                ('vendedor', models.ForeignKey(verbose_name='Vendedor', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Vendas',
                'permissions': (('pode_exportar_venda', 'Exportar Vendas'),),
                'verbose_name': 'Venda',
            },
        ),
        migrations.AddField(
            model_name='itensvenda',
            name='vendas',
            field=models.ForeignKey(verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT, to='venda.Venda'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(verbose_name='Venda', null=True, blank=True, to='venda.Venda'),
        ),
    ]
