#-*- coding: UTF-8 -*-
import re
from ast import literal_eval
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from text_tag.registry import registry


def remove_tags_html(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def stripped_parameters(p_received, validate_tags=False):
    """Separa tag/filtro dos demais parâmetros definidos"""
    try:
        p_stripped = re.split('\[|\]', p_received)
        tag_filter = p_stripped[0]
        list_param = [literal_eval(i) for i in p_stripped[1:] if i]
        return [tag_filter, list_param]
    except SyntaxError:
        if validate_tags:
            message_error = _(u'Parâmetros definidos incorretamente próximo à <b>%s</b>.') % (p_received)
            raise ValidationError(mark_safe(message_error))
        else:
            return p_received


def convert_tag(tag_received, validate_tags=False):
    """ 
    .. Note:: Inspiration
    http://effbot.org/zone/django-simple-template.htm 
    """
    # separa tag dos demais filtros
    tag = tag_received.strip()
    if "|" in tag:
        tag, filters = tag.split("|", 1)
    else:
        filters = None

    tag_args = stripped_parameters(tag, validate_tags)
    try:
        if tag_args[1]:
            value = registry.get(tag_args[0])(*tag_args[1])
        else:
            value = registry.get(tag_args[0])()
    except (TypeError, ValueError):
        if validate_tags:
            message_error = _(u'Tag inválida ou definida incorretamente: <b>%s</b>.') % (tag_args[0])
            raise ValidationError(mark_safe(message_error))
        else:
            return tag
    
    if filters:
        for f in filters.split('|'):
            filter_args = stripped_parameters(f, validate_tags)
            try:
                if filter_args[1]:
                    filter_args[1] = [value] + filter_args[1]
                    value = registry.get(filter_args[0])(*filter_args[1])
                else:
                    value = registry.get(filter_args[0])(value)
            except (TypeError, ValueError):
                if validate_tags:
                    message_error = _(u'Filtro inválido ou definido incorretamente: <b>%s</b>.') % (filter_args[0])
                    raise ValidationError(mark_safe(message_error))
                else:
                    return tag
    return value


def parses_tags(text, validate_tags=False):
    next = iter(re.split("({{|}})", text)).__next__
    data = []
    try:
        token = next()
        while 1:
            if token == "{{": # variable
                tag = next()
                data.append(str(convert_tag(tag, validate_tags)))
                if next() != "}}":
                    if validate_tags:
                        message_error = _(u'Faltando finalização da tag próximo à <b>%s</b>.') % (remove_tags_html(tag))
                        raise ValidationError(mark_safe(message_error))
            else:
                data.append(token) # literal
            token = next()
    except StopIteration:
        pass
    return u''.join(data)


def validate_tags(text):
    parses_tags(text, True)