# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0002_auto_20150511_2127'),
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnderecoEntregaCliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('endereco', models.CharField(max_length=50, verbose_name='Endere\xe7o')),
                ('numero', models.CharField(max_length=15, verbose_name='N\xfamero')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro')),
                ('complemento', models.CharField(max_length=50, verbose_name='Complemento', blank=True)),
                ('estado', models.CharField(max_length=2, null=True, verbose_name='Estado', blank=True)),
                ('cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('observacao', models.TextField(verbose_name='Observa\xe7\xf5es', blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'estado', on_delete=django.db.models.deletion.PROTECT, chained_field=b'estado', verbose_name='Cidade', auto_choose=True, to='localidade.Cidade')),
            ],
            options={
                'verbose_name': 'Endere\xe7o de Entrega',
                'verbose_name_plural': 'Endere\xe7os de Entrega',
            },
        ),
        migrations.AlterField(
            model_name='cargo',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='nome',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='usuario',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Usu\xe1rio'),
        ),
        migrations.AddField(
            model_name='enderecoentregacliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente'),
        ),
    ]
