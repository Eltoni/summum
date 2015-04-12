# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parametrizacao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade_inlines_compra', models.IntegerField(help_text='Quantidade de inlines pr\xe9vios na compra', null=True, verbose_name='Qtde itens de compra', blank=True)),
                ('quantidade_inlines_venda', models.IntegerField(help_text='Quantidade de inlines pr\xe9vios na venda', null=True, verbose_name='Qtde itens de venda', blank=True)),
                ('habilita_pedido_compra', models.BooleanField(default=True, help_text='Marcando o Checkbox, o bot\xe3o para adicionar um pedido de compra ser\xe1 exibido no cadastro da compra.', verbose_name='Habilita pedido de compra?')),
                ('habilita_pedido_venda', models.BooleanField(default=True, help_text='Marcando o Checkbox, o bot\xe3o para adicionar um pedido de venda ser\xe1 exibido no cadastro da venda.', verbose_name='Habilita pedido de venda?')),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(help_text='Indique a quantidade m\xednima de itens de produto no estoque.', null=True, verbose_name='Qtde m\xednima em estoque', blank=True)),
                ('perc_valor_minimo_pagamento', models.DecimalField(decimal_places=0, max_digits=20, blank=True, help_text='Percentual m\xednimo do valor do primeiro pagamento de uma parcela.', null=True, verbose_name='Perc. Valor do 1\xba pagamento')),
            ],
            options={
                'verbose_name': 'Parametriza\xe7\xe3o',
                'verbose_name_plural': 'Parametriza\xe7\xf5es',
            },
            bases=(models.Model,),
        ),
    ]
