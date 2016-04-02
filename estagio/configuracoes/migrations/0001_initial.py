# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parametrizacao',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('quantidade_inlines_compra', models.IntegerField(verbose_name='Qtde itens de compra', help_text='Quantidade de inlines prévios na compra', blank=True, null=True)),
                ('quantidade_inlines_venda', models.IntegerField(verbose_name='Qtde itens de venda', help_text='Quantidade de inlines prévios na venda', blank=True, null=True)),
                ('habilita_pedido_compra', models.BooleanField(verbose_name='Habilita pedido de compra?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.', default=True)),
                ('habilita_pedido_venda', models.BooleanField(verbose_name='Habilita pedido de venda?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.', default=True)),
                ('periodo_venc_pedido_compra', models.IntegerField(verbose_name='Período de vencimento do pedido (dias)', help_text='Defina o período de vencimento de um pedido de compra. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.', blank=True, null=True)),
                ('periodo_venc_pedido_venda', models.IntegerField(verbose_name='Período de vencimento do pedido (dias)', help_text='Defina o período de vencimento de um pedido de venda. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.', blank=True, null=True)),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(verbose_name='Qtde mínima em estoque', help_text='Indique a quantidade mínima de itens de produto no estoque.', blank=True, null=True)),
                ('perc_valor_minimo_recebimento', models.DecimalField(verbose_name='Perc. Valor do 1º recebimento', max_digits=20, help_text='Percentual mínimo do valor do primeiro recebimento de uma parcela.', decimal_places=0, blank=True, null=True)),
                ('intervalo_dias_entrega_venda', models.IntegerField(verbose_name='Intervalo para entrega', help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).', default=0)),
                ('email_abertura_caixa', models.TextField(verbose_name='Email de abertura de caixa', help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.', blank=True)),
                ('evento_calendario', models.CharField(verbose_name='Calendário de eventos', help_text='Defina o calendário de eventos que aparecerão no dashboard do sistema.', blank=True, null=True, max_length=200)),
            ],
            options={
                'verbose_name': 'Parametrização',
                'verbose_name_plural': 'Parametrizações',
            },
        ),
    ]
