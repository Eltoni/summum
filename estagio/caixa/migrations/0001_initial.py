# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_receber', '__first__'),
        ('contas_pagar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Caixa',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('status', models.BooleanField(verbose_name='Status', help_text='Desmarque o Checkbox para indicar que o caixa está fechado.', default=True)),
                ('data_abertura', models.DateTimeField(null=True, verbose_name='Data de abertura')),
                ('data_fechamento', models.DateTimeField(null=True, verbose_name='Data de fechamento')),
                ('valor_entrada', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor de entrada', default=0.0)),
                ('valor_saida', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor de saída', default=0.0)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor total', default=0.0)),
                ('valor_inicial', models.DecimalField(decimal_places=2, max_digits=20, default=0.0)),
                ('valor_fechamento', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor de fechamento', default=0.0)),
                ('diferenca', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Diferença', default=0.0)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Valor', default=0.0)),
                ('data', models.DateTimeField(verbose_name='Data')),
                ('tipo_mov', models.CharField(max_length=45, verbose_name='Tipo de movimento')),
                ('caixa', models.ForeignKey(verbose_name='Caixa', on_delete=django.db.models.deletion.PROTECT, to='caixa.Caixa')),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Pagamento', null=True, to='contas_pagar.Pagamento')),
                ('recebimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, verbose_name='Recebimento', null=True, to='contas_receber.Recebimento')),
            ],
            options={
                'verbose_name_plural': 'Movimentos de Caixas',
                'permissions': (('pode_exportar_movimentoscaixa', 'Exportar Movimentos de Caixas'),),
                'verbose_name': 'Movimento de Caixa',
            },
        ),
    ]
