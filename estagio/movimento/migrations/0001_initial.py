# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('logo', sorl.thumbnail.fields.ImageField(max_length=255, verbose_name='Logo', upload_to='marcas', blank=True)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('preco', models.DecimalField(max_digits=20, verbose_name='Preço de compra', decimal_places=2)),
                ('preco_venda', models.DecimalField(max_digits=20, verbose_name='Preço de venda', decimal_places=2)),
                ('quantidade', models.IntegerField(verbose_name='Quantidade', default=0)),
                ('descricao', models.TextField(verbose_name='Descrição', blank=True)),
                ('status', models.BooleanField(verbose_name='Status', help_text='Indica se o produto está ativo para atividades de compra e venda.', default=True)),
                ('imagem', sorl.thumbnail.fields.ImageField(max_length=255, verbose_name='Imagem', upload_to='produtos', blank=True)),
                ('categorias', models.ManyToManyField(verbose_name='Categoria', to='movimento.Categoria', blank=True)),
                ('marca', models.ForeignKey(to='movimento.Marca', blank=True, null=True, verbose_name='Marca', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
            },
        ),
    ]
