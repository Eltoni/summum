#-*- coding: UTF-8 -*-
from django.db import models
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

import datetime
from decimal import Decimal

from contas_receber.models.recebimento import Recebimento
from utilitarios.calculos_encargos import EncargoSimples, EncargoCompostos
from utilitarios.funcoes import lista_status_parcela


@python_2_unicode_compatible
class ParcelasContasReceber(models.Model):
    u""" 
    Classe ParcelasContasReceber. 

    Criada em 22/09/2014.  
    """
    
    vencimento = models.DateField(db_index=True, verbose_name=_(u"Data de vencimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor")) 
    status = models.BooleanField(default=False, db_index=True, verbose_name=_(u"Status"))
    num_parcelas = models.IntegerField(verbose_name=_(u"Nº Parcela"))
    contas_receber = models.ForeignKey('ContasReceber', on_delete=models.PROTECT, verbose_name=_(u"Conta a receber"))

    zero  = Decimal(0.00).quantize(Decimal("0.00"))
    data = datetime.date.today()

    class Meta(object):
        verbose_name = _(u"Parcela de Conta a Receber")
        verbose_name_plural = _(u"Parcelas de Contas a Receber")
        permissions = ((u"pode_exportar_parcelascontasreceber", _(u"Exportar Parcelas de Contas a Receber")),)


    def __str__(self):
        return u'%s' % (self.id)


    def conta_associada(self):
        if self.contas_receber:
            url = reverse("admin:contas_receber_contasreceber_change", args=[self.contas_receber])
            return u"<a href='%s' target='_blank'>%s</a>" % (url, self.contas_receber)
        return '-'
    conta_associada.allow_tags = True
    conta_associada.short_description = _(u"Conta a receber")
    conta_associada.admin_order_field = 'contas_receber'


    def quant_dias_vencidos(self):

        if self.pk and self.vencimento < self.data:
            data_primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).values_list('data')
            if not data_primeiro_recebimento:
                dias_vencidos = self.data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                dias_vencidos = data_primeiro_recebimento[0][0].date() - self.vencimento
                dias_vencidos = dias_vencidos.days

                if dias_vencidos <= 0:
                    return 0

            return dias_vencidos
        return 0
    quant_dias_vencidos.short_description = _(u"Quantidade de dias vencidos")


    def calculo_juros(self):
        u""" 
        Retorna o valor cálculado dos juros de acordo com a parametrização feita no grupo de encargos selecionado para a conta a pagar 
        """

        if self.pk and self.vencimento < self.data:
            
            percentual_juros = self.contas_receber.grupo_encargo.juros
            tipo_juros = self.contas_receber.grupo_encargo.tipo_juros

            if self.quant_dias_vencidos() <= 0:
                return self.zero

            if tipo_juros == 'S':
                return EncargoSimples(self.valor, percentual_juros, self.quant_dias_vencidos()).calcular_juros()

            if tipo_juros == 'C':
                return EncargoCompostos(self.valor, percentual_juros, self.quant_dias_vencidos()).calcular_juros()
            
        return self.zero
    calculo_juros.short_description = _(u"Juros")


    def calculo_multa(self):
        u""" 
        Retorna o valor calculado da multa.
        Caso a parcela seja vencida, a mesma sofre acréscimo no valor de acordo o percentual parametrizado no grupo de encargo.
        O valor da multa é único. Sendo assim, independe a quantidade de dias que a parcela está vencida, isto é, 1, 10, 100 dias de vencimento, o valor da multa será o mesmo.  
        """

        if self.pk and self.vencimento < self.data:

            percentual_multa = self.contas_receber.grupo_encargo.multa

            if self.quant_dias_vencidos() <= 0:
                return self.zero

            return EncargoSimples(self.valor, percentual_multa, self.quant_dias_vencidos()).calcular_multa()

        return self.zero
    calculo_multa.short_description = _(u"Multa")


    def encargos_calculados(self):
        u""" 
        Retorna o valor total dos encargos de multa e juros calculados 
        """

        valor_total_encargos = Decimal(self.calculo_juros() + self.calculo_multa()).quantize(Decimal("0.00"))
        return valor_total_encargos
    encargos_calculados.short_description = _(u"Encargos")


    def encargos_pagos(self):
        u""" 
        Retorna o valor pago dos encargos cobrados da parcela
        """
        if self.pk:
            encargos_pagos = Decimal(self.valor_pago() - self.valor).quantize(Decimal("0.00"))
            if encargos_pagos < 0.00:
                return self.zero
            else:
                return encargos_pagos
        return 0.00
    encargos_pagos.short_description = _(u"Encargos Pagos")


    def encargos_a_pagar(self):
        u""" 
        Retorna o valor a pagar dos encargos cobrados da parcela
        """
        if self.pk:
            encargos_a_pagar = Decimal(self.valor_total() - self.valor - self.encargos_pagos()).quantize(Decimal("0.00"))
            if encargos_a_pagar < 0.00:
                return self.zero
            else:
                return encargos_a_pagar
        return 0.00
    encargos_a_pagar.short_description = _(u"Encargos a Pagar")


    def valor_desconto(self):
        u""" 
        Retorna o valor total dos descontos aplicados a parcela
        """

        valor_desconto = Recebimento.objects.filter(parcelas_contas_receber=self.pk).aggregate(Sum('desconto'))
        valor_desconto = valor_desconto["desconto__sum"]
        return valor_desconto or self.zero
    valor_desconto.short_description = _(u"Descontos")
    

    def valor_total(self):
        u""" 
        Retorna o valor total da parcela com os encargos cálculados (valor juro + valor multa + valor parcela) 
        """

        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk:
            valor_total = Decimal(self.valor + self.encargos_calculados() - self.valor_desconto()).quantize(Decimal("0.00"))
            return valor_total or 0.00
        return 0.00
    valor_total.short_description = _(u"Valot Total")


    def valor_pago(self):

        valor_pago = Recebimento.objects.filter(parcelas_contas_receber=self.pk).aggregate(Sum('valor'))
        valor_pago = valor_pago["valor__sum"]
        return valor_pago or self.zero
    valor_pago.short_description = _(u"Valor Pago")


    def valor_a_receber(self):
        parcela_recebimentos = Recebimento.objects.filter(parcelas_contas_receber=self.pk).aggregate(Sum('valor'))
        parcela_recebimentos = parcela_recebimentos["valor__sum"]
        valor_a_receber = Decimal(self.valor_total()).quantize(Decimal("0.00")) - (self.zero if not parcela_recebimentos else parcela_recebimentos)
        return valor_a_receber
    valor_a_receber.short_description = _(u"Valor a Receber")


    def status_parcela(self):
        lsp = lista_status_parcela()

        if self.valor_pago() >= self.valor_total():
            return lsp[0] #Pago

        if self.valor_total() > self.valor_pago() and self.valor_pago() > 0.00:
            return lsp[1] #Pago Parcial

        if self.vencimento < self.data:
            return lsp[2] #Vencido

        else: 
            return lsp[3] #Em aberto


    def cor_valor_pago(self):
        return u"<p style='color:%(cor_p)s;'>%(valor)s</p>" % {'cor_p': self.status_parcela()[0], 'valor': self.valor_pago()}
    cor_valor_pago.allow_tags = True
    cor_valor_pago.short_description = _(u"Valor Recebido")


    def acoes_parcela(self):
        url = reverse("admin:contas_receber_recebimento_changelist")
        return u"<div class='btn-group'>                                                         \
                    <button class='btn btn-small dropdown-toggle' data-toggle='dropdown'>        \
                        Ações   <span class='caret'></span>                                      \
                    </button>                                                                    \
                    <ul class='dropdown-menu'>                                                   \
                        <li>                                                                     \
                            <a href='%(url)sefetiva_recebimento_parcela/%(pk)s' class='modal-recebimento modal-main-custom' name='_return_id_parcela'><i class='icon-tag'></i>&nbsp;&nbsp;%(desc_p)s</a> \
                        </li>                                                                    \
                        <li>                                                                     \
                            <a href='%(url)srecebimentos_parcela/%(pk)s' class='modal-rel-recebimentos modal-main-custom'><i class='icon-tags'></i>&nbsp;&nbsp;%(desc_al)s</a> \
                        </li>                                                                    \
                    </ul>                                                                        \
                </div>" % {'url': url, 'pk': self.pk, 'desc_p': _(u"Receber"), 'desc_al': _(u"Recebimentos Realizados"),}
    acoes_parcela.allow_tags = True
    acoes_parcela.short_description = u''


    def formata_data(obj):
        return obj.vencimento.strftime('%d/%m/%Y')
    formata_data.short_description = _(u"Vencimento")


    # def save(self, *args, **kwargs):
    #     """
    #     Método que trata a adição dos recebimentos.
    #     """

    #     data = datetime.date.today()

    #     if self.pk is None:
    #         super(ParcelasContasReceber, self).save(*args, **kwargs)

    #     else:
    #         super(ParcelasContasReceber, self).save(*args, **kwargs)
            
    #         # Bloqueio para criar somente pagamento de parcelas que ainda não foram pagas.
    #         if not Recebimento.objects.filter(parcelas_contas_receber__pk=self.pk).exists():
    #             # Cria o pagamento caso o checkbox de status seja selecionado
    #             Recebimento(data=data, 
    #                         valor=self.valor, 
    #                         juros=0.00, 
    #                         desconto=0.00, 
    #                         parcelas_contas_receber=self
    #                         ).save()
    #         else: 
    #             # Faz o save no pagamento já efetuado para atualizar o status da conta
    #             recebimento = Recebimento.objects.get(parcelas_contas_receber__pk=self.pk).save()


    # def cliente_associado(self):
    #     ParcelasContasReceber.objects.filter(contas_receber__cliente=1).values_list('contas_receber__cliente')
    #     return self.vendas
    # venda_associada.short_description = 'Venda'

    # def cliente_associado(self):
    #     try:
    #         return self.contas_receber.cliente
    #     except ValueError:
    #         pass