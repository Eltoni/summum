#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from parametros_financeiros.models import FormaPagamento
from movimento.models import Produtos
from django.core.exceptions import ValidationError
import datetime


class Venda(models.Model):
    u""" 
    Classe Venda. 
    Criada para registrar todas as vendas efetivadas no estabelecimento.

    Criada em 05/10/2014. 
    """
    total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Total (R$)', help_text=u'Valor total da venda.')
    data = models.DateField(auto_now_add=True, verbose_name=u'Data da venda')
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=u'Desconto (%)', help_text=u'Desconto sob o valor total da venda.')
    status = models.BooleanField(default=False, verbose_name=u'Cancelada?', help_text=u'Marcando o Checkbox, a venda será cancelada e os itens financeiros estornados.')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as informações relavantes da venda.")

    def __unicode__(self):
        return u'%s' % (self.id)


    def clean(self):
        """ 
        Bloqueia o registro de uma venda quando não há caixa aberto.
        """

        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError('Não há caixa aberto. Para efetivar uma venda é necessário ter o caixa aberto.')


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma venda.
        """
        data = datetime.date.today()
        
        if self.pk is None:

            # Chama a função save original para o save atual do modelo
            super(Venda, self).save(*args, **kwargs)

            # Descrição informada no contas à pagar
            descricao = u'Conta aberta proveniente de venda %s' % (self)

            # Insere o contas à pagar
            venda = ContasReceber(data=data, 
                                valor_total=self.total, 
                                descricao=descricao,
                                vendas=self, 
                                cliente=self.cliente, 
                                forma_pagamento=self.forma_pagamento, 
                                status=False
                                )
            venda.save()
        
        else:

            # tratar cancelamento de venda efetuada
            super(Venda, self).save(*args, **kwargs)



class ItensVenda(models.Model):
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Valor unitário (R$)')
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=u'Total (R$)')
    desconto = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True, verbose_name=u'Desconto (%)')
    #status = models.CharField(db_column='STATUS', max_length=1)
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    vendas = models.ForeignKey(Venda)

    class Meta:
        verbose_name = u'Item de Venda'
        verbose_name_plural = "Itens de Venda"


    def __unicode__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a remoção da quantidade de produtos ao estoque.
        """
        if self.pk is None:
            
            # Subtrai a quantidade de produtos vendidos com a que já existe no estoque
            super(ItensVenda, self).save(*args, **kwargs)
            produto = Produtos.objects.get(pk=self.produto.pk)
            produto.quantidade = produto.quantidade - self.quantidade
            produto.save()

        else:

            # tratar cancelamento de venda efetuada
            super(ItensVenda, self).save(*args, **kwargs)



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_receber.models import ContasReceber
from caixa.models import Caixa