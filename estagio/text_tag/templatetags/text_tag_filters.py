#-*- coding: UTF-8 -*-
from django import template
from text_tag.registry import *

register = template.Library()

@register.assignment_tag
def get_docsting_tags_available():
    return [ (i, v.__doc__) for i, v in registry.get_all_tag_registers.items() ]

@register.assignment_tag
def get_docsting_filters_available():
    return [ (i, v.__doc__) for i, v in registry.get_all_filter_registers.items() ]
