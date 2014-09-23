#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from movimento.models import Produtos
import time


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

    # Sobrepoe o método save para gravar em outras tabelas
    def save(self, *args, **kwargs):
        formaPagamentoCompra = FormaPagamento.objects.get(pk=1)

        if self.pk is None:

            # Pagamento efetuado à vista. Grava com status fechado em ContasPagar
            if formaPagamentoCompra.quant_parcelas == 1 and formaPagamentoCompra.carencia == 0:
                statusContasPagar = True
            else:
                statusContasPagar = False

            # Chama a função save original para o save atual do modelo
            super(Compra, self).save(*args, **kwargs)   
            ContasPagar(data=time.strftime('%Y-%m-%d'), 
                        valor_total=self.total, 
                        compras=self, 
                        fornecedores=self.fornecedor, 
                        forma_pagamento=self.forma_pagamento, 
                        status=statusContasPagar
                        ).save()
        
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
from contas_pagar.models import ContasPagar, Pagamento