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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('quantidade_inlines_compra', models.IntegerField(null=True, verbose_name='Qtde itens de compra', help_text='Quantidade de inlines prévios na compra', blank=True)),
                ('quantidade_inlines_venda', models.IntegerField(null=True, verbose_name='Qtde itens de venda', help_text='Quantidade de inlines prévios na venda', blank=True)),
                ('habilita_pedido_compra', models.BooleanField(default=True, verbose_name='Habilita pedido de compra?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de compra será exibido no cadastro da compra.')),
                ('habilita_pedido_venda', models.BooleanField(default=True, verbose_name='Habilita pedido de venda?', help_text='Marcando o Checkbox, o botão para adicionar um pedido de venda será exibido no cadastro da venda.')),
                ('qtde_minima_produtos_em_estoque', models.IntegerField(null=True, verbose_name='Qtde mínima em estoque', help_text='Indique a quantidade mínima de itens de produto no estoque.', blank=True)),
                ('perc_valor_minimo_recebimento', models.DecimalField(max_digits=20, null=True, blank=True, decimal_places=0, verbose_name='Perc. Valor do 1º recebimento', help_text='Percentual mínimo do valor do primeiro recebimento de uma parcela.')),
                ('intervalo_dias_entrega_venda', models.IntegerField(default=0, verbose_name='Intervalo para entrega', help_text='Intervalo mínimo entre a data de venda e a data de entrega (dias).')),
                ('email_abertura_caixa', models.TextField(blank=True, verbose_name='Email de abertura de caixa', help_text='Insira uma mensagem customizada. Esta será exibida acima do rodapé no email de abertura do caixa.')),
                ('evento_calendario', models.CharField(null=True, max_length=200, verbose_name='Calendário de eventos', help_text='Defina o calendário de eventos que aparecerão no dashboard do sistema.', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Parametrizações',
                'verbose_name': 'Parametrização',
            },
        ),
    ]
