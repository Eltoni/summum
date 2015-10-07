# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='marcas', verbose_name='Logo')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('preco', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Preço de compra')),
                ('preco_venda', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Preço de venda')),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('status', models.BooleanField(help_text='Indica se o produto está ativo para atividades de compra e venda.', verbose_name='Status', default=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='produtos', verbose_name='Imagem')),
                ('categorias', models.ManyToManyField(blank=True, verbose_name='Categoria', to='movimento.Categoria')),
                ('marca', models.ForeignKey(verbose_name='Marca', null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to='movimento.Marca')),
            ],
            options={
                'verbose_name_plural': 'Produtos',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name': 'Produto',
            },
        ),
    ]
