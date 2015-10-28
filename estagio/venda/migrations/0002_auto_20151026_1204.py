# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='status',
            field=models.BooleanField(help_text='Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.', default=False, verbose_name='Cancelado?'),
        ),
    ]
