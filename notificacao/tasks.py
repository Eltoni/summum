#-*- coding: UTF-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from celery.app.task import Task
import datetime
import logging
import smtplib

from utilitarios.funcoes_email import TextosEmail

logger = logging.getLogger(__name__)


class MensagemTask(Task):

    def run(self, obj):
        from notificacao.models import Mensagem
        obj_msg = Mensagem.objects.get(pk=obj)

        if not obj_msg.enviado:
            lista_destinatarios = obj_msg.get_lista_completa_destinatarios()
            assunto = obj_msg.assunto
            from_email = settings.DEFAULT_FROM_EMAIL
            text_content = _(u'Essa é uma mensagem importante.')
            html_content = u'%(header)s \
                             %(texto)s \
                             %(footer)s'\
                             % {'header': TextosEmail.headerEmailInterno,
                                'footer': TextosEmail.footerEmailInterno,
                                'texto': obj_msg.get_texto_formatado(),
                                }

            msg = EmailMultiAlternatives(assunto, text_content, from_email, bcc=lista_destinatarios)
            msg.attach_alternative(html_content, "text/html")

            # insere anexos caso haja algum
            for anexo in obj_msg.anexo_set.all():
                msg.attach_file(anexo.arquivo_anexo.path)

            try:
                msg.send()
                obj_msg.enviado = True
                obj_msg.endereco_email_enviado = ', '.join(msg.bcc + msg.cc + msg.to)
                obj_msg.save()
            except smtplib.SMTPException as e:
                logger.error('Exceção em fila de envios de email: {0}'.format(e))