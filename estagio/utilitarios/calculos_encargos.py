#-*- coding: UTF-8 -*-
# from utilitarios.calculos_encargos import *

class EncargoSimples:

    def __init__(self, capital, percentual, periodo):
        self.capital = capital
        self.percentual = percentual
        self.periodo = periodo
        
        
    # def calcular_percentual_diario(self):
    #     self.juros_diario = (self.percentual / 100) / 30
    #     return self.juros_diario
        
        
    def calcular_multa(self):
        self.multa = self.capital * (self.percentual / 100)
        return self.multa
        
        
    def calcular_juros(self):
        self.juros = self.capital * (self.periodo * (self.percentual / 100))
        return self.juros
        
        
    def calcular_total_multa(self):
        self.total_multa = self.capital + self.calcular_multa()
        return self.total_multa
        
        
    def calcular_total_juros(self):
        self.total_juros = self.capital + self.calcular_juros()
        return self.total_juros



class EncargoCompostos:

    def __init__(self, capital, percentual, periodo):
        self.capital = capital
        self.percentual = percentual
        self.periodo = periodo
        

    # def calcular_percentual_diario(self):
    #     self.juros_diario = self.percentual / 100
    #     return self.juros_diario


    def calcular_total_juros(self):
        self.total_juros = self.capital
        for i in range(self.periodo):
            self.total_juros += self.total_juros * (self.percentual / 100)
        return self.total_juros


    def calcular_juros(self):
        self.calcular_juros = self.calcular_total_juros() - self.capital
        return self.calcular_juros