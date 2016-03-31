# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parametros_financeiros', '0001_initial'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', models.BooleanField(default=False, verbose_name='Entrega agendada?')),
                ('data', models.DateTimeField(blank=True, verbose_name='Data de entrega', null=True)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da entrega.')),
                ('posicao', geoposition.fields.GeopositionField(blank=True, verbose_name='Posição', max_length=42)),
                ('endereco', models.ForeignKey(to='pessoal.EnderecoEntregaCliente', blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Endereço', null=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', decimal_places=2, max_digits=20)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, max_digits=20)),
                ('desconto', models.DecimalField(blank=True, max_digits=20, verbose_name='Desconto (%)', decimal_places=0, null=True)),
                ('remove_estoque', models.BooleanField(default=False, verbose_name='Removido do estoque?')),
                ('produto', models.ForeignKey(to='movimento.Produtos', on_delete=django.db.models.deletion.PROTECT, verbose_name='Produto')),
            ],
            options={
                'verbose_name_plural': 'Itens de Venda',
                'verbose_name': 'Item de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('total', models.DecimalField(max_digits=20, verbose_name='Total (R$)', decimal_places=2, help_text='Valor total da venda.')),
                ('data_venda', models.DateTimeField(verbose_name='Data da venda', null=True)),
                ('data_pedido', models.DateTimeField(verbose_name='Data do pedido', null=True)),
                ('data_cancelamento', models.DateTimeField(verbose_name='Data do cancelamento', null=True)),
                ('desconto', models.DecimalField(blank=True, verbose_name='Desconto (%)', null=True, help_text='Desconto sob o valor total da venda.', decimal_places=0, max_digits=20)),
                ('status', models.BooleanField(default=False, verbose_name='Cancelado?', help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da venda.')),
                ('pedido', models.CharField(choices=[('S', 'Sim'), ('N', 'Não')], blank=True, verbose_name='Pedido?', max_length=1)),
                ('status_pedido', models.BooleanField(default=False, verbose_name='Pedido confirmado?', help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.')),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente')),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT, verbose_name='Forma de pagamento')),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT, verbose_name='Grupo de encargo')),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='Vendedor', null=True)),
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
            field=models.ForeignKey(to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, verbose_name='Venda'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(blank=True, to='venda.Venda', verbose_name='Venda', null=True),
        ),
    ]
