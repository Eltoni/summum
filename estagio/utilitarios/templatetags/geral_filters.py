#-*- coding: UTF-8 -*-
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

