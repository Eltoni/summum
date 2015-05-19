# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0003_auto_20150517_2343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargo',
            options={'verbose_name': 'Cargo', 'verbose_name_plural': 'Cargos', 'permissions': (('pode_exportar_cargo', 'Exportar Cargos'),)},
        ),
        migrations.AlterModelOptions(
            name='cliente',
            options={'permissions': (('pode_exportar_cliente', 'Exportar Clientes'),)},
        ),
        migrations.AlterModelOptions(
            name='fornecedor',
            options={'verbose_name': 'Fornecedor', 'verbose_name_plural': 'Fornecedores', 'permissions': (('pode_exportar_fornecedor', 'Exportar Fornecedores'),)},
        ),
        migrations.AlterModelOptions(
            name='funcionario',
            options={'verbose_name': 'Funcion\xe1rio', 'verbose_name_plural': 'Funcion\xe1rios', 'permissions': (('pode_exportar_funcionario', 'Exportar Funcion\xe1rios'),)},
        ),
    ]
