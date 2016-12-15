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
                ('quant_parcelas', models.IntegerField(db_index=True, verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(db_index=True, verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(db_index=True, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de prazo', blank=True, max_length=1)),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(db_index=True, choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], verbose_name='Tipo de carência', blank=True, max_length=1)),
                ('status', models.BooleanField(verbose_name='Status', db_index=True, help_text='Indica se a forma de pagamento está ativa para uso.', default=True)),
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
                ('multa', models.DecimalField(max_digits=7, decimal_places=4, verbose_name='Taxa de multa (%)', blank=True, null=True)),
                ('juros', models.DecimalField(verbose_name='Taxa de juros (%)', max_digits=7, help_text='Juros que serão calculados diariamente.', decimal_places=4, blank=True, null=True)),
                ('tipo_juros', models.CharField(db_index=True, choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], verbose_name='Tipo de juros', default='S', max_length=1)),
                ('status', models.BooleanField(db_index=True, verbose_name='Status', default=True)),
                ('padrao', models.BooleanField(verbose_name='Padrão', db_index=True, help_text='Define o Grupo de Encargo padrão', default=False)),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
        ),
    ]
