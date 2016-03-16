# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localidade', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencia',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('agencia', models.CharField(verbose_name='Agência', max_length=7)),
                ('nome', models.CharField(verbose_name='Nome', max_length=50)),
                ('bairro', models.CharField(blank=True, null=True, verbose_name='Bairro', max_length=50)),
                ('estado', models.CharField(blank=True, null=True, verbose_name='Estado', max_length=2)),
                ('endereco', models.CharField(blank=True, null=True, verbose_name='Endereço', max_length=50)),
                ('numero', models.CharField(blank=True, null=True, verbose_name='Número', max_length=15)),
                ('cep', models.CharField(blank=True, null=True, verbose_name='Cep', max_length=9)),
                ('contato', models.CharField(blank=True, null=True, verbose_name='Contato', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Agências',
                'verbose_name': 'Agência',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('banco', models.IntegerField(unique=True, verbose_name='Banco')),
                ('nome', models.CharField(verbose_name='Nome', max_length=200)),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, upload_to='logo_banco', verbose_name='Logo', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Bancos',
                'verbose_name': 'Banco',
            },
        ),
        migrations.AddField(
            model_name='agencia',
            name='banco',
            field=models.ForeignKey(verbose_name='Banco', on_delete=django.db.models.deletion.PROTECT, to='banco.Banco'),
        ),
        migrations.AddField(
            model_name='agencia',
            name='cidade',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, null=True, to='localidade.Cidade', verbose_name='Cidade', default=''),
        ),
        migrations.AlterUniqueTogether(
            name='agencia',
            unique_together=set([('banco', 'agencia')]),
        ),
    ]
