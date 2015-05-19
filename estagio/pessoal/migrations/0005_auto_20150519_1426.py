# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0004_auto_20150519_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes', 'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),)},
        ),
    ]
