# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('estado', models.CharField(blank=True, max_length=2, verbose_name='Estado', null=True)),
            ],
            options={
                'verbose_name_plural': 'Cidades',
                'verbose_name': 'Cidade',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cidade',
            unique_together=set([('nome', 'estado')]),
        ),
    ]
