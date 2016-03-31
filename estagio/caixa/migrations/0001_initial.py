# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.')),
                ('data_abertura', models.DateTimeField(verbose_name='Data de abertura', null=True, help_text='Data de abertura do caixa.')),
                ('data_fechamento', models.DateTimeField(verbose_name='Data de fechamento', null=True, help_text='Data de fechamento do caixa.')),
                ('valor_entrada', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor de entrada', decimal_places=2, help_text='Somatório de todos os recebimentos (mov. do tipo Crédito).')),
                ('valor_saida', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor de saída', decimal_places=2, help_text='Somatório de todos os pagamentos (mov. do tipo Débito).')),
                ('valor_total', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor total', decimal_places=2, help_text='Valor calculado automaticamente da quantia existente no Caixa em seu fechamento.')),
                ('valor_inicial', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor inicial', decimal_places=2, help_text='Valor existente no Caixa em sua abertura.')),
                ('valor_fechamento', models.DecimalField(default=0.0, max_digits=20, verbose_name='Valor de fechamento', decimal_places=2, help_text='Valor calculado manualmente da quantia existente no Caixa em seu fechamento.')),
                ('diferenca', models.DecimalField(default=0.0, max_digits=20, verbose_name='Diferença', decimal_places=2, help_text='Diferença do Valor Total calculado junto ao valor informado no fechamento do Caixa.')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('descricao', models.CharField(verbose_name='Descrição', max_length=100)),
                ('valor', models.DecimalField(default=0.0, verbose_name='Valor', decimal_places=2, max_digits=20)),
                ('data', models.DateTimeField(verbose_name='Data de movimento')),
                ('tipo_mov', models.CharField(verbose_name='Tipo de movimento', max_length=45)),
                ('caixa', models.ForeignKey(to='caixa.Caixa', on_delete=django.db.models.deletion.PROTECT, verbose_name='Caixa')),
                ('pagamento', models.ForeignKey(to='contas_pagar.Pagamento', blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Pagamento', null=True)),
                ('recebimento', models.ForeignKey(to='contas_receber.Recebimento', blank=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento', null=True)),
            ],
            options={
                'verbose_name_plural': 'Movimentos de Caixas',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name': 'Movimento de Caixa',
            },
        ),
    ]
