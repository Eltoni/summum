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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('estado', models.CharField(max_length=2, verbose_name='Estado', blank=True, null=True)),
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
