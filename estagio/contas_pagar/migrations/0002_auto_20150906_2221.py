# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas_pagar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='descricao',
            field=models.TextField(verbose_name='Descrição', blank=True),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateTimeField(verbose_name='Data do pagamento', auto_now_add=True),
        ),
    ]
