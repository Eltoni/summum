# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.CharField(verbose_name='Descrição', blank=True, max_length=250)),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de prazo', blank=True, max_length=1)),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de carência', blank=True, max_length=1)),
                ('status', models.BooleanField(default=True, help_text='Indica se a forma de pagamento está ativa para uso.', verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
                ('multa', models.DecimalField(null=True, decimal_places=0, verbose_name='Taxa de multa (%)', blank=True, max_digits=20)),
                ('juros', models.DecimalField(null=True, decimal_places=0, verbose_name='Taxa de juros (%)', blank=True, max_digits=20)),
                ('tipo_juros', models.CharField(choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], default='S', verbose_name='Tipo de juros', max_length=1)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('padrao', models.BooleanField(default=False, help_text='Defini o Grupo de Encargo padrão', verbose_name='Padrão')),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
        ),
    ]
