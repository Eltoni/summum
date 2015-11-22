# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0003_auto_20151122_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recebimento',
            name='data',
            field=models.DateTimeField(verbose_name='Data do recebimento'),
        ),
    ]
