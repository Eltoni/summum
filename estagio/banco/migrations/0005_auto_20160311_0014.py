# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0004_auto_20160310_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banco',
            name='banco',
            field=models.CharField(unique=True, verbose_name='Banco', max_length=10),
        ),
    ]
