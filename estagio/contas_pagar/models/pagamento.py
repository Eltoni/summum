#-*- coding: UTF-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

from configuracoes.models import *
from contas_pagar.models.parcela_conta_pagar import ParcelasContasPagar
from contas_pagar.models.conta_pagar import ContasPagar


@python_2_unicode_compatible
class Pagamento(models.Model):
    u""" 
    Classe Pagamento. 
    Criada para registrar todas as saídas financeiras do estabelecimento.
    Os registros de pagamentos entrarão automaticamente na tabela. 
    Contudo, também será possível cadastrar pagamentos manualmente, pensando em casos em que valores são pagos, eventualmente, sem a compra ter sido cadastrada.

    Criada em 16/06/2014. 
    """
    
    data = models.DateTimeField(db_index=True, verbose_name=_(u"Data do pagamento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_pagar = models.ForeignKey(ParcelasContasPagar, on_delete=models.PROTECT, verbose_name=_(u"Pagamento de parcela"))
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

    # # O pagamento não é mais realizado no formulário original do Django, deste modo, o tratamento abaixo foi transferido para a view "efetiva_pagamento_parcela" que processa a efetivação do pagamento
    # def clean(self):
    #     u""" 
    #     Bloqueia os pagamentos parciais que forem abaixo do percentual mínimo parametrizado nas configurações do sistema.
    #     Bloqueia somente o primeiro pagamento da parcela.

    #     Bloqueia a tentativa de efetuar um pagamento enquanto não houver caixa aberto no sistema.
    #     Bloqueia quaisquer alterações num registro de pagamento enquanto não houver caixa aberto no sistema.
    #     """
    #     # Checa a situação do caixa
    #     from caixa.models import Caixa
    #     if not Caixa.objects.filter(status=1).exists() and not self.pk:
    #         raise ValidationError(_(u"Não há caixa aberto. Para efetivar um pagamento é necessário ter o caixa aberto."))

    #     if not Caixa.objects.filter(status=1).exists() and self.pk:
    #         raise ValidationError(_(u"Não há caixa aberto. Alterações num pagamento só podem ser efetivados após a abertura do caixa."))

    #     # Checa a situação do valor do pagamento
    #     perc_valor_minimo_pagamento = Parametrizacao.objects.all().values_list('perc_valor_minimo_pagamento')[0][0]
        
    #     parcela = ParcelasContasPagar.objects.get(pk=self.parcelas_contas_pagar.pk)
    #     valor_minimo_pagamento = round((parcela.valor_total() * perc_valor_minimo_pagamento) / 100, 2)
    #     primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.parcelas_contas_pagar.pk).exists()
    #     if self.valor < valor_minimo_pagamento and not primeiro_pagamento:
    #         raise ValidationError(_(u"Primeiro pagamento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_pagamento, 'valor_minimo': valor_minimo_pagamento})


    def save(self, *args, **kwargs):

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
            