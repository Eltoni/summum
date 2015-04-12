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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100, verbose_name='Name')),
                ('descricao', models.CharField(max_length=250, verbose_name='Descri\xe7\xe3o', blank=True)),
                ('quant_parcelas', models.IntegerField(verbose_name='Quantidade de parcelas')),
                ('prazo_entre_parcelas', models.IntegerField(verbose_name='Prazo entre parcelas')),
                ('tipo_prazo', models.CharField(blank=True, max_length=1, verbose_name='Tipo de prazo', choices=[('D', 'Di\xe1rio'), ('S', 'Semanal'), ('M', 'Mensal')])),
                ('carencia', models.IntegerField(verbose_name='Car\xeancia')),
                ('tipo_carencia', models.CharField(blank=True, max_length=1, verbose_name='Tipo de car\xeancia', choices=[('D', 'Di\xe1rio'), ('S', 'Semanal'), ('M', 'Mensal')])),
                ('status', models.BooleanField(default=True, help_text='Indica se a forma de pagamento est\xe1 ativa para uso.', verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Forma de Pagamento',
                'verbose_name_plural': 'Formas de Pagamento',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrupoEncargo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('multa', models.DecimalField(null=True, verbose_name='Taxa de multa (%)', max_digits=20, decimal_places=0, blank=True)),
                ('juros', models.DecimalField(null=True, verbose_name='Taxa de juros (%)', max_digits=20, decimal_places=0, blank=True)),
                ('tipo_juros', models.CharField(default=b'S', max_length=1, verbose_name='Tipo de juros', choices=[(b'S', 'Juros Simples'), (b'C', 'Juros Compostos')])),
                ('status', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('padrao', models.BooleanField(default=False, help_text='Defini o Grupo de Encargo padr\xe3o', verbose_name='Padr\xe3o')),
            ],
            options={
                'verbose_name': 'Grupo de Encargo',
                'verbose_name_plural': 'Grupo de Encargos',
            },
            bases=(models.Model,),
        ),
    ]
