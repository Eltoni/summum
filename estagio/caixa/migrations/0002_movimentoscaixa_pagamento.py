# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas_pagar', '0001_initial'),
        ('caixa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentoscaixa',
            name='pagamento',
            field=models.ForeignKey(to='contas_pagar.Pagamento', verbose_name='Pagamento', blank=True, null=True, on_delete=django.db.models.deletion.PROTECT),
        ),
    ]
