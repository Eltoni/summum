# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0001_initial'),
        ('caixa', '0002_movimentoscaixa_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentoscaixa',
            name='recebimento',
            field=models.ForeignKey(to='contas_receber.Recebimento', verbose_name='Recebimento', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
