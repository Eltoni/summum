#-*- coding: UTF-8 -*-
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.validators import validate_email
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

import csv
import os


# usado para mapear cabeçalhos csv e campos de localização
HEADERS = {
    'email': {'field':'email', 'required':True},
    # 'platinum_member': {'field':'platinum_member', 'required':False},
}

def valida_documento_csv(document):
    """
        Checa se formato de arquivo csv é válido.
        Os campos obrigatórios que devem conter o arquivo são especificados no dicionário HEADERS.

        Fontes: http://blog.jeremyaldrich.net/en/latest/django_filefield_csv_validation.html
                http://blog.hayleyanderson.us/2015/07/18/validating-file-types-in-django/

    """
    
    # Ao salvar um arquivo pela primeira vez, este ainda não encontra-se em disco.
    # Por isso o bloco abaixo checa se é possível encontrar o arquivo salvo no diretório padrão.
    # caso não seja, o arquivo é salvo em um diretório temporário.
    try:
        open(document.path)
        file_saved = document.path
    except IOError:
        tmp_path = 'notificacao/mensagem/tmp/%s' % document.name
        file_saved = default_storage.save(tmp_path, ContentFile(document.file.read()))
        file_saved = os.path.join(settings.MEDIA_ROOT, file_saved)

    try:
        with open(file_saved) as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0, 0)
    except csv.Error:
        raise ValidationError(_(u'Não é um arquivo csv válido!'))

    with open(file_saved) as f:
        reader = csv.reader(f.read().splitlines(), dialect)

    csv_headers = []
    required_headers = [header_name for header_name, values in
                        HEADERS.items() if values['required']]
    for y_index, row in enumerate(reader):
        # check that all headers are present
        if y_index == 0:
            # store header_names to sanity check required cells later
            csv_headers = [header_name.lower() for header_name in row if header_name]
            missing_headers = set(required_headers) - set([r.lower() for r in row])
            if missing_headers:
                missing_headers_str = ', '.join(missing_headers)
                raise ValidationError(_(u'Faltando cabeçalhos: %s.') % (missing_headers_str))
            continue
        # ignore blank rows
        if not ''.join(str(x) for x in row):
            continue
        # sanity check required cell values
        for x_index, cell_value in enumerate(row):
            # if indexerror, probably an empty cell past the headers col count
            try:
                csv_headers[x_index]
            except IndexError:
                continue
            if csv_headers[x_index] in required_headers:
                if not cell_value:
                    raise ValidationError(_(u'Faltando valor obrigatório na coluna %s linha %s.') %
                                            (csv_headers[x_index], y_index + 1))
    return True


def valida_lista_email(value):
    try:
        lista_emails = value.split(',')
        for email in lista_emails:
            if email.strip():
                validate_email(email.strip())
    except ValidationError:
        raise ValidationError(_(u'Insira uma lista de emails válidos.'))