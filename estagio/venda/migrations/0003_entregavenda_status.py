# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0002_auto_20150511_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregavenda',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Tem entrega?'),
        ),
    ]
