# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('banco', '0008_auto_20160313_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banco',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, verbose_name='Logo', max_length=255, upload_to='logo_banco'),
        ),
    ]
