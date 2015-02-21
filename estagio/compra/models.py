#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
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
    status = models.BooleanField(default=False, verbose_name=u'Cancelada?', help_text=u'Marcando o Checkbox, a compra será cancelada e o financeiro acertado.')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT)
    forma_pagamento = models.ForeignKey(FormaPagamento, verbose_name=u'Forma de pagamento', on_delete=models.PROTECT)
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=u'Grupo de encargo', on_delete=models.PROTECT)
    observacao = models.TextField(blank=True, verbose_name=u'observações', help_text="Descreva na área as informações relavantes da compra.")
    pedido = models.CharField(max_length=1, blank=True, choices=((u'S', 'Sim'), (u'N', 'Não'),), verbose_name=u'Pedido?') 
    status_pedido = models.BooleanField(default=False, verbose_name=u'Pedido confirmado?', help_text=u'Marcando o Checkbox, os itens financeiros serão gerados e o estoque movimentado.')

    def __unicode__(self):
        return u'%s' % (self.id)


    def clean(self):
        """ 
        Bloqueia o registro de uma compra quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError('Não há caixa aberto. Para efetivar uma compra é necessário ter o caixa aberto.')


    def clean_fields(self, *args, **kwargs):
        """ 
        Bloqueia o cancelamento de uma compra quando já há pagamentos no caixa.
        """

        contas_pagar = ContasPagar.objects.filter(compras__pk=self.pk)
        compra_movimento_financeiro = ParcelasContasPagar.objects.filter(contas_pagar=contas_pagar, status=True).select_related('contas_pagar__contaspagar').values_list('status').exists()
        if self.status and compra_movimento_financeiro:
            raise ValidationError({'status': ["Compra não pode ser cancelada. Já há pagamento feito para esta compra. [Conta à Pagar: %s]" % (contas_pagar[0]),]})      


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo da parte financeira de uma compra.
        """
        data = datetime.date.today()

        if self.pk:

            status_antigo = Compra.objects.get(pk=self.pk)
            conta_gerada = ContasPagar.objects.filter(compras=self.pk).exists()
            super(Compra, self).save(*args, **kwargs)

            # Gera financeiro somente se compra for confirmada
            if self.pedido == 'N' and not conta_gerada or (self.status_pedido and not conta_gerada):

                # Descrição informada no contas à pagar
                descricao = u'Conta aberta proveniente de compra %s' % (self)

                # Insere o contas à pagar
                conta = ContasPagar(data=data, 
                                    valor_total=self.total, 
                                    descricao=descricao,
                                    compras=self, 
                                    fornecedores=self.fornecedor, 
                                    forma_pagamento=self.forma_pagamento, 
                                    grupo_encargo=self.grupo_encargo,
                                    status=False
                                    )
                conta.save()      
            
            # trata cancelamento de compra efetuada
            if not status_antigo.status and self.status and (self.pedido == 'N' or (self.pedido == 'S' and self.status_pedido)):
                # Numa compra cancelada: decrescenta a quantidade dos produtos cancelados novamente ao estoque.
                for i in ItensCompra.objects.filter(compras=self.pk).values_list('id', 'produto', 'quantidade'):
                    produto = Produtos.objects.get(pk=i[1])
                    produto.quantidade = produto.quantidade - i[2]
                    produto.save()
                
                # Fecha a conta à pagar
                conta = ContasPagar.objects.get(compras=self.pk)
                conta.status = True
                conta.save()

        else:

            # Chama a função save original para o save atual do modelo
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
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    compras = models.ForeignKey(Compra, on_delete=models.PROTECT)
    add_estoque = models.BooleanField(default=False, verbose_name=u'Adicionado ao estoque?')

    class Meta:
        verbose_name = u'Item de Compra'
        verbose_name_plural = "Itens de Compra"


    def __unicode__(self):
        return u'%s' % (self.id)


    def save(self, *args, **kwargs):
        """
        Método que trata a adição da quantidade de produtos ao estoque.
        """
        if self.pk and not self.add_estoque:
            
            # Soma a quantidade de produtos comprados com a que já existe no estoque
            compra = Compra.objects.get(pk=self.compras.pk)
            super(ItensCompra, self).save(*args, **kwargs)

            if compra.pedido == 'N' or (compra.pedido == 'S' and compra.status_pedido):
                self.add_estoque = True
                self.save()

                produto = Produtos.objects.get(pk=self.produto.pk)
                produto.quantidade = produto.quantidade + self.quantidade
                produto.save()

        else:

            super(ItensCompra, self).save(*args, **kwargs)



# Importado no final do arquivo para não ocorrer problemas com dependencia circular 
from contas_pagar.models import ContasPagar, ParcelasContasPagar
