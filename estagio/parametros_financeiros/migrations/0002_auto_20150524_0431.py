# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parametros_financeiros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoencargo',
            name='tipo_juros',
            field=models.CharField(default='S', max_length=1, verbose_name='Tipo de juros', choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')]),
        ),
    ]
