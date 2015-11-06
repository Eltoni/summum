# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, unique=True, verbose_name='Nome')),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='marcas', verbose_name='Logo')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('preco', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Preço de compra')),
                ('preco_venda', models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Preço de venda')),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Indica se o produto está ativo para atividades de compra e venda.')),
                ('imagem', sorl.thumbnail.fields.ImageField(blank=True, max_length=255, upload_to='produtos', verbose_name='Imagem')),
                ('categorias', models.ManyToManyField(blank=True, verbose_name='Categoria', to='movimento.Categoria')),
                ('marca', models.ForeignKey(null=True, to='movimento.Marca', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Marca')),
            ],
            options={
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name_plural': 'Produtos',
                'verbose_name': 'Produto',
            },
        ),
    ]
