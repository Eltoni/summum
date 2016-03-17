# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0007_auto_20160312_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banco',
            name='site',
            field=models.URLField(blank=True, verbose_name='Site'),
        ),
    ]
