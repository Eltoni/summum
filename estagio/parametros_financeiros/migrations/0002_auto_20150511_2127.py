# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formapagamento',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='grupoencargo',
            name='nome',
            field=models.CharField(unique=True, max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='grupoencargo',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
    ]
