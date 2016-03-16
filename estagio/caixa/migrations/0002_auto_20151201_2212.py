# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caixa',
            name='data_abertura',
            field=models.DateTimeField(null=True, help_text='Data de abertura do caixa.', verbose_name='Data de abertura'),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='data_fechamento',
            field=models.DateTimeField(null=True, help_text='Data de fechamento do caixa.', verbose_name='Data de fechamento'),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='diferenca',
            field=models.DecimalField(max_digits=20, help_text='Diferença do Valor Total calculado junto ao valor informado no fechamento do Caixa.', verbose_name='Diferença', decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='valor_entrada',
            field=models.DecimalField(max_digits=20, help_text='Somatório de todos os recebimentos (mov. do tipo Crédito).', verbose_name='Valor de entrada', decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='valor_fechamento',
            field=models.DecimalField(max_digits=20, help_text='Valor calculado manualmente da quantia existente no Caixa em seu fechamento.', verbose_name='Valor de fechamento', decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='valor_inicial',
            field=models.DecimalField(max_digits=20, help_text='Valor existente no Caixa em sua abertura.', verbose_name='Valor inicial', decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='valor_saida',
            field=models.DecimalField(max_digits=20, help_text='Somatório de todos os pagamentos (mov. do tipo Débito).', verbose_name='Valor de saída', decimal_places=2, default=0.0),
        ),
        migrations.AlterField(
            model_name='caixa',
            name='valor_total',
            field=models.DecimalField(max_digits=20, help_text='Valor calculado automaticamente da quantia existente no Caixa em seu fechamento.', verbose_name='Valor total', decimal_places=2, default=0.0),
        ),
    ]
