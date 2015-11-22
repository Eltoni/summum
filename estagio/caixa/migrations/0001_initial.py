# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.')),
                ('data_abertura', models.DateTimeField(verbose_name='Data de abertura', null=True)),
                ('data_fechamento', models.DateTimeField(verbose_name='Data de fechamento', null=True)),
                ('valor_entrada', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Valor de entrada', max_digits=20)),
                ('valor_saida', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Valor de saída', max_digits=20)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Valor total', max_digits=20)),
                ('valor_inicial', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('valor_fechamento', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Valor de fechamento', max_digits=20)),
                ('diferenca', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Diferença', max_digits=20)),
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
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, verbose_name='Valor', max_digits=20)),
                ('data', models.DateTimeField(verbose_name='Data de movimento')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(to='caixa.Caixa', on_delete=django.db.models.deletion.PROTECT, verbose_name='Caixa')),
                ('pagamento', models.ForeignKey(blank=True, to='contas_pagar.Pagamento', null=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Pagamento')),
                ('recebimento', models.ForeignKey(blank=True, to='contas_receber.Recebimento', null=True, on_delete=django.db.models.deletion.PROTECT, verbose_name='Recebimento')),
            ],
            options={
                'verbose_name': 'Movimento de Caixa',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name_plural': 'Movimentos de Caixas',
            },
        ),
    ]
