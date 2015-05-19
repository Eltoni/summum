# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0004_auto_20150517_2343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entregavenda',
            options={'verbose_name': 'Entrega', 'verbose_name_plural': 'Entregas', 'permissions': (('pode_exportar_entregavenda', 'Exportar Entregas'),)},
        ),
        migrations.AlterModelOptions(
            name='venda',
            options={'verbose_name': 'Venda', 'verbose_name_plural': 'Vendas', 'permissions': (('pode_exportar_venda', 'Exportar Vendas'),)},
        ),
    ]
