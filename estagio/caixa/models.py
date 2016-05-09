#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from datetime import datetime


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
    : diferenca         : diferença calculada automaticamente entre o valor_total e o valor_fechamento 
                         (calculado de acordo com as mov. de caixa do sistema - valor informado manualmente)
    
    valor_inicial e valor_fechamento são referentes ao valor monetário existente no caixa. Ambos devem ser informados.
    diferenca> tem como objetivo principal saber se o que tem no caixa é o mesmo valor que foi calculado pelo sistema.
    
    """
    status = models.BooleanField(
        default=True, 
        db_index=True, 
        verbose_name=_(u"Status"), 
        help_text=_(u"Desmarque o Checkbox para indicar que o caixa está fechado.")
    )
    data_abertura = models.DateTimeField(
        null=True, 
        db_index=True, 
        verbose_name=_(u"Data de abertura"), 
        help_text=_(u"Data de abertura do caixa.")
    )
    data_fechamento = models.DateTimeField(
        null=True, 
        db_index=True, 
        verbose_name=_(u"Data de fechamento"), 
        help_text=_(u"Data de fechamento do caixa.")
    )
    valor_entrada = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Valor de entrada"), 
        help_text=_(u"Somatório de todos os recebimentos (mov. do tipo Crédito).")
    )
    valor_saida = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Valor de saída"), 
        help_text=_(u"Somatório de todos os pagamentos (mov. do tipo Débito).")
    )
    valor_total = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Valor total"), 
        help_text=_(u"Valor calculado automaticamente da quantia existente no Caixa em seu fechamento.")
    )
    valor_inicial = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Valor inicial"), 
        help_text=_(u"Valor existente no Caixa em sua abertura.")
    )
    valor_fechamento = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Valor de fechamento"), 
        help_text=_(u"Valor calculado manualmente da quantia existente no Caixa em seu fechamento.")
    )
    diferenca = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=0.00, 
        verbose_name=_(u"Diferença"), 
        help_text=_(u"Diferença do Valor Total calculado junto ao valor informado no fechamento do Caixa.")
    )

    class Meta(object):
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
    data = models.DateTimeField(db_index=True, verbose_name=_(u"Data de movimento"))
    tipo_mov = models.CharField(max_length=45, db_index=True, verbose_name=_(u"Tipo de movimento"))
    caixa = models.ForeignKey('Caixa', on_delete=models.PROTECT, verbose_name=_(u"Caixa"))
    pagamento = models.ForeignKey('contas_pagar.Pagamento', on_delete=models.PROTECT, blank=True, null=True, verbose_name=_(u"Pagamento"))
    recebimento = models.ForeignKey('contas_receber.Recebimento', on_delete=models.PROTECT, blank=True, null=True, verbose_name=_(u"Recebimento"))

    class Meta(object):
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