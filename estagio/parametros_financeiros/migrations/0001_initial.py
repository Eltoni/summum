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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(verbose_name='Nome', max_length=100)),
                ('descricao', models.CharField(verbose_name='Descrição', blank=True, max_length=250)),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], blank=True, verbose_name='Tipo de prazo', max_length=1)),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], blank=True, verbose_name='Tipo de carência', max_length=1)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('nome', models.CharField(unique=True, verbose_name='Nome', max_length=100)),
                ('multa', models.DecimalField(null=True, verbose_name='Taxa de multa (%)', blank=True, decimal_places=4, max_digits=7)),
                ('juros', models.DecimalField(null=True, help_text='Juros que serão calculados diariamente.', max_digits=7, verbose_name='Taxa de juros (%)', blank=True, decimal_places=4)),
                ('tipo_juros', models.CharField(default='S', choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], verbose_name='Tipo de juros', max_length=1)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('padrao', models.BooleanField(default=False, verbose_name='Padrão', help_text='Define o Grupo de Encargo padrão')),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
        ),
    ]
