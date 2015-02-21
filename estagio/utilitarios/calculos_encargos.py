#-*- coding: UTF-8 -*-
def calculo_composto(valor, dias_vencidos, perc_juros):
    u"""
    Cálculo de juros compostos
    >>> calculo_composto(200, 2, 0.04)
    
    """
    valor_juros = valor
    for i in range(dias_vencidos):
            valor_juros += valor_juros * perc_juros
    valor_juros -= valor
    return valor_juros


def calculo_simples(valor, dias_vencidos, perc_juros):
    u"""
    Cálculo de juros simples
    >>> calculo_simples(200, 2, 0.04)

    """
    valor_juros = valor
    juros = 0
    for i in range(dias_vencidos):
            juros += valor_juros * perc_juros
    return juros




