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
            name='email_abertura_caixa',
            field=models.TextField(help_text='Insira uma mensagem customizada. Esta ser\xe1 exibida acima do rodap\xe9 no email de abertura do caixa.', verbose_name='Email de abertura de caixa', blank=True),
        ),
    ]
