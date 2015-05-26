# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0004_ordemmodelos_parametrizacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemmodelos',
            name='exibe_listagem_principal',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ordemmodelos',
            name='permite_exportar',
            field=models.BooleanField(default=False),
        ),
    ]
