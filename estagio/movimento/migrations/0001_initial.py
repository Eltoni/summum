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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('logo', sorl.thumbnail.fields.ImageField(verbose_name='Logo', blank=True, max_length=255, upload_to='marcas')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('preco', models.DecimalField(verbose_name='Preço de compra', decimal_places=2, max_digits=20)),
                ('preco_venda', models.DecimalField(verbose_name='Preço de venda', decimal_places=2, max_digits=20)),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Indica se o produto está ativo para atividades de compra e venda.')),
                ('imagem', sorl.thumbnail.fields.ImageField(verbose_name='Imagem', blank=True, max_length=255, upload_to='produtos')),
                ('categorias', models.ManyToManyField(verbose_name='Categoria', blank=True, to='movimento.Categoria')),
                ('marca', models.ForeignKey(to='movimento.Marca', null=True, verbose_name='Marca', blank=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Produto',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
