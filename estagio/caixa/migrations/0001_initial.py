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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(help_text='Desmarque o Checkbox para indicar que o caixa está fechado.', verbose_name='Status', default=True)),
                ('data_abertura', models.DateTimeField(verbose_name='Data de abertura', null=True)),
                ('data_fechamento', models.DateTimeField(verbose_name='Data de fechamento', null=True)),
                ('valor_entrada', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Valor de entrada')),
                ('valor_saida', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Valor de saída')),
                ('valor_total', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Valor total')),
                ('valor_inicial', models.DecimalField(max_digits=20, default=0.0, decimal_places=2)),
                ('valor_fechamento', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Valor de fechamento')),
                ('diferenca', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Diferença')),
            ],
            options={
                'verbose_name_plural': 'Caixas',
                'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notificações de caixa.')),
                'verbose_name': 'Caixa',
            },
        ),
        migrations.CreateModel(
            name='MovimentosCaixa',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('valor', models.DecimalField(max_digits=20, default=0.0, decimal_places=2, verbose_name='Valor')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(verbose_name='Caixa', on_delete=django.db.models.deletion.PROTECT, to='caixa.Caixa')),
                ('pagamento', models.ForeignKey(verbose_name='Pagamento', null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to='contas_pagar.Pagamento')),
                ('recebimento', models.ForeignKey(verbose_name='Recebimento', null=True, blank=True, on_delete=django.db.models.deletion.PROTECT, to='contas_receber.Recebimento')),
            ],
            options={
                'verbose_name_plural': 'Movimentos de Caixas',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name': 'Movimento de Caixa',
            },
        ),
    ]
