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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('logo', sorl.thumbnail.fields.ImageField(upload_to='marcas', verbose_name='Logo', blank=True, max_length=255)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('preco', models.DecimalField(decimal_places=2, verbose_name='Preço de compra', max_digits=20)),
                ('preco_venda', models.DecimalField(decimal_places=2, verbose_name='Preço de venda', max_digits=20)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade', default=0)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('status', models.BooleanField(verbose_name='Status', db_index=True, help_text='Indica se o produto está ativo para atividades de compra e venda.', default=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(upload_to='produtos', verbose_name='Imagem', blank=True, max_length=255)),
                ('categorias', models.ManyToManyField(to='movimento.Categoria', verbose_name='Categoria', blank=True)),
                ('marca', models.ForeignKey(to='movimento.Marca', verbose_name='Marca', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
    ]
