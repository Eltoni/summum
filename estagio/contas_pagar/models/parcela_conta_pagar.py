#-*- coding: UTF-8 -*-
from django.db import models
from parametros_financeiros.models import GrupoEncargo
from utilitarios.funcoes_data import date_settings_timezone
from utilitarios.calculos_encargos import calculo_composto, calculo_simples
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

    vencimento = models.DateField(verbose_name=_(u"Vencimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor")) 
    status = models.BooleanField(default=False, verbose_name=_(u"Status"))
    num_parcelas = models.IntegerField(verbose_name=_(u"Nº Parcela"))
    contas_pagar = models.ForeignKey(ContasPagar, on_delete=models.PROTECT, verbose_name=_(u"Conta a pagar"))

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


    def calculo_juros(self):
        u""" 
        Retorna o valor cálculado dos juros de acordo com a parametrização feita no grupo de encargos selecionado para a conta a pagar 
        """

        data = datetime.date.today()

        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk and self.vencimento < data:
            
            parametros_grupo_encargo = GrupoEncargo.objects.filter(pk=self.contas_pagar.grupo_encargo.pk).values_list('juros', 'tipo_juros')[0]
            # Percentual de multa
            percentual_juros = parametros_grupo_encargo[0] / 100
            
            # quantidade de dias em atraso
            existe_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).exists()
            if not existe_pagamento:
                dias_vencidos = data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                data_primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).values_list('data')[0][0]
                dias_vencidos = date_settings_timezone(data_primeiro_pagamento) - self.vencimento
                dias_vencidos = dias_vencidos.days

            if parametros_grupo_encargo[1] == 'S':
                return calculo_simples(self.valor, dias_vencidos, percentual_juros)

            if parametros_grupo_encargo[1] == 'C':
                return calculo_composto(self.valor, dias_vencidos, percentual_juros)
            
        return 0.00
    calculo_juros.short_description = _(u"Juros")


    def calculo_multa(self):
        u""" 
        Retorna o valor calculado da multa.
        Caso a parcela seja vencida, a mesma sofre acréscimo no valor de acordo o percentual parametrizado no grupo de encargo.
        O valor da multa é único. Sendo assim, independe a quantidade de dias que a parcela está vencida, isto é, 1, 10, 100 dias de vencimento, o valor da multa será o mesmo.  
        """

        data = datetime.date.today()

        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk and self.vencimento < data:
            
            percentual_multa = GrupoEncargo.objects.filter(pk=self.contas_pagar.grupo_encargo.pk).values_list('multa')[0][0]
            percentual_multa = percentual_multa / 100

            # quantidade de dias em atraso
            existe_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).exists()
            if not existe_pagamento:
                dias_vencidos = data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                data_primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).values_list('data')[0][0]
                dias_vencidos = date_settings_timezone(data_primeiro_pagamento) - self.vencimento
                dias_vencidos = dias_vencidos.days

            return calculo_simples(self.valor, dias_vencidos, percentual_multa)

        return 0.00
    calculo_multa.short_description = _(u"Multa")


    def encargos_calculados(self):
        u""" 
        Retorna o valor total dos encargos de multa e juros calculados 
        """

        valor_total_encargos = Decimal(self.calculo_juros() + self.calculo_multa()).quantize(Decimal("0.00"))
        return valor_total_encargos
    encargos_calculados.short_description = _(u"Encargos")


    def valor_total(self):
        u""" 
        Retorna o valor total da parcela com os encargos cálculados (valor juro + valor multa + valor mensalidade) 
        """
        
        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk:
            valor_total = Decimal(self.valor + self.encargos_calculados()).quantize(Decimal("0.00"))
            return valor_total or 0.00
        return 0.00
    valor_total.short_description = _(u"Valot Total")


    def valor_pago(self):

        valor_pago = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor'))
        valor_pago = valor_pago["valor__sum"]
        return valor_pago or Decimal(0.00).quantize(Decimal("0.00"))
    valor_pago.short_description = _(u"Valor Pago")


    def valor_a_pagar(self):
        parcela_pagamentos = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor'))
        parcela_pagamentos = parcela_pagamentos["valor__sum"]
        valor_a_pagar = Decimal(self.valor_total()).quantize(Decimal("0.00")) - (Decimal(0.00).quantize(Decimal("0.00")) if not parcela_pagamentos else parcela_pagamentos)
        return valor_a_pagar
    valor_a_pagar.short_description = _(u"Valor a Pagar")


    def status_parcela(self):
        data = datetime.date.today()
        if self.valor_pago() >= self.valor_total():
            return ('#2DB218', _(u'Pago')) #Pago

        if self.valor_total() > self.valor_pago() and self.valor_pago() > 0.00:
            return ('#355EED', _(u'Pago Parcialmente')) #Pago Parcial

        if self.vencimento < data:
            return ('#E8262A', _(u'Vencido')) #Vencido

        else: 
            return ('#333333', _(u'Em aberto')) #Em aberto


    def link_pagamentos_parcela(self):
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_pagar'})
        return format_html('<a href="{0}pagamento/pagamentos_parcela/{1}" target="_blank" style="color: {2};">{3}<span class="icon-share icon-alpha5 hint--bottom hint--bounce" style="position: relative; float: right; right: 20%;" rel="tooltip" data-hint="{4} {1}"</span></a>', url, self.pk, self.status_parcela()[0], self.valor_pago(), _(u"Visualize todos os pagamentos efetuados da parcela"))
    link_pagamentos_parcela.allow_tags = True
    link_pagamentos_parcela.short_description = _(u"Valor Pago")


    def link_pagamento(self):
        url = reverse("admin:contas_pagar_pagamento_changelist")
        return u"<a href='%(url)sefetiva_pagamento_parcela/%(pk)s' class='modal-pagamento' name='_return_id_parcela' rel='modal:open'>%(p)s</a>" % {'url': url, 'pk': self.pk, 'p': _(u"Pagar")}
    link_pagamento.allow_tags = True
    link_pagamento.short_description = u''


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