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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.CharField(verbose_name='Descrição', blank=True, max_length=250)),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(verbose_name='Tipo de prazo', blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')])),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(verbose_name='Tipo de carência', blank=True, max_length=1, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')])),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Indica se a forma de pagamento está ativa para uso.')),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
                ('multa', models.DecimalField(verbose_name='Taxa de multa (%)', null=True, decimal_places=0, max_digits=20, blank=True)),
                ('juros', models.DecimalField(verbose_name='Taxa de juros (%)', null=True, decimal_places=0, max_digits=20, blank=True)),
                ('tipo_juros', models.CharField(default='S', verbose_name='Tipo de juros', max_length=1, choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')])),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('padrao', models.BooleanField(default=False, verbose_name='Padrão', help_text='Defini o Grupo de Encargo padrão')),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
        ),
    ]
