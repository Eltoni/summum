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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=255, verbose_name='Name')),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('ultima_alteracao', models.DateTimeField(auto_now=True, verbose_name='\xdaltima altera\xe7\xe3o')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='cidade',
            unique_together=set([('nome', 'estado')]),
        ),
    ]
