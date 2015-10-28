# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='status',
            field=models.BooleanField(help_text='Indica se o status da compra está ativo ou cancelada.', default=False, verbose_name='Cancelado?'),
        ),
        migrations.AlterField(
            model_name='itenscompra',
            name='quantidade',
            field=models.IntegerField(verbose_name='Quantidade'),
        ),
    ]
