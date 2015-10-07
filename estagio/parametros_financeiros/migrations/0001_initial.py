# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.CharField(blank=True, max_length=250, verbose_name='Descrição')),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de prazo')),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de carência')),
                ('status', models.BooleanField(help_text='Indica se a forma de pagamento está ativa para uso.', verbose_name='Status', default=True)),
            ],
            options={
                'verbose_name_plural': 'Formas de Pagamento',
                'verbose_name': 'Forma de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('multa', models.DecimalField(blank=True, max_digits=20, decimal_places=0, verbose_name='Taxa de multa (%)', null=True)),
                ('juros', models.DecimalField(blank=True, max_digits=20, decimal_places=0, verbose_name='Taxa de juros (%)', null=True)),
                ('tipo_juros', models.CharField(default='S', max_length=1, choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], verbose_name='Tipo de juros')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('padrao', models.BooleanField(help_text='Defini o Grupo de Encargo padrão', verbose_name='Padrão', default=False)),
            ],
            options={
                'verbose_name_plural': 'Grupo de Encargos',
                'verbose_name': 'Grupo de Encargo',
            },
        ),
    ]
