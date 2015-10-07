# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametrizacao',
            name='evento_calendario',
            field=models.CharField(verbose_name='Calendário de eventos', choices=[('eventos', 'Eventos')], null=True, help_text='Defina o calendário de eventos que aparecerão no dashboard do sistema.', max_length=200),
        ),
    ]
