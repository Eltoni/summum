#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from movimento.models import Produtos
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days
import datetime


class Compra(models.Model):
    u""" 
    Classe Compra. 
    Criada para registrar todas as compras efetivadas no estabelecimento.

    Criada em 15/06/2014. 
    """
    total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Total (R$)', help_text=u'Valor total da compra.')
    data = models.DateTimeField(auto_now_add=True, verbose_name=u'Data da compra')
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=u'Desconto (%)', help_text=u'Desconto sob o valor total da compra.')
    status = models.BooleanField(default=False, verbose_name=u'Cancelada?', help_text=u'Marcando o Checkbox, a compra será cancelada e os itens financeiros estornados.')
    fornecedor = models.ForeignKey(Fornecedor)
    forma_pagamento = models.ForeignKey(FormaPagamento)
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as informações relavantes da compra.")


    def __unicode__(self):
        return u'%s' % (self.id)


    def prazo_primeira_parcela(self, data, num_parcela):
        """
        Método que define a data de vencimento da primeira parcela baseado na parametrização da forma de pagamento.

        Parâmetros passados (data_da_compra, número_da_parcela) 
        """
        self.formaPagamentoCompra = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo_primeira_parcela = self.formaPagamentoCompra.carencia

        if self.formaPagamentoCompra.tipo_carencia == 'M' and num_parcela == 0:
            data = date_add_months(data, prazo_primeira_parcela)
            return data
         
        if self.formaPagamentoCompra.tipo_carencia == 'S' and num_parcela == 0:
            data = date_add_week(data, prazo_primeira_parcela)
            return data

        if self.formaPagamentoCompra.tipo_carencia == 'D' and num_parcela == 0:
            data = date_add_days(data, prazo_primeira_parcela)
            return data

        else:
            return data


    def prazo_entre_parcelas(self, data):
        """
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_compra) 
        """
        self.formaPagamentoCompra = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo = self.formaPagamentoCompra.prazo_entre_parcelas

        if self.formaPagamentoCompra.tipo_prazo == 'M':
            data = date_add_months(data, prazo)
            return data

        if self.formaPagamentoCompra.tipo_prazo == 'S':
            data = date_add_week(data, prazo)
            return data

        if self.formaPagamentoCompra.tipo_prazo == 'D':
            data = date_add_days(data, prazo)
            return data


    def valor_parcela(self, num_parcela, total):
        """
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da compra recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_compra)
        """
        self.formaPagamentoCompra = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quant_parc = self.formaPagamentoCompra.quant_parcelas
        valor_parcela = round(total / quant_parc, 2)

        if (num_parcela + 1) == quant_parc:
            soma_parcelas = valor_parcela * num_parcela
            valor_parcela = float(total) - soma_parcelas
            return valor_parcela
        else:
            return valor_parcela


    def pagamento_primeira_parcela_compra(self, num_parcela):
        """
        Método que define como pago a primeira parcela de uma compra à prazo, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """
        self.formaPagamentoCompra = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)

        if self.formaPagamentoCompra.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma compra.
        """
        formaPagamentoCompra = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        data = datetime.date.today()
        quantidadeParcelada = formaPagamentoCompra.quant_parcelas
        
        if self.pk is None:

            # Pagamento efetuado à vista. Grava com status fechado em ContasPagar
            if formaPagamentoCompra.quant_parcelas == 1 and formaPagamentoCompra.carencia == 0:
                statusContasPagar = True
            else:
                statusContasPagar = False

            # Chama a função save original para o save atual do modelo
            super(Compra, self).save(*args, **kwargs)
            
            # Insere o contas à pagar
            conta = ContasPagar(data=data, 
                                valor_total=self.total, 
                                compras=self, 
                                fornecedores=self.fornecedor, 
                                forma_pagamento=self.forma_pagamento, 
                                status=statusContasPagar
                                )
            conta.save()

            # Insere as parcelas do contas à pagar
            for i in range(quantidadeParcelada):                
                b = ParcelasContasPagar()
                data = self.prazo_primeira_parcela(data, i)
                b.vencimento = data
                data = self.prazo_entre_parcelas(data)
                b.valor = self.valor_parcela(i, self.total)
                b.status = self.pagamento_primeira_parcela_compra(i)
                b.num_parcelas = i + 1
                b.contas_pagar = conta
                b.save()
        
        else:

            # tratar cancelamento de compra efetuada
            super(Compra, self).save(*args, **kwargs)



class ItensCompra(models.Model):
    u""" 
    Classe ItensCompra. 
    Inline criada para ser exibida na página de compras.
    Nesta, todos os itens de uma compra são registrados.
    
    Criada em 15/06/2014. 
    """

    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Valor unitário (R$)')
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Total (R$)')
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=u'Desconto (%)')
    #status = models.BooleanField(verbose_name=u'Confirma?')
    produto = models.ForeignKey(Produtos)
    compras = models.ForeignKey(Compra)

    class Meta:
        verbose_name = u'Item de Compra'
        verbose_name_plural = "Itens de Compra"


# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_pagar.models import ContasPagar, ParcelasContasPagar, Pagamento