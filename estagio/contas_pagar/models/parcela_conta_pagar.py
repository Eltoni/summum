#-*- coding: UTF-8 -*-
from django.db import models
from parametros_financeiros.models import GrupoEncargo
from utilitarios.calculos_encargos import EncargoSimples, EncargoCompostos
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from contas_pagar.models.conta_pagar import ContasPagar


@python_2_unicode_compatible
class ParcelasContasPagar(models.Model):
    u""" 
    Classe ParcelasContasPagar. 

    Criada em 22/09/2014.  
    """

    vencimento = models.DateField(verbose_name=_(u"Data de vencimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor")) 
    status = models.BooleanField(default=False, verbose_name=_(u"Status"))
    num_parcelas = models.IntegerField(verbose_name=_(u"Nº Parcela"))
    contas_pagar = models.ForeignKey(ContasPagar, on_delete=models.PROTECT, verbose_name=_(u"Conta a pagar"))

    zero  = Decimal(0.00).quantize(Decimal("0.00"))
    data = datetime.date.today()

    class Meta:
        verbose_name = _(u"Parcela de Conta a Pagar")
        verbose_name_plural = _(u"Parcelas de Contas a Pagar")
        permissions = ((u"pode_exportar_parcelascontaspagar", _(u"Exportar Parcelas de Contas a Pagar")),)


    def __str__(self):
        return u'%s' % (self.id)


    def conta_associada(self):
        if self.contas_pagar:
            url = reverse("admin:contas_pagar_contaspagar_change", args=[self.contas_pagar])
            return u"<a href='%s' target='_blank'>%s</a>" % (url, self.contas_pagar)
        return '-'
    conta_associada.allow_tags = True
    conta_associada.short_description = _(u"Conta a pagar")
    conta_associada.admin_order_field = 'contas_pagar'


    def quant_dias_vencidos(self):

        if self.pk and self.vencimento < self.data:
            data_primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).values_list('data')
            if not data_primeiro_pagamento:
                dias_vencidos = self.data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                dias_vencidos = data_primeiro_pagamento[0][0].date() - self.vencimento
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
            
            percentual_juros = self.contas_pagar.grupo_encargo.juros
            tipo_juros = self.contas_pagar.grupo_encargo.tipo_juros
            
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
            
            percentual_multa = self.contas_pagar.grupo_encargo.multa

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


    def valor_desconto(self):
        u""" 
        Retorna o valor total dos descontos aplicados a parcela
        """

        valor_desconto = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('desconto'))
        valor_desconto = valor_desconto["desconto__sum"]
        return valor_desconto or self.zero
    valor_desconto.short_description = _(u"Descontos")


    def valor_total(self):
        u""" 
        Retorna o valor total da parcela com os encargos cálculados (valor juro + valor multa + valor mensalidade) 
        """
        
        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk:
            valor_total = Decimal(self.valor + self.encargos_calculados() - self.valor_desconto()).quantize(Decimal("0.00"))
            return valor_total or self.zero
        return self.zero
    valor_total.short_description = _(u"Valot Total")


    def valor_pago(self):

        valor_pago = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor'))
        valor_pago = valor_pago["valor__sum"]
        return valor_pago or self.zero
    valor_pago.short_description = _(u"Valor Pago")


    def valor_a_pagar(self):
        parcela_pagamentos = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor'))
        parcela_pagamentos = parcela_pagamentos["valor__sum"]
        valor_a_pagar = Decimal(self.valor_total()).quantize(Decimal("0.00")) - (self.zero if not parcela_pagamentos else parcela_pagamentos)
        return valor_a_pagar
    valor_a_pagar.short_description = _(u"Valor a Pagar")


    def status_parcela(self):
        if self.valor_pago() >= self.valor_total():
            return ('#2DB218', _(u'Pago')) #Pago

        if self.valor_total() > self.valor_pago() and self.valor_pago() > 0.00:
            return ('#355EED', _(u'Pago Parcialmente')) #Pago Parcial

        if self.vencimento < self.data:
            return ('#E8262A', _(u'Vencido')) #Vencido

        else: 
            return ('#333333', _(u'Em aberto')) #Em aberto


    def cor_valor_pago(self):
        return u"<p style='color:%(cor_p)s;'>%(valor)s</p>" % {'cor_p': self.status_parcela()[0], 'valor': self.valor_pago()}
    cor_valor_pago.allow_tags = True
    cor_valor_pago.short_description = _(u"Valor Pago")


    def acoes_parcela(self):
        url = reverse("admin:contas_pagar_pagamento_changelist")
        return u"<div class='btn-group'>                                                         \
                    <button class='btn btn-small dropdown-toggle' data-toggle='dropdown'>        \
                        Ações   <span class='caret'></span>                                      \
                    </button>                                                                    \
                    <ul class='dropdown-menu'>                                                   \
                        <li>                                                                     \
                            <a href='%(url)sefetiva_pagamento_parcela/%(pk)s' class='modal-pagamento modal-main-custom' name='_return_id_parcela'><i class='icon-tag'></i>&nbsp;&nbsp;%(desc_p)s</a> \
                        </li>                                                                    \
                        <li>                                                                     \
                            <a href='%(url)spagamentos_parcela/%(pk)s' class='modal-rel-pagamentos modal-main-custom'><i class='icon-tags'></i>&nbsp;&nbsp;%(desc_al)s</a> \
                        </li>                                                                    \
                        <!--<li>                                                                     \
                            <a href='%(url)sestorno_parcela/%(pk)s'><i class='icon-minus-sign'></i>&nbsp;&nbsp;%(desc_est)s</a> \
                        </li>-->                                                                    \
                    </ul>                                                                        \
                </div>" % {'url': url, 'pk': self.pk, 'desc_p': _(u"Pagar"), 'desc_al': _(u"Pagamentos Realizados"), 'desc_est': _(u"Estornar Parcela"),}
    acoes_parcela.allow_tags = True
    acoes_parcela.short_description = u''


    def formata_data(obj):
      return obj.vencimento.strftime('%d/%m/%Y')
    formata_data.short_description = _(u"Vencimento")


    # def save(self, *args, **kwargs):
    #     u"""
    #     Método que trata a adição dos pagamentos.
    #     """

    #     data = datetime.date.today()

    #     if self.pk is None:
    #         super(ParcelasContasPagar, self).save(*args, **kwargs)

    #     else:
    #         super(ParcelasContasPagar, self).save(*args, **kwargs)
            
    #         # Bloqueio para criar somente pagamento de parcelas que ainda não foram pagas.
    #         if not Pagamento.objects.filter(parcelas_contas_pagar__pk=self.pk).exists():
    #             # Cria o pagamento caso o checkbox de status seja selecionado
    #             Pagamento(  data=data, 
    #                         valor=self.valor, 
    #                         juros=0.00, 
    #                         desconto=0.00, 
    #                         parcelas_contas_pagar=self
    #                         ).save()
    #         else: 
    #             # Faz o save no pagamento já efetuado para atualizar o status da conta
    #             pagamento = Pagamento.objects.get(parcelas_contas_pagar__pk=self.pk).save()

from contas_pagar.models.pagamento import Pagamento