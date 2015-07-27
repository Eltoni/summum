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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('quantidade_inlines_compra', models.IntegerField(blank=True, null=True, help_text='Quantidade de inlines prévios na compra', verbose_name='Qtde itens de compra')),
                ('quantidade_inlines_venda', models.IntegerField(blank=True, null=True, help_text='Quantidade de inlines prévios na venda', verbose_name='Qtde itens de venda')),
                ('habilita_pedido_compra', models.BooleanField(verbose_name='Habilita pedido de compra?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.', default=True)),
                ('habilita_pedido_venda', models.BooleanField(verbose_name='Habilita pedido de venda?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.', default=True)),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(blank=True, null=True, help_text='Indique a quantidade mínima de itens de produto no estoque.', verbose_name='Qtde mínima em estoque')),
                ('perc_valor_minimo_pagamento', models.DecimalField(blank=True, null=True, max_digits=20, verbose_name='Perc. Valor do 1º pagamento', help_text='Percentual mínimo do valor do primeiro pagamento de uma parcela.', decimal_places=0)),
                ('intervalo_dias_entrega_venda', models.IntegerField(verbose_name='Intervalo para entrega', help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).', default=0)),
                ('email_abertura_caixa', models.TextField(blank=True, verbose_name='Email de abertura de caixa', help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.')),
            ],
            options={
                'verbose_name': 'Parametrização',
                'verbose_name_plural': 'Parametrizações',
            },
        ),
    ]
