#-*- coding: UTF-8 -*-
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django import template

register = template.Library()


@register.filter(name='format_value_null')
def format_value_null(value):
    """ 
        Formata texto que é exido como NULL no campo  
    """
    if value:
        return value
    if not value:
        return '-'



@register.filter(name='formata_booleano')
def formata_booleano(value):

    if value:
        return 'admin/img/icon-yes.gif'
    else:
        return 'admin/img/icon-no.gif'



@register.filter(name='formata_quantidade_produtos')
def formata_quantidade_produtos(value, quantidade_minima):
    """
    Formata a classe da linha para indicar como vermelho se estiver com 50%\ do mínimo definido
    """
    quantidade_minima_limite = quantidade_minima*0.5
    if value <= quantidade_minima_limite:
        return "error"
    else:
        return "warning"



@register.simple_tag
def template_dir(this_object, its_name=""):
    """
    Retorna as variáveis da instância, os atributos da classe e das demais classes base.
    Funciona apenas se o Debug está ativado no servidor.

    Para utilização no template:

    {%/ load geral_filters %}
    {%/ template_dir object.field "object.field" %}
    {%/ template_dir object "Propriedades do objeto" %}
    """
    if settings.DEBUG:
        output = dir(this_object)
        return "<pre>" + str(its_name) + " " + str(output) + "</pre>"
    return ""



@register.filter(name='pode_exportar')
def pode_exportar(usuario, opts):
    """
    Retorna booleano que indica se usuário tem permissão para acesso ao elemento do contexto.

    Para utilização no template:

    {%/ load geral_filters %}
    {%/ if user|pode_exportar:opts.model_name %}...{%/ endif %}
    """

    nome_permissao = 'pode_exportar_' + opts.app_label
    try:
        perm = Permission.objects.get(codename=nome_permissao, content_type__model=opts.model_name)
    except Permission.DoesNotExist: 
        perm = False

    tem_permissao = User.objects.filter((Q(groups__permissions=perm) | Q(user_permissions=perm) | Q(is_superuser=True)) & Q(username=usuario)).exists()
    
    # Se existe permissão, retorna True
    if tem_permissao:
        return True
    return False