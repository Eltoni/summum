# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.')),
                ('data_abertura', models.DateTimeField(help_text='Data de abertura do caixa.', verbose_name='Data de abertura', null=True)),
                ('data_fechamento', models.DateTimeField(help_text='Data de fechamento do caixa.', verbose_name='Data de fechamento', null=True)),
                ('valor_entrada', models.DecimalField(default=0.0, help_text='Somatório de todos os recebimentos (mov. do tipo Crédito).', max_digits=20, verbose_name='Valor de entrada', decimal_places=2)),
                ('valor_saida', models.DecimalField(default=0.0, help_text='Somatório de todos os pagamentos (mov. do tipo Débito).', max_digits=20, verbose_name='Valor de saída', decimal_places=2)),
                ('valor_total', models.DecimalField(default=0.0, help_text='Valor calculado automaticamente da quantia existente no Caixa em seu fechamento.', max_digits=20, verbose_name='Valor total', decimal_places=2)),
                ('valor_inicial', models.DecimalField(default=0.0, help_text='Valor existente no Caixa em sua abertura.', max_digits=20, verbose_name='Valor inicial', decimal_places=2)),
                ('valor_fechamento', models.DecimalField(default=0.0, help_text='Valor calculado manualmente da quantia existente no Caixa em seu fechamento.', max_digits=20, verbose_name='Valor de fechamento', decimal_places=2)),
                ('diferenca', models.DecimalField(default=0.0, help_text='Diferença do Valor Total calculado junto ao valor informado no fechamento do Caixa.', max_digits=20, verbose_name='Diferença', decimal_places=2)),
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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('valor', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor', decimal_places=2)),
                ('data', models.DateTimeField(verbose_name='Data de movimento')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(verbose_name='Caixa', to='caixa.Caixa', on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'verbose_name_plural': 'Movimentos de Caixas',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name': 'Movimento de Caixa',
            },
        ),
    ]
