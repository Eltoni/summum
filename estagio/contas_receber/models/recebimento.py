#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from configuracoes.models import *
from contas_receber.models.parcela_conta_receber import ParcelasContasReceber
from contas_receber.models.conta_receber import ContasReceber
from django.core.urlresolvers import reverse


@python_2_unicode_compatible
class Recebimento(models.Model):
    u""" 
    Classe Recebimento. 
    Criada para registrar todas as entradas financeiras do estabelecimento.
    Os registros de recebimentos entrarão automaticamente na tabela. 

    Criada em 15/06/2014. 
    """

    data = models.DateTimeField(verbose_name=_(u"Data do recebimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber, on_delete=models.PROTECT, verbose_name=_(u"Recebimento de parcela"))
    observacao = models.TextField(blank=True, verbose_name=_(u"Observações"))

    class Meta:
        verbose_name = _(u"Recebimento")
        verbose_name_plural = _(u"Recebimentos")


    def __str__(self):
        return u'%s' % (self.id)


    def conta_associada(self):
        if self.parcelas_contas_receber:
            url = reverse("admin:contas_receber_contasreceber_change", args=[self.parcelas_contas_receber.contas_receber])
            return u"<a href='%s'>%s</a>" % (url, self.parcelas_contas_receber.contas_receber)
        return '-'
    conta_associada.allow_tags = True
    conta_associada.short_description = _(u"Conta a receber")
    conta_associada.admin_order_field = 'parcelas_contas_receber__contas_receber'


    def save(self, *args, **kwargs):

        if self.pk is None:
            super(Recebimento, self).save(*args, **kwargs)
            parcela_recebimento = Recebimento.objects.filter(pk=self.pk).values_list('parcelas_contas_receber')[0]

            parcela = ParcelasContasReceber.objects.get(pk=parcela_recebimento[0])
            if parcela.valor_pago() >= parcela.valor_total():
                parcela.status = True
                parcela.save()

                #Atualiza o status da conta à receber indicando se a venda está fechada, ou tem parcelas em aberto.
                conta_receber = ContasReceber.objects.get(pk=parcela.contas_receber.pk)
                conta_aberta = ParcelasContasReceber.objects.filter(contas_receber=conta_receber.pk, status=0).exists()
                if conta_aberta:
                    conta_receber.status = False
                    conta_receber.save()
                else:
                    conta_receber.status = True
                    conta_receber.save()
        else:
            super(Recebimento, self).save(*args, **kwargs)