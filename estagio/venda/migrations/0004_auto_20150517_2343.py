# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0003_entregavenda_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregavenda',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Entrega agendada?'),
        ),
    ]
