#-*- coding: UTF-8 -*-
from django.db import models
from compra.models import Compra
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento


class ContasPagar(models.Model):
    u""" 
    Classe ContasPagar. 

    Criada em 22/09/2014. 
    """

    data = models.DateField() 
    valor_total = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.BooleanField(default=False, help_text=u'Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')
    descricao = models.TextField(blank=True) 
    compras = models.ForeignKey(Compra) 
    fornecedores = models.ForeignKey(Fornecedor)
    forma_pagamento = models.ForeignKey(FormaPagamento) 

    class Meta:
        verbose_name = u'Conta à Pagar'
        verbose_name_plural = "Contas à Pagar"



class ParcelasContasPagar(models.Model):
    u""" 
    Classe ParcelasContasPagar. 

    Criada em 22/09/2014.  
    """

    vencimento = models.DateField()
    valor = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.CharField(max_length=1)
    num_parcelas = models.IntegerField()
    contas_pagar = models.ForeignKey(ContasPagar)



class Pagamento(models.Model):
    u""" 
    Classe Pagamento. 
    Criada para registrar todas as saídas financeiras do estabelecimento.
    Os registros de pagamentos entrarão automaticamente na tabela. 
    Contudo, também será possível cadastrar pagamentos manualmente, pensando em casos em que valores são pagos, eventualmente, sem a compra ter sido cadastrada.

    Criada em 16/06/2014. 
    """
    
    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    # estornada = models.BooleanField(verbose_name=u'Estornada?')
    # data_estorno = models.DateField(auto_now_add=True, verbose_name=u'Data do estorno')
    #parcelas_contas_pagar = models.ForeignKey(ParcelasContasPagar)
    
    def __unicode__(self):
        return u'%s' % (self.id)
