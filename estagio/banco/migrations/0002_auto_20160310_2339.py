# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencia',
            name='complemento',
            field=models.CharField(blank=True, verbose_name='Complemento', max_length=50),
        ),
        migrations.AddField(
            model_name='banco',
            name='email',
            field=models.EmailField(blank=True, verbose_name='E-mail', max_length=100),
        ),
    ]
