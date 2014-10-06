#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from venda.models import Venda
from parametros_financeiros.models import FormaPagamento


class ContasReceber(models.Model):
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



class ParcelasContasReceber(models.Model):
    valor = models.DecimalField(db_column='VALOR', max_digits=20, decimal_places=2)
    vencimento = models.DateField(db_column='VENCIMENTO')
    status = models.CharField(db_column='STATUS', max_length=1)
    num_parcelas = models.CharField(db_column='NUM_PARCELAS', max_length=45)
    contas_receber = models.ForeignKey(ContasReceber, db_column='CONTAS_RECEBER_ID')

    class Meta:
        verbose_name = u'Parcela de Conta à Receber'
        verbose_name_plural = "Parcelas de Contas à Receber"


    def __unicode__(self):
        return u'%s' % (self.id)



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
    # estornada = models.BooleanField(verbose_name=u'Estornada?')
    # data_estorno = models.DateField(auto_now_add=True, verbose_name=u'Data do estorno')
    # parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber)

    def __unicode__(self):
        return u'%s' % (self.id)