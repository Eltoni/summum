# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255, unique=True)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255, unique=True)),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='marcas', verbose_name='Logo')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('preco', models.DecimalField(verbose_name='Preço de compra', max_digits=20, decimal_places=2)),
                ('preco_venda', models.DecimalField(verbose_name='Preço de venda', max_digits=20, decimal_places=2)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade', default=0)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('status', models.BooleanField(verbose_name='Status', help_text='Indica se o produto está ativo para atividades de compra e venda.', default=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='produtos', verbose_name='Imagem')),
                ('categorias', models.ManyToManyField(blank=True, verbose_name='Categoria', to='movimento.Categoria')),
                ('marca', models.ForeignKey(blank=True, null=True, to='movimento.Marca', verbose_name='Marca', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Produto',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
