# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0001_initial'),
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contasreceber',
            name='vendas',
            field=models.ForeignKey(verbose_name='Venda', to='venda.Venda', on_delete=django.db.models.deletion.PROTECT, null=True),
        ),
    ]
