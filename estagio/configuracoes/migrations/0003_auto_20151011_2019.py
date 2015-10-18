# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0002_auto_20150906_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametrizacao',
            name='perc_valor_minimo_pagamento',
        ),
        migrations.AddField(
            model_name='parametrizacao',
            name='perc_valor_minimo_recebimento',
            field=models.DecimalField(verbose_name='Perc. Valor do 1º recebimento', decimal_places=0, null=True, max_digits=20, blank=True, help_text='Percentual mínimo do valor do primeiro recebimento de uma parcela.'),
        ),
    ]
