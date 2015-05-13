# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0002_auto_20150511_2127'),
        ('venda', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntregaVenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.DateTimeField(null=True, verbose_name='Data de entrega', blank=True)),
                ('observacao', models.TextField(help_text='Descreva na \xe1rea as informa\xe7\xf5es relavantes da entrega.', verbose_name='Observa\xe7\xf5es', blank=True)),
                ('posicao', geoposition.fields.GeopositionField(max_length=42, verbose_name='Posi\xe7\xe3o', blank=True)),
                ('endereco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Endere\xe7o', blank=True, to='pessoal.EnderecoEntregaCliente', null=True)),
            ],
            options={
                'verbose_name': 'Entrega',
                'verbose_name_plural': 'Entregas',
            },
        ),
        migrations.AlterField(
            model_name='venda',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Cliente', to='pessoal.Cliente'),
        ),
        migrations.AddField(
            model_name='entregavenda',
            name='venda',
            field=models.OneToOneField(null=True, blank=True, to='venda.Venda', verbose_name='Venda'),
        ),
    ]
