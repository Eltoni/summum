#-*- coding: UTF-8 -*-
from caixa.models import Caixa


def caixa_aberto():
    """Retorna status atual do Caixa"""

    return Caixa.objects.filter(status=1).exists()
