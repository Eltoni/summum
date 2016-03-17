# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0003_auto_20160310_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banco',
            name='site',
            field=models.EmailField(blank=True, max_length=100, verbose_name='Site'),
        ),
    ]
