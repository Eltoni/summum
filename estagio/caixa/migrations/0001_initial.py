# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_pagar', '0001_initial'),
        ('contas_receber', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=True, help_text='Desmarque o Checkbox para indicar que o caixa est\xe1 fechado.', verbose_name='Status')),
                ('data_abertura', models.DateTimeField(null=True, verbose_name='Data de abertura')),
                ('data_fechamento', models.DateTimeField(null=True, verbose_name='Data de fechamento')),
                ('valor_entrada', models.DecimalField(default=0.0, verbose_name='Valor de entrada', max_digits=20, decimal_places=2)),
                ('valor_saida', models.DecimalField(default=0.0, verbose_name='Valor de sa\xedda', max_digits=20, decimal_places=2)),
                ('valor_total', models.DecimalField(default=0.0, verbose_name='Valor total', max_digits=20, decimal_places=2)),
                ('valor_inicial', models.DecimalField(default=0.0, max_digits=20, decimal_places=2)),
                ('valor_fechamento', models.DecimalField(default=0.0, verbose_name='Valor de fechamento', max_digits=20, decimal_places=2)),
                ('diferenca', models.DecimalField(default=0.0, verbose_name='Diferen\xe7a', max_digits=20, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Caixa',
                'verbose_name_plural': 'Caixas',
                'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notifica\xe7\xf5es de caixa.')),
            },
        ),
        migrations.CreateModel(
            name='MovimentosCaixa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descricao', models.CharField(max_length=100, verbose_name='Descri\xe7\xe3o')),
                ('valor', models.CharField(max_length=45, verbose_name='Valor')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Caixa', to='caixa.Caixa')),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Pagamento', blank=True, to='contas_pagar.Pagamento', null=True)),
                ('recebimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento', blank=True, to='contas_receber.Recebimento', null=True)),
            ],
            options={
                'verbose_name': 'Movimento de Caixa',
                'verbose_name_plural': 'Movimentos de Caixas',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
            },
        ),
    ]
