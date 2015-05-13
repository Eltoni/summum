# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='nome',
            field=models.CharField(unique=True, max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='marca',
            name='nome',
            field=models.CharField(unique=True, max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='categorias',
            field=models.ManyToManyField(to='movimento.Categoria', verbose_name='Categoria', blank=True),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
    ]
