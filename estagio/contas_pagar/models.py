#-*- coding: UTF-8 -*-
from django.db import models
from compra.models import Compra
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from django.db.models.signals import post_save


class ContasPagar(models.Model):
    u""" 
    Classe ContasPagar. 

    Criada em 22/09/2014. 
    """

    data = models.DateField() 
    valor_total = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.BooleanField(default=False, help_text=u'Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 
    compras = models.ForeignKey(Compra, verbose_name=u'Compra') 
    fornecedores = models.ForeignKey(Fornecedor)
    forma_pagamento = models.ForeignKey(FormaPagamento) 

    class Meta:
        verbose_name = u'Conta à Pagar'
        verbose_name_plural = "Contas à Pagar"

    def __unicode__(self):
        return u'%s' % (self.id)



class ParcelasContasPagar(models.Model):
    u""" 
    Classe ParcelasContasPagar. 

    Criada em 22/09/2014.  
    """

    vencimento = models.DateField()
    valor = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.BooleanField(default=False)
    num_parcelas = models.IntegerField(verbose_name=u'Nº Parcela')
    contas_pagar = models.ForeignKey(ContasPagar, verbose_name=u'Conta à pagar')

    class Meta:
        verbose_name = u'Parcela de Conta à Pagar'
        verbose_name_plural = "Parcelas de Contas à Pagar"

    def __unicode__(self):
        return u'%s' % (self.id)



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
    parcelas_contas_pagar = models.ForeignKey(ParcelasContasPagar, verbose_name=u'Pagamento de parcela')
    
    def __unicode__(self):
        return u'%s' % (self.id)



from caixa.models import Caixa, MovimentosCaixa


def update_movimento_caixa(sender, instance, **kwargs):
    """ 
    Método para ïnserir na tabela de movimentos_de_caixa os movimentos de saída financeira.
    O mesmo age sobre o Movimento de Caixa e o Caixa, fazendo todo o cálculo para controle dessas entidades.

    Criada em 01/10/2014. 
    """

    # Busca o id da conta à pagar e da compra vinculado ao pagamento instanciado
    conta = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__pk', 'contas_pagar__compras')[0]
    
    # Condição que monta a descrição que é salvo no registro do movimento
    if conta[1]:
        # Caso a query traga o id de uma compra, então a descrição a ser cadastrada no movimento de caixa será a pré-definida abaixo.
        descricao = u'Pagamento: %s, proveniente da parcela: %s, da conta à pagar: %s, da compra: %s.' % (instance.pk, instance.parcelas_contas_pagar.pk, conta[0], conta[1])
    
    else:
        conta_avulsa = ParcelasContasPagar.objects.filter(pk=1).select_related('contas_pagar__contaspagar').values_list('contas_pagar__descricao', flat=True)[0]
        descricao = u'Pagamento avulso. %s' % (conta_avulsa)

    # Insere os itens de saída de movimentos de caixa
    MovimentosCaixa(descricao=descricao, 
                    valor=instance.valor,
                    data=instance.data, 
                    tipo_mov='Débito', 
                    caixa=Caixa.objects.get(status=1),
                    pagamento=instance
                    ).save()

# registro da signal
post_save.connect(update_movimento_caixa, sender=Pagamento, dispatch_uid="update_movimento_caixa")