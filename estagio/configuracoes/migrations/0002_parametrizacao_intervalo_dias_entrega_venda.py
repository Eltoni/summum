# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracoes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametrizacao',
            name='intervalo_dias_entrega_venda',
            field=models.IntegerField(default=0, help_text='Intervalo m\xednimo entre a data de venda e a data de entrega (dias).', verbose_name='Intervalo para entrega'),
        ),
    ]
