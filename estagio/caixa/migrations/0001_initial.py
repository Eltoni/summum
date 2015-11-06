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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('status', models.BooleanField(default=True, verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.')),
                ('data_abertura', models.DateTimeField(null=True, verbose_name='Data de abertura')),
                ('data_fechamento', models.DateTimeField(null=True, verbose_name='Data de fechamento')),
                ('valor_entrada', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Valor de entrada')),
                ('valor_saida', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Valor de saída')),
                ('valor_total', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Valor total')),
                ('valor_inicial', models.DecimalField(max_digits=20, decimal_places=2, default=0.0)),
                ('valor_fechamento', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Valor de fechamento')),
                ('diferenca', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Diferença')),
            ],
            options={
                'permissions': (('pode_exportar_caixa', 'Exportar Caixas'), ('recebe_notificacoes_caixa', 'Receber notificações de caixa.')),
                'verbose_name_plural': 'Caixas',
                'verbose_name': 'Caixa',
            },
        ),
        migrations.CreateModel(
            name='MovimentosCaixa',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('valor', models.DecimalField(max_digits=20, decimal_places=2, default=0.0, verbose_name='Valor')),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='caixa.Caixa', verbose_name='Caixa')),
                ('pagamento', models.ForeignKey(null=True, to='contas_pagar.Pagamento', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Pagamento')),
                ('recebimento', models.ForeignKey(null=True, to='contas_receber.Recebimento', on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Recebimento')),
            ],
            options={
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name_plural': 'Movimentos de Caixas',
                'verbose_name': 'Movimento de Caixa',
            },
        ),
    ]
