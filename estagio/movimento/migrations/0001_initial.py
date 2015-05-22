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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=255, verbose_name='Nome')),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=255, verbose_name='Nome')),
                ('logo', sorl.thumbnail.fields.ImageField(upload_to=b'marcas', max_length=255, verbose_name='Logo', blank=True)),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('preco', models.DecimalField(verbose_name='Pre\xe7o de compra', max_digits=20, decimal_places=2)),
                ('preco_venda', models.DecimalField(verbose_name='Pre\xe7o de venda', max_digits=20, decimal_places=2)),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('descricao', models.TextField(verbose_name='Descri\xe7\xe3o', blank=True)),
                ('status', models.BooleanField(default=True, help_text='Indica se o produto est\xe1 ativo para atividades de compra e venda.', verbose_name='Status')),
                ('imagem', sorl.thumbnail.fields.ImageField(upload_to=b'produtos', max_length=255, verbose_name='Imagem', blank=True)),
                ('categorias', models.ManyToManyField(to='movimento.Categoria', verbose_name='Categoria', blank=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Marca', blank=True, to='movimento.Marca', null=True)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
            },
        ),
    ]
