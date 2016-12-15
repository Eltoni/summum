# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import geoposition.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pessoal', '0001_initial'),
        ('parametros_financeiros', '0001_initial'),
        ('movimento', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('status', models.BooleanField(db_index=True, verbose_name='Entrega agendada?', default=False)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data de entrega', blank=True, null=True)),
                ('observacao', models.TextField(verbose_name='Observações', help_text='Descreva na área as informações relavantes da entrega.', blank=True)),
                ('posicao', geoposition.fields.GeopositionField(verbose_name='Posição', blank=True, max_length=42)),
                ('endereco', models.ForeignKey(to='pessoal.EnderecoEntregaCliente', verbose_name='Endereço', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade')),
                ('valor_unitario', models.DecimalField(decimal_places=2, verbose_name='Valor unitário (R$)', max_digits=20)),
                ('valor_total', models.DecimalField(decimal_places=2, verbose_name='Total (R$)', max_digits=20)),
                ('desconto', models.DecimalField(max_digits=20, decimal_places=0, verbose_name='Desconto (%)', blank=True, null=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('total', models.DecimalField(verbose_name='Total (R$)', decimal_places=2, help_text='Valor total da venda.', max_digits=20)),
                ('data_venda', models.DateTimeField(db_index=True, verbose_name='Data da venda', null=True)),
                ('data_pedido', models.DateTimeField(db_index=True, verbose_name='Data do pedido', null=True)),
                ('data_cancelamento', models.DateTimeField(db_index=True, verbose_name='Data do cancelamento', null=True)),
                ('desconto', models.DecimalField(verbose_name='Desconto (%)', max_digits=20, help_text='Desconto sob o valor total da venda.', decimal_places=0, blank=True, null=True)),
                ('status', models.BooleanField(verbose_name='Cancelado?', db_index=True, help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', default=False)),
                ('observacao', models.TextField(verbose_name='Observações', help_text='Descreva na área as informações relavantes da venda.', blank=True)),
                ('pedido', models.CharField(db_index=True, choices=[('S', 'Sim'), ('N', 'Não')], verbose_name='Pedido?', blank=True, max_length=1)),
                ('status_pedido', models.BooleanField(verbose_name='Pedido confirmado?', db_index=True, help_text='Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.', default=False)),
                ('cliente', models.ForeignKey(to='pessoal.Cliente', verbose_name='Cliente', on_delete=django.db.models.deletion.PROTECT)),
                ('forma_pagamento', models.ForeignKey(to='parametros_financeiros.FormaPagamento', verbose_name='Forma de pagamento', on_delete=django.db.models.deletion.PROTECT)),
                ('grupo_encargo', models.ForeignKey(to='parametros_financeiros.GrupoEncargo', verbose_name='Grupo de encargo', on_delete=django.db.models.deletion.PROTECT)),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Vendedor', blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING)),
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
            field=models.ForeignKey(to='venda.Venda', verbose_name='Venda', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(to='venda.Venda', verbose_name='Venda', null=True, blank=True),
        ),
    ]
