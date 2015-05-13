# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cidade',
            name='ultima_alteracao',
        ),
        migrations.AlterField(
            model_name='cidade',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
    ]
