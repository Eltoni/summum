#-*- coding: UTF-8 -*-
from django.db import models
from contas_pagar.models import ContasPagar, ParcelasContasPagar, Pagamento
from contas_receber.models import ContasReceber, ParcelasContasReceber, Recebimento
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from datetime import datetime
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Caixa(models.Model):
    u"""
    : status            : indica se o caixa está aberto/fechado
    : data_abertura     : data de abertura do caixa
    : data_fechamento   : data de fechamento do caixa
    : valor_entrada     : somatória de todas entradas (mov do tipo crédito) com o ID desse caixa
    : valor_saida       : somatória de todas saídas (mov do tipo débito) com o ID desse caixa
    : valor_total       : valor_inicial + (valor_entrada - valor_saida) (valor_inicial + (valor_entrada menos o valor_saida), pois o caixa pode ser negativo)
    : valor_inicial     : é o valor (R$) que existe no caixa quando ele for aberto
    : valor_fechamento  : é o valor (R$) que existe no caixa quando ele for fechado
    : diferenca         : diferença calculada automaticamente entre o valor_total e o valor_fechamento (calculado de acordo com as mov. de caixa do sistema - valor informado manualmente)
    
    valor_inicial e valor_fechamento são referentes ao valor monetário existente no caixa. Ambos devem ser informados.
    diferenca> tem como objetivo principal saber se o que tem no caixa é o mesmo valor que foi calculado pelo sistema.
    
    """
    status = models.BooleanField(default=True, verbose_name=_(u"Status"), help_text=_(u"Desmarque o Checkbox para indicar que o caixa está fechado."))
    data_abertura = models.DateTimeField(null=True, verbose_name=_(u"Data de abertura"))
    data_fechamento = models.DateTimeField(null=True, verbose_name=_(u"Data de fechamento"))
    valor_entrada = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Valor de entrada"))
    valor_saida = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Valor de saída"))
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Valor total"))
    valor_inicial = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    valor_fechamento = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Valor de fechamento"))
    diferenca = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Diferença"))

    class Meta:
        verbose_name = _(u"Caixa")
        verbose_name_plural = _(u"Caixas")
        permissions = ((u"pode_exportar_caixa", _(u"Exportar Caixas")),
                       (u"recebe_notificacoes_caixa", _(u"Receber notificações de caixa.")),)


    def __str__(self):
        return u'%s' % (self.id)


    def formata_data_fechamento(self):
        if self.data_fechamento:
            return self.data_fechamento
        return '-'
    formata_data_fechamento.allow_tags = True
    formata_data_fechamento.short_description = _(u"Data de fechamento")
    formata_data_fechamento.admin_order_field = 'data_fechamento'
        

    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo do Caixa.
        """

        data = datetime.now()

        if self.pk:

            status_antigo = Caixa.objects.get(pk=self.pk)
            super(Caixa, self).save(*args, **kwargs)
            # print u"Teste > Antes da verficicação do status. Novo status: %s. Status antigo: %s." % (self.status, status_antigo.status)
            if not self.status and status_antigo.status:
                self.valor_total = self.valor_inicial + (self.valor_entrada - self.valor_saida)
                self.diferenca = self.valor_fechamento - self.valor_total
                self.data_fechamento = data
                self.save()

        super(Caixa, self).save(*args, **kwargs)

        if self.status and self.data_abertura is None:
            self.data_abertura = data
            self.save() 



    def clean(self):
        """ 
        Não permite que seja aberto dois caixas ao mesmo tempo. Para abrir um caixa, não pode haver obrigatóriamente um outro com status ativo.
        Caso um usuário tente abri-lo nesse contexto, receberá mensagem informando o erro e o id do caixa atualmente aberto.
        """
        try:
            caixa_aberto = Caixa.objects.filter(status=1).exclude(pk=self.id)
        except Caixa.DoesNotExist:
            caixa_aberto = False

        if caixa_aberto and self.status == 1:
            raise ValidationError(_(u"Já há um caixa aberto. Para abrir este, é necessário fechar o caixa atualmente aberto (Caixa: %(caixa_aberto)s).") % {'caixa_aberto': caixa_aberto[0]})



@python_2_unicode_compatible
class MovimentosCaixa(models.Model):
    descricao = models.CharField(max_length=100, verbose_name=_(u"Descrição"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name=_(u"Valor"))
    data = models.DateTimeField(verbose_name=_(u"Data de movimento"))
    tipo_mov = models.CharField(max_length=45, verbose_name=_(u"Tipo de movimento"))
    caixa = models.ForeignKey(Caixa, on_delete=models.PROTECT, verbose_name=_(u"Caixa"))
    pagamento = models.ForeignKey(Pagamento, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_(u"Pagamento"))
    recebimento = models.ForeignKey(Recebimento, on_delete=models.PROTECT, blank=True, null=True, verbose_name=_(u"Recebimento"))

    class Meta:
        verbose_name = _(u"Movimento de Caixa")
        verbose_name_plural = _(u"Movimentos de Caixas")
        permissions = ((u"pode_exportar_movimentoscaixa", _(u"Exportar Movimentos de Caixas")),)

    def __str__(self):
        return u'%s' % (self.id)

    def pagamento_associado(self):
        if self.pagamento:
            return self.pagamento
        return '-'
    pagamento_associado.short_description = _(u"Pagamento")
    pagamento_associado.admin_order_field = 'pagamento'


    def recebimento_associado(self):
        if self.recebimento:
            return self.recebimento
        return '-'
    recebimento_associado.short_description = _(u"Recebimento")
    recebimento_associado.admin_order_field = 'recebimento'


    def save(self, *args, **kwargs):
        """
        Método que trata os movimentos do sistema de caixa
        """
        super(MovimentosCaixa, self).save(*args, **kwargs)

        caixa_aberto = Caixa.objects.get(status=1)

        if self.caixa == caixa_aberto:
            if self.tipo_mov == 'Crédito':
                caixa_aberto.valor_entrada = caixa_aberto.valor_entrada + self.valor
                caixa_aberto.save()

            if self.tipo_mov == 'Débito':
                caixa_aberto.valor_saida = caixa_aberto.valor_saida + self.valor
                caixa_aberto.save()



def update_movimento_caixa_pagamento(sender, instance, **kwargs):
    """ 
    Método para inserir na tabela de movimentos_de_caixa os movimentos de saída financeira.
    O mesmo age sobre o Movimento de Caixa e o Caixa, fazendo todo o cálculo para controle dessas entidades.

    Criada em 01/10/2014. 
    """

    # Não prossegue com o processamento caso não saia valor do caixa.
    if instance.valor <= 0:
        return

    # Busca o id da conta à pagar e da compra vinculado ao pagamento instanciado
    conta = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__pk', 'contas_pagar__compras')[0]
    
    # Condição que monta a descrição que é salvo no registro do movimento. Condiciona para descrições distintas caso o pagamento seja de uma conta avulsa, ou de uma conta vinculada a uma compra
    if conta[1]:
        descricao = _(u"Pagamento: %(pagamento)s, proveniente da parcela: %(parcela)s, da conta a pagar: %(conta_pagar)s, da compra: %(compra)s.") % {'pagamento': instance.pk, 'parcela': instance.parcelas_contas_pagar.pk, 'conta_pagar': conta[0], 'compra': conta[1]}
    
    else:
        conta_avulsa = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__descricao', flat=True)[0]
        descricao = _(u"Pagamento avulso. %(pagamento)s") % {'pagamento': conta_avulsa[:50]}

    # Insere os itens de saída de movimentos de caixa
    movimento_caixa = MovimentosCaixa(  descricao=descricao, 
                                        valor=Decimal(instance.valor).quantize(Decimal("0.00")),
                                        data=instance.data, 
                                        tipo_mov='Débito', 
                                        caixa=Caixa.objects.get(status=1),
                                        pagamento=instance
                                        )
    # Não insere duas vezes se o pagamento existir e se o mesmo tiver o mesmo valor
    if MovimentosCaixa.objects.filter(pagamento__pk=instance.pk).exists():
        pass
    else:
        movimento_caixa.save()

# registro da signal
post_save.connect(update_movimento_caixa_pagamento, sender=Pagamento, dispatch_uid="update_movimento_caixa_pagamento")



def update_movimento_caixa_recebimento(sender, instance, **kwargs):
    """ 
    Método para ïnserir na tabela de movimentos_de_caixa os movimentos de entrada financeira.
    O mesmo age sobre o Movimento de Caixa e o Caixa, fazendo todo o cálculo para controle dessas entidades.

    Criada em 09/10/2014. 
    """

    # Não prossegue com o processamento caso não entre valor no caixa.
    if instance.valor <= 0:
        return

    # Busca o id da conta à receber e da compra vinculado ao recebimento instanciado
    conta = ParcelasContasReceber.objects.filter(pk=instance.parcelas_contas_receber.pk).select_related('contas_receber__contasreceber').values_list('contas_receber__pk', 'contas_receber__vendas')[0]
    
    # Condição que monta a descrição que é salvo no registro do movimento. Condiciona para descrições distintas caso o recebimento seja de uma conta avulsa, ou de uma conta vinculada a uma compra
    if conta[1]:
        descricao = _(u"Recebimento: %(recebimento)s, proveniente da parcela: %(parcela)s, da conta a receber: %(conta_receber)s, da venda: %(venda)s.") % {'recebimento': instance.pk, 'parcela': instance.parcelas_contas_receber.pk, 'conta_receber': conta[0], 'venda': conta[1]}
    
    else:
        conta_avulsa = ParcelasContasReceber.objects.filter(pk=instance.parcelas_contas_receber.pk).select_related('contas_receber__contasreceber').values_list('contas_receber__descricao', flat=True)[0]
        descricao = _(u"Recebimento avulso. %(recebimento)s") % {'recebimento': conta_avulsa[:50]}

    # Insere os itens de saída de movimentos de caixa
    movimento_caixa = MovimentosCaixa(  descricao=descricao, 
                                        valor=Decimal(instance.valor).quantize(Decimal("0.00")),
                                        data=instance.data, 
                                        tipo_mov='Crédito', 
                                        caixa=Caixa.objects.get(status=1),
                                        recebimento=instance
                                        )
    # Não insere duas vezes se o recebimento existir e se o mesmo tiver o mesmo valor
    if MovimentosCaixa.objects.filter(recebimento__pk=instance.pk).exists():
        pass
    else:
        movimento_caixa.save()

# registro da signal
post_save.connect(update_movimento_caixa_recebimento, sender=Recebimento, dispatch_uid="update_movimento_caixa_recebimento")



