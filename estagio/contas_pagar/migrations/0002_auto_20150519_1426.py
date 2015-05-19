# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas_pagar', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contaspagar',
            options={'verbose_name': 'Conta a Pagar', 'verbose_name_plural': 'Contas a Pagar', 'permissions': (('pode_exportar_contaspagar', 'Exportar Contas a Pagar'),)},
        ),
    ]
