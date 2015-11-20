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
    perc_juros_diario = perc_juros / 30
    total_juros = dias_vencidos * perc_juros_diario
    return total_juros + valor

    # valor_juros = valor
    # juros = 0
    # for i in range(dias_vencidos):
    #         juros += valor_juros * perc_juros
    # return juros




class EncargoSimples:

    def __init__(self, capital, percentual, periodo):
        self.capital = capital
        self.percentual = percentual
        self.periodo = periodo
        
        
    def calcular_percentual_diario(self):
        self.juros_diario = (self.percentual / 100) / 30
        return self.juros_diario
        
        
    def calcular_multa(self):
        self.multa = self.capital * (self.percentual / 100)
        return self.multa
        
        
    def calcular_juros(self):
        self.juros = self.capital * (self.periodo * self.calcular_percentual_diario())
        return self.juros
        
        
    def calcular_total_multa(self):
        self.total_multa = self.capital + self.calcular_multa()
        return self.total_multa
        
        
    def calcular_total_juros(self):
        self.total_juros = self.capital + self.calcular_juros()
        return self.total_juros