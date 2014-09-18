#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from movimento.models import Produtos


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
    # parcelas_contas_pagar = models.ForeignKey(ParcelasContasPagar)
    
    def __unicode__(self):
        return u'%s' % (self.id)



class Compra(models.Model):
    u""" 
    Classe Compra. 
    Criada para registrar todas as compras efetivadas no estabelecimento.

    Criada em 15/06/2014. 
    """

    total = models.DecimalField(max_digits=20, decimal_places=2, help_text=u'Valor total da compra.')
    data = models.DateTimeField(auto_now_add=True, verbose_name=u'Data da compra')
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=u'Desconto (%)', help_text=u'Desconto sob o valor total da compra.')
    status = models.BooleanField(default=False, verbose_name=u'Cancelada?', help_text=u'Marcando o Checkbox, a compra será cancelada e os itens financeiros estornados.')
    fornecedor = models.ForeignKey(Fornecedor)
    forma_pagamento = models.ForeignKey(FormaPagamento)
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as informações relavantes da compra.")

    def __unicode__(self):
        return u'%s' % (self.id)

    # Sobrepoe o método save para gravar em outras tabelas
    def save(self, *args, **kwargs):
        # Chama a função save original para o save atual do modelo
        super(Compra, self).save(*args, **kwargs)

        # Agora que esse modelo está salvo, pode-se criar um Pagamento na tabela devida
        Pagamento(data=self.data, valor=self.total).save()



class ItensCompra(models.Model):
    u""" 
    Classe ItensCompra. 
    Inline criada para ser exibida na página de compras.
    Nesta, todos os itens de uma compra são registrados.
    
    Criada em 15/06/2014. 
    """

    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Valor unitário')
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Total')
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=u'Desconto (%)')
    #status = models.BooleanField(verbose_name=u'Confirma?')
    produto = models.ForeignKey(Produtos)
    compras = models.ForeignKey(Compra)

    class Meta:
        verbose_name = u'Item de Compra'
        verbose_name_plural = "Itens de Compra"
