#-*- coding: UTF-8 -*-
from django.conf import settings
from django import template

register = template.Library()


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
