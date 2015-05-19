# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caixa', '0002_auto_20150511_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caixa',
            options={'verbose_name': 'Caixa', 'verbose_name_plural': 'Caixas', 'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notifica\xe7\xf5es de caixa.'))},
        ),
        migrations.AlterModelOptions(
            name='movimentoscaixa',
            options={'verbose_name': 'Movimento de Caixa', 'verbose_name_plural': 'Movimentos de Caixas', 'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),)},
        ),
    ]
