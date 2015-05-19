# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0002_auto_20150511_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compra',
            options={'verbose_name': 'Compra', 'verbose_name_plural': 'Compras', 'permissions': (('pode_exportar_compra', 'Exportar Compras'),)},
        ),
    ]
