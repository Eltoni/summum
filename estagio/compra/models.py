#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from movimento.models import Produtos
from django.core.exceptions import ValidationError
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
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as informações relavantes da compra.")


    def __unicode__(self):
        return u'%s' % (self.id)


    def clean(self):
        """ 
        Bloqueia o registro de uma compra quando não há caixa aberto.
        """

        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError('Não há caixa aberto. Para efetivar uma compra é necessário ter o caixa aberto.')
        


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma compra.
        """
        data = datetime.date.today()
        
        if self.pk is None:

            # Chama a função save original para o save atual do modelo
            super(Compra, self).save(*args, **kwargs)

            # Descrição informada no contas à pagar
            descricao = u'Conta aberta proveniente de compra %s' % (self)

            # Insere o contas à pagar
            conta = ContasPagar(data=data, 
                                valor_total=self.total, 
                                descricao=descricao,
                                compras=self, 
                                fornecedores=self.fornecedor, 
                                forma_pagamento=self.forma_pagamento, 
                                status=False
                                )
            conta.save()
        
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
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    compras = models.ForeignKey(Compra)

    class Meta:
        verbose_name = u'Item de Compra'
        verbose_name_plural = "Itens de Compra"


    def __unicode__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a adição da quantidade de produtos ao estoque.
        """
        if self.pk is None:
            
            # Soma a quantidade de produtos comprados com a que já existe no estoque
            super(ItensCompra, self).save(*args, **kwargs)
            produto = Produtos.objects.get(pk=self.produto.pk)
            produto.quantidade = produto.quantidade + self.quantidade
            produto.save()

        else:

            # tratar cancelamento de compra efetuada
            super(ItensCompra, self).save(*args, **kwargs)



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_pagar.models import ContasPagar
from caixa.models import Caixa