# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoencargo',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status'),
            preserve_default=True,
        ),
    ]
