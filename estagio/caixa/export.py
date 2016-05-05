#-*- coding: UTF-8 -*-
from import_export import resources
from decimal import Decimal
from caixa.models import Caixa, MovimentosCaixa

#classe usada pelo import_export
class CaixaResource(resources.ModelResource):

    class Meta(object):
        model = Caixa
        #exclude = ('nome', 'estado')

    def dehydrate_status(self, caixa):
        if caixa.status:
            return 'Ativo'
        else:
            return 'Inativo'

    def dehydrate_data_abertura(self, caixa):
        return '%s' % (caixa.data_abertura.strftime('%d/%m/%Y'))

    def dehydrate_data_fechamento(self, caixa):
        try:
            return '%s' % (caixa.data_fechamento.strftime('%d/%m/%Y'))
        except:
            pass

    def dehydrate_valor_entrada(self, caixa):
        return '%s' % (Decimal(caixa.valor_entrada).quantize(Decimal("0.00")))

    def dehydrate_valor_saida(self, caixa):
        return '%s' % (Decimal(caixa.valor_saida).quantize(Decimal("0.00")))

    def dehydrate_valor_total(self, caixa):
        return '%s' % (Decimal(caixa.valor_total).quantize(Decimal("0.00")))

    def dehydrate_valor_inicial(self, caixa):
        return '%s' % (Decimal(caixa.valor_inicial).quantize(Decimal("0.00")))

    def dehydrate_valor_fechamento(self, caixa):
        return '%s' % (Decimal(caixa.valor_fechamento).quantize(Decimal("0.00")))

    def dehydrate_diferenca(self, caixa):
        return '%s' % (Decimal(caixa.diferenca).quantize(Decimal("0.00")))



class MovimentosCaixaResource(resources.ModelResource):

    class Meta(object):
        model = MovimentosCaixa
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, movimentoscaixa):
        return '%s' % (movimentoscaixa.data.strftime('%d/%m/%Y às %H:%M'))