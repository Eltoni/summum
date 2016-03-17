# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0005_auto_20160311_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencia',
            name='complemento',
            field=models.CharField(blank=True, max_length=50, verbose_name='Complemento', null=True),
        ),
        migrations.AlterField(
            model_name='banco',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(blank=True, max_length=255, verbose_name='Logo', default=False, upload_to='logo_banco'),
        ),
    ]
