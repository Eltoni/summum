# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 02:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import notificacao.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anexo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo_anexo', models.FileField(upload_to='notificacao/anexo')),
            ],
            options={
                'verbose_name': 'Anexo',
                'verbose_name_plural': 'Anexos',
            },
        ),
        migrations.CreateModel(
            name='Mensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto')),
                ('assunto', models.CharField(blank=True, max_length=150, verbose_name='Assunto')),
                ('destinatario', models.TextField(blank=True, help_text='Insira uma lista de emails que receberão a mensagem (todos separados por virgula).', null=True, validators=[notificacao.validators.valida_lista_email], verbose_name='Destinatários')),
                ('destinatario_lote', models.FileField(blank=True, help_text="Forneça um arquivo csv com a coluna 'email' contendo os emails de todos os destinatários.", max_length=255, null=True, upload_to='notificacao/mensagem', validators=[notificacao.validators.valida_documento_csv], verbose_name='Destinatários em Lote')),
                ('data_envio', models.DateTimeField(db_index=True, verbose_name='Data de envio')),
                ('enviado', models.BooleanField(db_index=True, default=False, help_text='Indica se a mensagem foi enviada.', verbose_name='Enviado?')),
                ('endereco_email_enviado', models.TextField(blank=True, help_text='Lista de endereços de email para os quais a mensagem foi enviada.', null=True, verbose_name='Endereços de Email Enviados')),
            ],
            options={
                'verbose_name': 'Mensagem',
                'verbose_name_plural': 'Mensagens',
            },
        ),
        migrations.AddField(
            model_name='anexo',
            name='mensagem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Mensagem'),
        ),
    ]