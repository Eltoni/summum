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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=255)),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Logo', upload_to='marcas', max_length=255)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('preco', models.DecimalField(verbose_name='Preço de compra', decimal_places=2, max_digits=20)),
                ('preco_venda', models.DecimalField(verbose_name='Preço de venda', decimal_places=2, max_digits=20)),
                ('quantidade', models.IntegerField(default=0, verbose_name='Quantidade')),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Indica se o produto está ativo para atividades de compra e venda.')),
                ('imagem', sorl.thumbnail.fields.ImageField(blank=True, verbose_name='Imagem', upload_to='produtos', max_length=255)),
                ('categorias', models.ManyToManyField(blank=True, to='movimento.Categoria', verbose_name='Categoria')),
                ('marca', models.ForeignKey(to='movimento.Marca', blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Marca', null=True)),
            ],
            options={
                'verbose_name_plural': 'Produtos',
                'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos')),
                'verbose_name': 'Produto',
            },
        ),
    ]
