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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('descricao', models.CharField(blank=True, max_length=250, verbose_name='Descrição')),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], blank=True, max_length=1, verbose_name='Tipo de prazo')),
                ('carencia', models.IntegerField(verbose_name='Carência')),
                ('tipo_carencia', models.CharField(choices=[('D', 'Diário'), ('S', 'Semanal'), ('M', 'Mensal')], blank=True, max_length=1, verbose_name='Tipo de carência')),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Indica se a forma de pagamento está ativa para uso.')),
            ],
            options={
                'verbose_name_plural': 'Formas de Pagamento',
                'verbose_name': 'Forma de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('multa', models.DecimalField(max_digits=20, null=True, decimal_places=0, verbose_name='Taxa de multa (%)', blank=True)),
                ('juros', models.DecimalField(max_digits=20, null=True, decimal_places=0, verbose_name='Taxa de juros (%)', blank=True)),
                ('tipo_juros', models.CharField(choices=[('S', 'Juros Simples'), ('C', 'Juros Compostos')], max_length=1, default='S', verbose_name='Tipo de juros')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('padrao', models.BooleanField(default=False, verbose_name='Padrão', help_text='Defini o Grupo de Encargo padrão')),
            ],
            options={
                'verbose_name_plural': 'Grupo de Encargos',
                'verbose_name': 'Grupo de Encargo',
            },
        ),
    ]
