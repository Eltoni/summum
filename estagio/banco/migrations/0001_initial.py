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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('agencia', models.CharField(verbose_name='Agência', max_length=7)),
                ('nome', models.CharField(verbose_name='Nome', max_length=75)),
                ('bairro', models.CharField(blank=True, verbose_name='Bairro', null=True, max_length=50)),
                ('estado', models.CharField(blank=True, verbose_name='Estado', null=True, max_length=2)),
                ('endereco', models.CharField(blank=True, verbose_name='Endereço', null=True, max_length=50)),
                ('numero', models.CharField(blank=True, verbose_name='Número', null=True, max_length=15)),
                ('complemento', models.CharField(blank=True, verbose_name='Complemento', null=True, max_length=50)),
                ('cep', models.CharField(blank=True, verbose_name='Cep', null=True, max_length=9)),
                ('contato', models.CharField(blank=True, verbose_name='Contato', null=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Agências',
                'verbose_name': 'Agência',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('banco', models.CharField(unique=True, verbose_name='Banco', max_length=10)),
                ('nome', models.CharField(verbose_name='Nome', max_length=200)),
                ('site', models.URLField(blank=True, verbose_name='Site')),
                ('logo', sorl.thumbnail.fields.ImageField(blank=True, upload_to='logo_banco', verbose_name='Logo', null=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Bancos',
                'verbose_name': 'Banco',
            },
        ),
        migrations.AddField(
            model_name='agencia',
            name='banco',
            field=models.ForeignKey(to='banco.Banco', on_delete=django.db.models.deletion.PROTECT, verbose_name='Banco'),
        ),
        migrations.AddField(
            model_name='agencia',
            name='cidade',
            field=models.ForeignKey(to='localidade.Cidade', blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade', default='', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='agencia',
            unique_together=set([('banco', 'agencia')]),
        ),
    ]
