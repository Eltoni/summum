# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contasreceber',
            options={'verbose_name': 'Conta a Receber', 'verbose_name_plural': 'Contas a Receber', 'permissions': (('pode_exportar_contasreceber', 'Exportar Contas a Receber'),)},
        ),
    ]
