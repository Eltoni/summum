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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('agencia', models.CharField(verbose_name='Agência', max_length=7)),
                ('nome', models.CharField(verbose_name='Nome', max_length=75)),
                ('bairro', models.CharField(verbose_name='Bairro', blank=True, null=True, max_length=50)),
                ('estado', models.CharField(verbose_name='Estado', blank=True, null=True, max_length=2)),
                ('endereco', models.CharField(verbose_name='Endereço', blank=True, null=True, max_length=50)),
                ('numero', models.CharField(verbose_name='Número', blank=True, null=True, max_length=15)),
                ('complemento', models.CharField(verbose_name='Complemento', blank=True, null=True, max_length=50)),
                ('cep', models.CharField(verbose_name='Cep', blank=True, null=True, max_length=9)),
                ('contato', models.CharField(verbose_name='Contato', blank=True, null=True, max_length=30)),
            ],
            options={
                'verbose_name': 'Agência',
                'verbose_name_plural': 'Agências',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('banco', models.CharField(unique=True, verbose_name='Banco', max_length=10)),
                ('nome', models.CharField(verbose_name='Nome', max_length=200)),
                ('site', models.URLField(verbose_name='Site', blank=True)),
                ('logo', sorl.thumbnail.fields.ImageField(upload_to='logo_banco', verbose_name='Logo', blank=True, null=True, max_length=255)),
            ],
            options={
                'verbose_name': 'Banco',
                'verbose_name_plural': 'Bancos',
            },
        ),
        migrations.AddField(
            model_name='agencia',
            name='banco',
            field=models.ForeignKey(to='banco.Banco', verbose_name='Banco', on_delete=django.db.models.deletion.PROTECT),
        ),
        migrations.AddField(
            model_name='agencia',
            name='cidade',
            field=models.ForeignKey(to='localidade.Cidade', verbose_name='Cidade', on_delete=django.db.models.deletion.PROTECT, default='', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='agencia',
            unique_together=set([('banco', 'agencia')]),
        ),
    ]
