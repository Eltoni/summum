# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movimento', '0002_auto_20150511_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produtos',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos', 'permissions': (('visualizar_rel_produtos_esgotando', 'Ver relatorio de produtos esgotando em estoque'), ('visualizar_rel_debitos_creditos_diario', 'Ver relatorio de debitos e creditos diarios'), ('visualizar_relatorios', 'Ver relatorios'), ('pode_exportar_produtos', 'Exportar Produtos'))},
        ),
    ]
