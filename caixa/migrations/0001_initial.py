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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('status', models.BooleanField(verbose_name='Status', db_index=True, help_text='Desmarque o Checkbox para indicar que o caixa está fechado.', default=True)),
                ('data_abertura', models.DateTimeField(verbose_name='Data de abertura', help_text='Data de abertura do caixa.', db_index=True, null=True)),
                ('data_fechamento', models.DateTimeField(verbose_name='Data de fechamento', help_text='Data de fechamento do caixa.', db_index=True, null=True)),
                ('valor_entrada', models.DecimalField(verbose_name='Valor de entrada', decimal_places=2, help_text='Somatório de todos os recebimentos (mov. do tipo Crédito).', default=0.0, max_digits=20)),
                ('valor_saida', models.DecimalField(verbose_name='Valor de saída', decimal_places=2, help_text='Somatório de todos os pagamentos (mov. do tipo Débito).', default=0.0, max_digits=20)),
                ('valor_total', models.DecimalField(verbose_name='Valor total', decimal_places=2, help_text='Valor calculado automaticamente da quantia existente no Caixa em seu fechamento.', default=0.0, max_digits=20)),
                ('valor_inicial', models.DecimalField(verbose_name='Valor inicial', decimal_places=2, help_text='Valor existente no Caixa em sua abertura.', default=0.0, max_digits=20)),
                ('valor_fechamento', models.DecimalField(verbose_name='Valor de fechamento', decimal_places=2, help_text='Valor calculado manualmente da quantia existente no Caixa em seu fechamento.', default=0.0, max_digits=20)),
                ('diferenca', models.DecimalField(verbose_name='Diferença', decimal_places=2, help_text='Diferença do Valor Total calculado junto ao valor informado no fechamento do Caixa.', default=0.0, max_digits=20)),
            ],
            options={
                'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notificações de caixa.')),
                'verbose_name': 'Caixa',
                'verbose_name_plural': 'Caixas',
            },
        ),
        migrations.CreateModel(
            name='MovimentosCaixa',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('descricao', models.CharField(verbose_name='Descrição', max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, verbose_name='Valor', default=0.0, max_digits=20)),
                ('data', models.DateTimeField(db_index=True, verbose_name='Data de movimento')),
                ('tipo_mov', models.CharField(db_index=True, verbose_name='Tipo de movimento', max_length=45)),
                ('caixa', models.ForeignKey(to='caixa.Caixa', verbose_name='Caixa', on_delete=django.db.models.deletion.PROTECT)),
                ('pagamento', models.ForeignKey(to='contas_pagar.Pagamento', verbose_name='Pagamento', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT)),
                ('recebimento', models.ForeignKey(to='contas_receber.Recebimento', verbose_name='Recebimento', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT)),
            ],
            options={
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name': 'Movimento de Caixa',
                'verbose_name_plural': 'Movimentos de Caixas',
            },
        ),
    ]
