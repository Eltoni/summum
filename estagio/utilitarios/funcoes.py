#-*- coding: UTF-8 -*-
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import xml.etree.ElementTree

def remove_tags(text):
    """Remove elementos html de uma string e retorna o resultado"""
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())


def pode_ver_link(usuario, app_name, model_name, object_pk):
    """
    Checa se usuário da sessão tem permissão para acesso a determinada página declarada nos argumentos da chamada da função.
    Caso usuário tenha permissão de visualização, é retornado a url que aponta para a página.

    >>> pode_ver_link('admin','parametros_financeiros','formapagamento', 1)
        '/parametros_financeiros/formapagamento/1/'
    >>> pode_ver_link('user_name','parametros_financeiros','formapagamento', 1)
        '#'
    """

    nome_permissao = 'change_' + model_name
    try:
        perm = Permission.objects.get(codename=nome_permissao, content_type__app_label=app_name, content_type__model=model_name)
    except Permission.DoesNotExist: 
        perm = False

    tem_permissao = User.objects.filter((Q(groups__permissions=perm) | Q(user_permissions=perm) | Q(is_superuser=True)) & Q(username=usuario)).exists()
    if tem_permissao:
        r = "admin:%s_%s_change" % ( app_name, model_name)
        return reverse(r, args=[object_pk])
    return '#'