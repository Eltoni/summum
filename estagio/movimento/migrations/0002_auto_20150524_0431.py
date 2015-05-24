# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(max_length=255, blank=True, upload_to='marcas', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='imagem',
            field=sorl.thumbnail.fields.ImageField(max_length=255, blank=True, upload_to='produtos', verbose_name='Imagem'),
        ),
    ]
