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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('quantidade_inlines_compra', models.IntegerField(verbose_name='Qtde itens de compra', null=True, blank=True, help_text='Quantidade de inlines prévios na compra')),
                ('quantidade_inlines_venda', models.IntegerField(verbose_name='Qtde itens de venda', null=True, blank=True, help_text='Quantidade de inlines prévios na venda')),
                ('habilita_pedido_compra', models.BooleanField(default=True, verbose_name='Habilita pedido de compra?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.')),
                ('habilita_pedido_venda', models.BooleanField(default=True, verbose_name='Habilita pedido de venda?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.')),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(verbose_name='Qtde mínima em estoque', null=True, blank=True, help_text='Indique a quantidade mínima de itens de produto no estoque.')),
                ('perc_valor_minimo_pagamento', models.DecimalField(null=True, decimal_places=0, max_digits=20, verbose_name='Perc. Valor do 1º pagamento', blank=True, help_text='Percentual mínimo do valor do primeiro pagamento de uma parcela.')),
                ('intervalo_dias_entrega_venda', models.IntegerField(default=0, verbose_name='Intervalo para entrega', help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).')),
                ('email_abertura_caixa', models.TextField(verbose_name='Email de abertura de caixa', blank=True, help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.')),
            ],
            options={
                'verbose_name': 'Parametrização',
                'verbose_name_plural': 'Parametrizações',
            },
        ),
    ]
