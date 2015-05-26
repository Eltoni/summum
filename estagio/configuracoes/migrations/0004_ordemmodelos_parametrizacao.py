# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0003_ordemmodelos'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemmodelos',
            name='parametrizacao',
            field=models.ForeignKey(to='configuracoes.Parametrizacao', on_delete=django.db.models.deletion.PROTECT, null=True),
        ),
    ]
