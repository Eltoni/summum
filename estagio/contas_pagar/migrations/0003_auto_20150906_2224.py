# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas_pagar', '0002_auto_20150906_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagamento',
            name='descricao',
        ),
        migrations.AddField(
            model_name='pagamento',
            name='observacao',
            field=models.TextField(verbose_name='Observações', blank=True),
        ),
    ]
