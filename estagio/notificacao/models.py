#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import pandas as pd

from notificacao.tasks import MensagemTask
from notificacao.funcoes import detecta_delimitador
from notificacao.validators import valida_lista_email, valida_documento_csv


@python_2_unicode_compatible
class Mensagem(models.Model):
    texto = models.TextField(
        verbose_name=_(u"Texto")
    )
    assunto = models.CharField(
        max_length=150, 
        blank=True, 
        verbose_name=_(u"Assunto")
    )
    destinatario = models.TextField(
        validators=[valida_lista_email],
        blank=True, 
        null=True,
        verbose_name=_(u"Destinatários"), 
        help_text=_(u"Insira uma lista de emails que receberão a mensagem (todos separados por virgula).")
    )
    destinatario_lote = models.FileField(
        validators=[valida_documento_csv],
        upload_to='notificacao/mensagem', 
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_(u"Destinatários em Lote"),
        help_text=_(u"Forneça um arquivo csv com a coluna 'email' contendo os emails de todos os destinatários.")
    )
    data_envio = models.DateTimeField(
        db_index=True, 
        verbose_name=_(u"Data de envio"),
    )
    enviado = models.BooleanField(
        default=False,
        db_index=True, 
        verbose_name=_(u"Enviado?"), 
        help_text=_(u"Indica se a mensagem foi enviada.")
    )
    endereco_email_enviado = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_(u"Endereços de Email Enviados"), 
        help_text=_(u"Lista de endereços de email para os quais a mensagem foi enviada.")
    )

    class Meta(object):
        verbose_name = _(u"Mensagem")
        verbose_name_plural = _(u"Mensagens")

    def __str__(self):
        return u'%s' % self.id

    def save(self, *args, **kwargs):
        super(Mensagem, self).save(*args, **kwargs)
        MensagemTask().apply_async(args=[self.pk], eta=self.data_envio)

    def get_destinatario(self):
        destinatarios = [email.strip() for email in self.destinatario.split(',') if email.strip()]
        return destinatarios

    def get_destinatario_lote(self):
        destinatario_lote = []
        if self.destinatario_lote:
            fp = self.destinatario_lote.path
            d = detecta_delimitador(fp)
            df = pd.read_csv(fp, delimiter=d)
            dl = df.email.tolist()

            for email in dl:
                try:
                    validate_email(email)
                    destinatario_lote.append(email)
                except ValidationError:
                    pass
        return destinatario_lote

    def get_lista_completa_destinatarios(self):
        destinatarios = self.get_destinatario()
        destinatarios_lote = self.get_destinatario_lote()
        lista_destinatarios = list(set(destinatarios)|set(destinatarios_lote))
        return lista_destinatarios


@python_2_unicode_compatible
class Anexo(models.Model):
    arquivo_anexo = models.FileField(upload_to='notificacao/anexo')
    mensagem = models.ForeignKey(Mensagem)

    class Meta(object):
        verbose_name = _('Anexo')
        verbose_name_plural = _('Anexos')

    def __str__(self):
        return self.arquivo_anexo.name