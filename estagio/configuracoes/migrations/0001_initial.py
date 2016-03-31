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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('quantidade_inlines_compra', models.IntegerField(blank=True, verbose_name='Qtde itens de compra', null=True, help_text='Quantidade de inlines prévios na compra')),
                ('quantidade_inlines_venda', models.IntegerField(blank=True, verbose_name='Qtde itens de venda', null=True, help_text='Quantidade de inlines prévios na venda')),
                ('habilita_pedido_compra', models.BooleanField(default=True, verbose_name='Habilita pedido de compra?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.')),
                ('habilita_pedido_venda', models.BooleanField(default=True, verbose_name='Habilita pedido de venda?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.')),
                ('periodo_venc_pedido_compra', models.IntegerField(blank=True, verbose_name='Período de vencimento do pedido (dias)', null=True, help_text='Defina o período de vencimento de um pedido de compra. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.')),
                ('periodo_venc_pedido_venda', models.IntegerField(blank=True, verbose_name='Período de vencimento do pedido (dias)', null=True, help_text='Defina o período de vencimento de um pedido de venda. Após o período estipulado, caso o pedido encontre-se sem confirmação, este será cancelado automaticamente.<br>configure-o baseado em dias inteiros.')),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(blank=True, verbose_name='Qtde mínima em estoque', null=True, help_text='Indique a quantidade mínima de itens de produto no estoque.')),
                ('perc_valor_minimo_recebimento', models.DecimalField(blank=True, verbose_name='Perc. Valor do 1º recebimento', null=True, help_text='Percentual mínimo do valor do primeiro recebimento de uma parcela.', decimal_places=0, max_digits=20)),
                ('intervalo_dias_entrega_venda', models.IntegerField(default=0, verbose_name='Intervalo para entrega', help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).')),
                ('email_abertura_caixa', models.TextField(blank=True, verbose_name='Email de abertura de caixa', help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.')),
                ('evento_calendario', models.CharField(blank=True, max_length=200, verbose_name='Calendário de eventos', null=True, help_text='Defina o calendário de eventos que aparecerão no dashboard do sistema.')),
            ],
            options={
                'verbose_name_plural': 'Parametrizações',
                'verbose_name': 'Parametrização',
            },
        ),
    ]
