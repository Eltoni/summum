# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0002_parametrizacao_email_abertura_caixa'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdemModelos',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('campo', models.CharField(max_length=50)),
                ('classe', models.CharField(max_length=50)),
                ('ordem', models.PositiveIntegerField(default=0)),
                ('permite_exportar', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Ordenação do modelo',
                'verbose_name_plural': 'Ordenações dos modelos',
            },
        ),
    ]
