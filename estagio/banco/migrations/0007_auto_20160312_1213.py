# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0006_auto_20160311_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencia',
            name='nome',
            field=models.CharField(max_length=75, verbose_name='Nome'),
        ),
    ]
