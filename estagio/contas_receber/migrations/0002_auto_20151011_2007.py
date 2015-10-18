# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recebimento',
            name='observacao',
            field=models.TextField(blank=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateTimeField(verbose_name='Data do recebimento', auto_now_add=True),
        ),
    ]
