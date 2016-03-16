# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='agencia',
            field=models.ForeignKey(null=True, to='banco.Agencia', verbose_name='Agência', blank=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='banco',
            field=models.ForeignKey(null=True, to='banco.Banco', verbose_name='Banco', blank=True),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='agencia',
            field=models.ForeignKey(null=True, to='banco.Agencia', verbose_name='Agência', blank=True),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='banco',
            field=models.ForeignKey(null=True, to='banco.Banco', verbose_name='Banco', blank=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='agencia',
            field=models.ForeignKey(null=True, to='banco.Agencia', verbose_name='Agência', blank=True),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='banco',
            field=models.ForeignKey(null=True, to='banco.Banco', verbose_name='Banco', blank=True),
        ),
    ]
