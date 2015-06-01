# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '0001_initial'),
        ('contas_pagar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.')),
                ('data_abertura', models.DateTimeField(verbose_name='Data de abertura', null=True)),
                ('data_fechamento', models.DateTimeField(verbose_name='Data de fechamento', null=True)),
                ('valor_entrada', models.DecimalField(default=0.0, verbose_name='Valor de entrada', decimal_places=2, max_digits=20)),
                ('valor_saida', models.DecimalField(default=0.0, verbose_name='Valor de saída', decimal_places=2, max_digits=20)),
                ('valor_total', models.DecimalField(default=0.0, verbose_name='Valor total', decimal_places=2, max_digits=20)),
                ('valor_inicial', models.DecimalField(default=0.0, decimal_places=2, max_digits=20)),
                ('valor_fechamento', models.DecimalField(default=0.0, verbose_name='Valor de fechamento', decimal_places=2, max_digits=20)),
                ('diferenca', models.DecimalField(default=0.0, verbose_name='Diferença', decimal_places=2, max_digits=20)),
            ],
            options={
                'verbose_name': 'Caixa',
                'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notificações de caixa.')),
                'verbose_name_plural': 'Caixas',
            },
        ),
        migrations.CreateModel(
            name='MovimentosCaixa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('descricao', models.CharField(verbose_name='Descrição', max_length=100)),
                ('valor', models.CharField(verbose_name='Valor', max_length=45)),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('tipo_mov', models.CharField(verbose_name='Tipo de movimento', max_length=45)),
                ('caixa', models.ForeignKey(to='caixa.Caixa', verbose_name='Caixa', on_delete=django.db.models.deletion.PROTECT)),
                ('pagamento', models.ForeignKey(to='contas_pagar.Pagamento', null=True, verbose_name='Pagamento', blank=True, on_delete=django.db.models.deletion.PROTECT)),
                ('recebimento', models.ForeignKey(to='contas_receber.Recebimento', null=True, verbose_name='Recebimento', blank=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name': 'Movimento de Caixa',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name_plural': 'Movimentos de Caixas',
            },
        ),
    ]
