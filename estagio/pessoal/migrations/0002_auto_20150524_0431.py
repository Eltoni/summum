# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import smart_selects.db_fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cidade',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='estado', chained_field='estado', auto_choose=True, to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado_civil',
            field=models.CharField(max_length=30, verbose_name='Estado Civil', blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='foto',
            field=sorl.thumbnail.fields.ImageField(max_length=255, blank=True, upload_to='fotos_pessoas', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='sexo',
            field=models.CharField(max_length=1, null=True, verbose_name='Sexo', blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_pessoa',
            field=models.CharField(default='PF', max_length=2, verbose_name='Tipo pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')]),
        ),
        migrations.AlterField(
            model_name='enderecoentregacliente',
            name='cidade',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='estado', chained_field='estado', auto_choose=True, to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='cidade',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='estado', chained_field='estado', auto_choose=True, to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='estado_civil',
            field=models.CharField(max_length=30, verbose_name='Estado Civil', blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')]),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='foto',
            field=sorl.thumbnail.fields.ImageField(max_length=255, blank=True, upload_to='fotos_pessoas', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='sexo',
            field=models.CharField(max_length=1, null=True, verbose_name='Sexo', blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='tipo_pessoa',
            field=models.CharField(default='PF', max_length=2, verbose_name='Tipo pessoa', choices=[('PF', 'Pessoa Física'), ('PJ', 'Pessoa Jurídica')]),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='cidade',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field='estado', chained_field='estado', auto_choose=True, to='localidade.Cidade', on_delete=django.db.models.deletion.PROTECT, verbose_name='Cidade'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='estado_civil',
            field=models.CharField(max_length=30, verbose_name='Estado Civil', blank=True, choices=[('solteiro', 'Solteiro'), ('casado', 'Casado'), ('separado', 'Separado'), ('viuvo', 'Viuvo'), ('divorciado', 'Divorciado'), ('marital', 'Marital'), ('separado_judicialmente', 'Separado Judicialmente'), ('separado_concensualmente', 'Separado Concensualmente'), ('uniao_estavel', 'União Estável')]),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='foto',
            field=sorl.thumbnail.fields.ImageField(max_length=255, blank=True, upload_to='fotos_pessoas', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='sexo',
            field=models.CharField(max_length=1, null=True, verbose_name='Sexo', blank=True, choices=[('M', 'Masculino'), ('F', 'Feminino')]),
        ),
    ]
