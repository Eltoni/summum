# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=255)),
                ('estado', models.CharField(db_index=True, verbose_name='Estado', blank=True, null=True, max_length=2)),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cidade',
            unique_together=set([('nome', 'estado')]),
        ),
    ]
