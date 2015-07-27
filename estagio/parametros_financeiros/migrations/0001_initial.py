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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.CharField(blank=True, max_length=250, verbose_name='Descrição')),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de prazo')),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de carência')),
                ('status', models.BooleanField(verbose_name='Status', help_text='Indica se a forma de pagamento está ativa para uso.', default=True)),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100, unique=True)),
                ('multa', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0, verbose_name='Taxa de multa (%)')),
                ('juros', models.DecimalField(blank=True, null=True, max_digits=20, decimal_places=0, verbose_name='Taxa de juros (%)')),
                ('tipo_juros', models.CharField(verbose_name='Tipo de juros', max_length=1, choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], default='S')),
                ('status', models.BooleanField(verbose_name='Status', default=True)),
                ('padrao', models.BooleanField(verbose_name='Padrão', help_text='Defini o Grupo de Encargo padrão', default=False)),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
        ),
    ]
