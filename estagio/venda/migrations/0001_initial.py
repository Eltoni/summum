# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
        ('movimento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('status', models.BooleanField(verbose_name='Entrega agendada?', default=False)),
                ('data', models.DateTimeField(blank=True, null=True, verbose_name='Data de entrega')),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da entrega.')),
                ('posicao', geoposition.fields.GeopositionField(blank=True, max_length=42, verbose_name='Posição')),
                ('endereco', models.ForeignKey(blank=True, null=True, to='pessoal.EnderecoEntregaCliente', verbose_name='Endereço', on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0, verbose_name='Desconto (%)')),
                ('remove_estoque', models.BooleanField(verbose_name='Removido do estoque?', default=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('total', models.DecimalField(verbose_name='Total (R$)', help_text='Valor total da venda.', max_digits=20, decimal_places=2)),
                ('data', models.DateTimeField(verbose_name='Data da venda', auto_now_add=True)),
                ('desconto', models.DecimalField(blank=True, null=True, max_digits=20, verbose_name='Desconto (%)', help_text='Desconto sob o valor total da venda.', decimal_places=0)),
                ('status', models.BooleanField(verbose_name='Cancelada?', help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', default=False)),
                ('observacao', models.TextField(blank=True, verbose_name='Observações', help_text='Descreva na área as informações relavantes da venda.')),
                ('pedido', models.CharField(blank=True, max_length=1, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?')),
                ('status_pedido', models.BooleanField(verbose_name='Pedido confirmado?', help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.', default=False)),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendedor', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Vendedor', on_delete=django.db.models.deletion.DO_NOTHING)),
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
            field=models.OneToOneField(blank=True, null=True, verbose_name='Venda', to='venda.Venda'),
        ),
    ]
