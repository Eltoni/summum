# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(verbose_name='Data de entrega', null=True, blank=True)),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da entrega.')),
                ('posicao', geoposition.fields.GeopositionField(verbose_name='Posição', blank=True, max_length=42)),
                ('endereco', models.ForeignKey(to='pessoal.EnderecoEntregaCliente', null=True, verbose_name='Endereço', blank=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Entrega',
                'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),),
                'verbose_name_plural': 'Entregas',
            },
        ),
        migrations.CreateModel(
            name='ItensVenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', decimal_places=2, max_digits=20)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', null=True, decimal_places=0, max_digits=20, blank=True)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(to='movimento.Produtos', verbose_name='Produto', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Item de Venda',
                'verbose_name_plural': 'Itens de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20, help_text='Valor total da venda.')),
                ('data', models.DateTimeField(verbose_name='Data da venda', auto_now_add=True)),
                ('desconto', models.DecimalField(null=True, decimal_places=0, max_digits=20, verbose_name='Desconto (%)', blank=True, help_text='Desconto sob o valor total da venda.')),
                ('status', models.BooleanField(default=False, verbose_name='Cancelada?', help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.')),
                ('observacao', models.TextField(verbose_name='Observações', blank=True, help_text='Descreva na área as informações relavantes da venda.')),
                ('pedido', models.CharField(verbose_name='Pedido?', blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')])),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.')),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Vendedor', blank=True, on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'verbose_name': 'Venda',
                'permissions': (('pode_exportar_venda', 'Exportar Vendas'),),
                'verbose_name_plural': 'Vendas',
            },
        ),
        migrations.AddField(
            model_name='itensvenda',
            name='vendas',
            field=models.ForeignKey(to='venda.Venda', verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(null=True, verbose_name='Venda', blank=True, to='venda.Venda'),
        ),
    ]
