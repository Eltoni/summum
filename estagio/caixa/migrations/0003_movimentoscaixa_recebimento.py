# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0002_movimentoscaixa_pagamento'),
        ('contas_receber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentoscaixa',
            name='recebimento',
            field=models.ForeignKey(blank=True, verbose_name='Recebimento', to='contas_receber.Recebimento', null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
