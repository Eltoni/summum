# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venda', '0005_auto_20150519_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='vendedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, verbose_name='Vendedor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
