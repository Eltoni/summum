# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0002_contasreceber_vendas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data do recebimento'),
        ),
    ]
