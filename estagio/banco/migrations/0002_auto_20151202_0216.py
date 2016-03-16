# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencia',
            name='cidade',
            field=models.ForeignKey(blank=True, verbose_name='Cidade', default='', to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, null=True),
        ),
    ]
