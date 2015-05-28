# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0002_auto_20150524_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='enderecoentregacliente',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='cidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='localidade.Cidade', verbose_name='Cidade'),
        ),
    ]
