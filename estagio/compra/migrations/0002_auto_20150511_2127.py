# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='status',
            field=models.BooleanField(default=False, help_text='Indica se o status da compra est\xe1 ativo ou cancelada.', verbose_name='Cancelada?'),
        ),
        migrations.AlterField(
            model_name='compra',
            name='status_pedido',
            field=models.BooleanField(default=False, help_text='Caso confirmado, os itens financeiros ser\xe3o gerados e o estoque movimentado.', verbose_name='Pedido confirmado?'),
        ),
    ]
