#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from venda.models import Venda
from parametros_financeiros.models import FormaPagamento
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days
import datetime


class ContasReceber(models.Model):
    u""" 
    Classe ContasReceber. 

    Criada em 22/09/2014. 
    """

    data = models.DateField()
    valor_total = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.BooleanField(default=False, verbose_name=u'Conta fechada', help_text=u'Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 
    cliente = models.ForeignKey(Cliente, null=True)
    vendas = models.ForeignKey(Venda, null=True, verbose_name=u'Venda') 
    forma_pagamento = models.ForeignKey(FormaPagamento)

    class Meta:
        verbose_name = u'Conta à Receber'
        verbose_name_plural = "Contas à Receber"


    def __unicode__(self):
        return u'%s' % (self.id)


    def venda_associada(self):
        if self.vendas:
            return self.vendas
        return '-'
    venda_associada.short_description = 'Venda'


    def prazo_primeira_parcela(self, data, num_parcela):
        """
        Método que define a data de vencimento da primeira parcela baseado na parametrização da forma de pagamento.

        Parâmetros passados (data_da_venda, número_da_parcela) 
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo_primeira_parcela = self.forma_pagamento_conta.carencia

        if self.forma_pagamento_conta.tipo_carencia == 'M' and num_parcela == 0:
            data = date_add_months(data, prazo_primeira_parcela)
            return data
         
        if self.forma_pagamento_conta.tipo_carencia == 'S' and num_parcela == 0:
            data = date_add_week(data, prazo_primeira_parcela)
            return data

        if self.forma_pagamento_conta.tipo_carencia == 'D' and num_parcela == 0:
            data = date_add_days(data, prazo_primeira_parcela)
            return data

        else:
            return data


    def prazo_entre_parcelas(self, data):
        """
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_venda) 
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo = self.forma_pagamento_conta.prazo_entre_parcelas

        if self.forma_pagamento_conta.tipo_prazo == 'M':
            data = date_add_months(data, prazo)
            return data

        if self.forma_pagamento_conta.tipo_prazo == 'S':
            data = date_add_week(data, prazo)
            return data

        if self.forma_pagamento_conta.tipo_prazo == 'D':
            data = date_add_days(data, prazo)
            return data


    def valor_parcela(self, num_parcela, total):
        """
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da venda recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_venda)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quant_parc = self.forma_pagamento_conta.quant_parcelas
        valor_parcela = round(total / quant_parc, 2)

        if (num_parcela + 1) == quant_parc:
            soma_parcelas = valor_parcela * num_parcela
            valor_parcela = float(total) - soma_parcelas
            return valor_parcela
        else:
            return valor_parcela


    def pagamento_primeira_parcela(self, num_parcela):
        """
        Método que define como pago a primeira parcela de uma conta, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)

        if self.forma_pagamento_conta.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo de contas à receber.
        """
        data = datetime.date.today()

        forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quantidade_parcelada = forma_pagamento_conta.quant_parcelas
        
        if self.pk is None:
            # Chama a função save original para o save atual do modelo
            super(ContasReceber, self).save(*args, **kwargs)

            # Insere as parcelas do contas à receber
            for i in range(quantidade_parcelada):                
                parcelas_conta = ParcelasContasReceber()
                data = self.prazo_primeira_parcela(data, i)
                parcelas_conta.vencimento = data
                data = self.prazo_entre_parcelas(data)
                parcelas_conta.valor = self.valor_parcela(i, self.valor_total)
                parcelas_conta.status = self.pagamento_primeira_parcela(i)
                parcelas_conta.num_parcelas = i + 1
                parcelas_conta.contas_receber = self
                parcelas_conta.save()

            # Insere o recebimento de uma venda que tenha o prazo de carência 0(zero) na parametrização da forma de pagamento. 
            try:
                parcela_paga = ParcelasContasReceber.objects.get(contas_receber=self, status=True)
                Recebimento(data=data, 
                            valor=parcela_paga.valor, 
                            juros=0.00, 
                            desconto=0.00, 
                            parcelas_contas_receber=parcela_paga
                            ).save()
            except ParcelasContasReceber.DoesNotExist:
                pass
        
        else:
            # tratar cancelamento de venda efetuada
            super(ContasReceber, self).save(*args, **kwargs)



class ParcelasContasReceber(models.Model):
    u""" 
    Classe ParcelasContasReceber. 

    Criada em 22/09/2014.  
    """
    
    vencimento = models.DateField()
    valor = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.BooleanField(default=False)
    num_parcelas = models.IntegerField(verbose_name=u'Nº Parcela')
    contas_receber = models.ForeignKey(ContasReceber, verbose_name=u'Conta à receber')

    class Meta:
        verbose_name = u'Parcela de Conta à Receber'
        verbose_name_plural = "Parcelas de Contas à Receber"


    def __unicode__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a adição dos recebimentos.
        """

        data = datetime.date.today()

        if self.pk is None:
            super(ParcelasContasReceber, self).save(*args, **kwargs)

        else:
            super(ParcelasContasReceber, self).save(*args, **kwargs)
            
            # Bloqueio para criar somente pagamento de parcelas que ainda não foram pagas.
            if not Recebimento.objects.filter(parcelas_contas_receber__pk=self.pk).exists():
                # Cria o pagamento caso o checkbox de status seja selecionado
                Recebimento(data=data, 
                            valor=self.valor, 
                            juros=0.00, 
                            desconto=0.00, 
                            parcelas_contas_receber=self
                            ).save()
            else: 
                # Faz o save no pagamento já efetuado para atualizar o status da conta
                recebimento = Recebimento.objects.get(parcelas_contas_receber__pk=self.pk).save()



class Recebimento(models.Model):
    u""" 
    Classe Recebimento. 
    Criada para registrar todas as entradas financeiras do estabelecimento.
    Os registros de recebimentos entrarão automaticamente na tabela. 

    Criada em 15/06/2014. 
    """

    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber, verbose_name=u'Recebimento de parcela')

    def __unicode__(self):
        return u'%s' % (self.id)

