#-*- coding: UTF-8 -*-
from django.db import models
from compra.models import Compra
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento
from django.db.models.signals import post_save
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days
import datetime


class ContasPagar(models.Model):
    u""" 
    Classe ContasPagar. 

    Criada em 22/09/2014. 
    """

    data = models.DateField() 
    valor_total = models.DecimalField(max_digits=20, decimal_places=2) 
    status = models.BooleanField(default=False, verbose_name=u'Conta fechada', help_text=u'Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada.')
    descricao = models.TextField(blank=True, verbose_name=u'Descrição') 
    compras = models.ForeignKey(Compra, null=True, verbose_name=u'Compra') 
    fornecedores = models.ForeignKey(Fornecedor, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento) 

    class Meta:
        verbose_name = u'Conta à Pagar'
        verbose_name_plural = "Contas à Pagar"


    def __unicode__(self):
        return u'%s' % (self.id)


    def compra_associada(self):
        if self.compras:
            return self.compras
        return '-'
    compra_associada.short_description = 'Compra'


    def prazo_primeira_parcela(self, data, num_parcela):
        """
        Método que define a data de vencimento da primeira parcela baseado na parametrização da forma de pagamento.

        Parâmetros passados (data_da_compra, número_da_parcela) 
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

        Parâmetros passados (data_da_compra) 
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
        Caso ocorra, a última parcela da compra recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_compra)
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


    def pagamento_primeira_parcela_compra(self, num_parcela):
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
        Método que trata a geração e cálculo de contas à pagar.
        """
        data = datetime.date.today()

        forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quantidade_parcelada = forma_pagamento_conta.quant_parcelas
        
        if self.pk is None:
            # Chama a função save original para o save atual do modelo
            super(ContasPagar, self).save(*args, **kwargs)

            # Insere as parcelas do contas à pagar
            for i in range(quantidade_parcelada):                
                parcelas_conta = ParcelasContasPagar()
                data = self.prazo_primeira_parcela(data, i)
                parcelas_conta.vencimento = data
                data = self.prazo_entre_parcelas(data)
                parcelas_conta.valor = self.valor_parcela(i, self.valor_total)
                parcelas_conta.status = self.pagamento_primeira_parcela_compra(i)
                parcelas_conta.num_parcelas = i + 1
                parcelas_conta.contas_pagar = self
                parcelas_conta.save()

            # Insere o pagamento de uma compra que tenha o prazo de carência 0(zero) na parametrização da forma de pagamento. 
            try:
                parcela_paga = ParcelasContasPagar.objects.get(contas_pagar=self, status=True)
                Pagamento(  data=data, 
                            valor=parcela_paga.valor, 
                            juros=0.00, 
                            desconto=0.00, 
                            parcelas_contas_pagar=parcela_paga
                            ).save()
            except ParcelasContasPagar.DoesNotExist:
                pass
        
        else:
            # tratar cancelamento de compra efetuada
            super(ContasPagar, self).save(*args, **kwargs)


        # Atualiza o status da conta à pagar indicando se a compra está fechada, ou tem parcelas em aberto.
        # conta_aberta = ParcelasContasPagar.objects.filter(contas_pagar=self, status=0).exists()
        # if conta_aberta and self.status:
        #     self.status = False
        #     self.save()
        # if not conta_aberta and not self.status:
        #     self.status = True
        #     self.save()



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


    def save(self, *args, **kwargs):
        """
        Método que trata a adição dos pagamentos.
        """

        data = datetime.date.today()

        if self.pk is None:
            super(ParcelasContasPagar, self).save(*args, **kwargs)

        else:
            super(ParcelasContasPagar, self).save(*args, **kwargs)
            
            # Bloqueio para criar somente pagamento de parcelas que ainda não foram pagas.
            if not Pagamento.objects.filter(parcelas_contas_pagar__pk=self.pk).exists():
                # Cria o pagamento caso o checkbox de status seja selecionado
                Pagamento(  data=data, 
                            valor=self.valor, 
                            juros=0.00, 
                            desconto=0.00, 
                            parcelas_contas_pagar=self
                            ).save()



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
        conta_avulsa = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__descricao', flat=True)[0]
        descricao = u'Pagamento avulso. %s' % (conta_avulsa[:50])

    # Insere os itens de saída de movimentos de caixa
    MovimentosCaixa(descricao=descricao, 
                    valor=instance.valor,
                    data=instance.data, 
                    tipo_mov='Débito', 
                    caixa=Caixa.objects.get(status=1),
                    pagamento=instance
                    ).save()


    #Atualiza o status da conta à pagar indicando se a compra está fechada, ou tem parcelas em aberto.
    conta_aberta = ParcelasContasPagar.objects.filter(contas_pagar=conta[0], status=0).exists()
    conta_pagar = ContasPagar.objects.get(pk=conta[0])

    if conta_aberta:
        conta_pagar.status = False
        conta_pagar.save()
    else:
        conta_pagar.status = True
        conta_pagar.save()


# registro da signal
post_save.connect(update_movimento_caixa, sender=Pagamento, dispatch_uid="update_movimento_caixa")