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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('quantidade_inlines_compra', models.IntegerField(blank=True, help_text='Quantidade de inlines prévios na compra', verbose_name='Qtde itens de compra', null=True)),
                ('quantidade_inlines_venda', models.IntegerField(blank=True, help_text='Quantidade de inlines prévios na venda', verbose_name='Qtde itens de venda', null=True)),
                ('habilita_pedido_compra', models.BooleanField(help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.', verbose_name='Habilita pedido de compra?', default=True)),
                ('habilita_pedido_venda', models.BooleanField(help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.', verbose_name='Habilita pedido de venda?', default=True)),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(blank=True, help_text='Indique a quantidade mínima de itens de produto no estoque.', verbose_name='Qtde mínima em estoque', null=True)),
                ('perc_valor_minimo_pagamento', models.DecimalField(help_text='Percentual mínimo do valor do primeiro pagamento de uma parcela.', max_digits=20, verbose_name='Perc. Valor do 1º pagamento', null=True, blank=True, decimal_places=0)),
                ('intervalo_dias_entrega_venda', models.IntegerField(help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).', default=0, verbose_name='Intervalo para entrega')),
                ('email_abertura_caixa', models.TextField(blank=True, help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.', verbose_name='Email de abertura de caixa')),
                ('evento_calendario', models.CharField(help_text='Defina o calendário de eventos que aparecerão no dashboard do sistema.', max_length=200, verbose_name='Calendário de eventos', null=True)),
            ],
            options={
                'verbose_name_plural': 'Parametrizações',
                'verbose_name': 'Parametrização',
            },
        ),
    ]
