#-*- coding: UTF-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Pagamento(models.Model):
    u""" 
    Classe Pagamento. 
    Criada para registrar todas as saídas financeiras do estabelecimento.
    Os registros de pagamentos entrarão automaticamente na tabela. 
    Contudo, também será possível cadastrar pagamentos manualmente, pensando em casos em que valores são pagos, 
    eventualmente, sem a compra ter sido cadastrada.

    Criada em 16/06/2014. 
    """
    
    data = models.DateTimeField(db_index=True, verbose_name=_(u"Data do pagamento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_pagar = models.ForeignKey('ParcelasContasPagar', on_delete=models.PROTECT, verbose_name=_(u"Pagamento de parcela"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"))
    
    def __str__(self):
        return u'%s' % (self.id)


    def conta_associada(self):
        if self.parcelas_contas_pagar:
            url = reverse("admin:contas_pagar_contaspagar_change", args=[self.parcelas_contas_pagar.contas_pagar])
            return u"<a href='%s'>%s</a>" % (url, self.parcelas_contas_pagar.contas_pagar)
        return '-'
    conta_associada.allow_tags = True
    conta_associada.short_description = _(u"Conta a pagar")
    conta_associada.admin_order_field = 'parcelas_contas_pagar__contas_pagar'
    

    def save(self, *args, **kwargs):
        from contas_pagar.models import ContasPagar, ParcelasContasPagar

        if self.pk is None:
            super(Pagamento, self).save(*args, **kwargs)
            parcela_pagamento = Pagamento.objects.filter(pk=self.pk).values_list('parcelas_contas_pagar')[0]

            parcela = ParcelasContasPagar.objects.get(pk=parcela_pagamento[0])
            if parcela.valor_pago() >= parcela.valor_total():
                parcela.status = True
                parcela.save()

                #Atualiza o status da conta à pagar indicando se a compra está fechada, ou tem parcelas em aberto.
                conta_pagar = ContasPagar.objects.get(pk=parcela.contas_pagar.pk)
                conta_aberta = ParcelasContasPagar.objects.filter(contas_pagar=conta_pagar.pk, status=0).exists()
                if conta_aberta:
                    conta_pagar.status = False
                    conta_pagar.save()
                else:
                    conta_pagar.status = True
                    conta_pagar.save()
        else:
            super(Pagamento, self).save(*args, **kwargs)
            

