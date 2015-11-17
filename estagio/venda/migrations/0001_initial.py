# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.BooleanField(verbose_name='Entrega agendada?', default=False)),
                ('data', models.DateTimeField(verbose_name='Data de entrega', blank=True, null=True)),
                ('observacao', models.TextField(help_text='Descreva na área as informações relavantes da entrega.', verbose_name='Observações', blank=True)),
                ('posicao', geoposition.fields.GeopositionField(verbose_name='Posição', blank=True, max_length=42)),
                ('endereco', models.ForeignKey(to='pessoal.EnderecoEntregaCliente', blank=True, verbose_name='Endereço', null=True, on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(verbose_name='Valor unitário (R$)', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, decimal_places=2)),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', max_digits=20, blank=True, null=True, decimal_places=0)),
                ('remove_estoque', models.BooleanField(verbose_name='Removido do estoque?', default=False)),
                ('produto', models.ForeignKey(verbose_name='Produto', to='movimento.Produtos', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Item de Venda',
                'verbose_name_plural': 'Itens de Venda',
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('total', models.DecimalField(verbose_name='Total (R$)', max_digits=20, help_text='Valor total da venda.', decimal_places=2)),
                ('data_venda', models.DateTimeField(verbose_name='Data da venda', null=True)),
                ('data_pedido', models.DateTimeField(verbose_name='Data do pedido', null=True)),
                ('data_cancelamento', models.DateTimeField(verbose_name='Data do cancelamento', null=True)),
                ('desconto', models.DecimalField(max_digits=20, help_text='Desconto sob o valor total da venda.', blank=True, verbose_name='Desconto (%)', decimal_places=0, null=True)),
                ('status', models.BooleanField(help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', verbose_name='Cancelado?', default=False)),
                ('observacao', models.TextField(help_text='Descreva na área as informações relavantes da venda.', verbose_name='Observações', blank=True)),
                ('pedido', models.CharField(verbose_name='Pedido?', blank=True, choices=[('S', 'Sim'), ('N', 'Não')], max_length=1)),
                ('status_pedido', models.BooleanField(help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.', verbose_name='Pedido confirmado?', default=False)),
                ('cliente', models.ForeignKey(verbose_name='Cliente', to='pessoal.Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(verbose_name='Forma de pagamento', to='parametros_financeiros.FormaPagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(verbose_name='Grupo de encargo', to='parametros_financeiros.GrupoEncargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Vendedor', null=True, on_delete=django.db.models.deletion.DO_NOTHING)),
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
            field=models.ForeignKey(verbose_name='Venda', to='venda.Venda', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(blank=True, verbose_name='Venda', null=True, to='venda.Venda'),
        ),
    ]
