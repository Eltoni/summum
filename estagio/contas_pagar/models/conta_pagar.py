#-*- coding: UTF-8 -*-
from django.db import models
from compra.models import Compra
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days
from utilitarios.funcoes import pode_ver_link
from django.core.exceptions import ValidationError
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ContasPagar(models.Model):
    u""" 
    Classe ContasPagar. 

    Criada em 22/09/2014. 
    """

    data = models.DateTimeField(verbose_name=_(u"Data")) 
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor total")) 
    status = models.BooleanField(default=False, verbose_name=_(u"Conta fechada"), help_text=_(u"Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada."))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição")) 
    compras = models.ForeignKey(Compra, on_delete=models.PROTECT, null=True, verbose_name=_(u"Compra")) 
    fornecedores = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, null=True, verbose_name=_(u"Fornecedor"))
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, verbose_name=_(u"Forma de pagamento")) 
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=_(u"Grupo de encargo"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _(u"Conta a Pagar")
        verbose_name_plural = _(u"Contas a Pagar")
        permissions = ((u"pode_exportar_contaspagar", _(u"Exportar Contas a Pagar")),)


    def clean(self):
        u""" 
        Bloqueia o registro de uma conta a pagar avulsa quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar um cadastro de uma conta a pagar avulsa, é necessário ter o caixa aberto."))

        if not Caixa.objects.filter(status=1).exists() and self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Alterações numa conta a pagar só podem ser efetivadas após a abertura do caixa."))


    def __str__(self):
        return u'%s' % (self.id)


    def compra_associada(self):
        if self.compras:
            try:
                url = pode_ver_link(self.usuario_sessao, 'compra', 'compra', self.compras.pk)
            except:
                url = '#'
            return u"<a href='%s'>%s</a>" % (url, self.compras)
        return '-'
    compra_associada.allow_tags = True
    compra_associada.short_description = _(u"Compra")
    compra_associada.admin_order_field = 'compras'


    def fornecedor_associado(self):
        if self.fornecedores:
            url = pode_ver_link(self.usuario_sessao, 'pessoal', 'fornecedor', self.fornecedores.pk)
            return u"<a href='%s'>%s</a>" % (url, self.fornecedores)
        return '-'
    fornecedor_associado.allow_tags = True
    fornecedor_associado.short_description = _(u"Fornecedor")
    fornecedor_associado.admin_order_field = 'fornecedores'


    def forma_pagamento_associada(self):
        choices_tp = self.forma_pagamento._meta.get_field_by_name('tipo_prazo')[0].flatchoices
        tp = dict(choices_tp).get(self.forma_pagamento.tipo_prazo)
        choices_tp = self.forma_pagamento._meta.get_field_by_name('tipo_carencia')[0].flatchoices
        tc = dict(choices_tp).get(self.forma_pagamento.tipo_carencia)
        if self.forma_pagamento:
            url = pode_ver_link(self.usuario_sessao, 'parametros_financeiros', 'formapagamento', self.forma_pagamento.pk)
            return u"<a href='%s' rel='tooltip' data-hint='%s: %s&#10;&#10;%s: %s (%s)&#10;&#10;%s: %s (%s)' class='hint--right hint--bounce' target='_blank'>%s</a>" % ( url, 
                                                                                                                                                                          self.forma_pagamento._meta.get_field_by_name('quant_parcelas')[0].verbose_name,
                                                                                                                                                                          self.forma_pagamento.quant_parcelas,  
                                                                                                                                                                          self.forma_pagamento._meta.get_field_by_name('prazo_entre_parcelas')[0].verbose_name,                                                                                                                                                                                             
                                                                                                                                                                          self.forma_pagamento.prazo_entre_parcelas, 
                                                                                                                                                                          tp,
                                                                                                                                                                          self.forma_pagamento._meta.get_field_by_name('carencia')[0].verbose_name,
                                                                                                                                                                          self.forma_pagamento.carencia, 
                                                                                                                                                                          tc, 
                                                                                                                                                                          self.forma_pagamento )
        return '-'
    forma_pagamento_associada.allow_tags = True
    forma_pagamento_associada.short_description = _(u"Forma de pagamento")
    forma_pagamento_associada.admin_order_field = 'forma_pagamento'


    def grupo_encargo_associado(self):
        choices_tj = self.grupo_encargo._meta.get_field_by_name('tipo_juros')[0].flatchoices
        tj = dict(choices_tj).get(self.grupo_encargo.tipo_juros)
        if self.grupo_encargo:
            url = pode_ver_link(self.usuario_sessao, 'parametros_financeiros', 'grupoencargo', self.grupo_encargo.pk)
            return u"<a href='%s' rel='tooltip' data-hint='%s: %s&#10;&#10;%s: %s&#10;&#10;%s: %s' class='hint--right hint--bounce' target='_blank'>%s</a>" % ( url, 
                                                                                                                                                                self.grupo_encargo._meta.get_field_by_name('juros')[0].verbose_name,
                                                                                                                                                                self.grupo_encargo.juros,  
                                                                                                                                                                self.grupo_encargo._meta.get_field_by_name('multa')[0].verbose_name,                                                                                                                                                                                             
                                                                                                                                                                self.grupo_encargo.multa,
                                                                                                                                                                self.grupo_encargo._meta.get_field_by_name('tipo_juros')[0].verbose_name,
                                                                                                                                                                tj, 
                                                                                                                                                                self.grupo_encargo )
        return '-'
    grupo_encargo_associado.allow_tags = True
    grupo_encargo_associado.short_description = _(u"Grupo de encargo")
    grupo_encargo_associado.admin_order_field = 'grupo_encargo'


    def formata_descricao(self):
        if self.descricao:
            return u"<p title='%s'>%s...</p>" % (self.descricao, self.descricao[:35])
        return '-'
    formata_descricao.allow_tags = True
    formata_descricao.short_description = _(u"Descrição")


    def valor_total_juros(self):

        valor_total_juros = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor = ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).calculo_juros()
            valor_juros = 0 if not valor else valor
            valor_total_juros += valor_juros
        return Decimal(valor_total_juros).quantize(Decimal("0.00")) or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_juros.short_description = _(u"Valor total de juros")


    def valor_total_multa(self):

        valor_total_multa = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor = ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).calculo_multa()
            valor_multa = 0 if not valor else valor
            valor_total_multa += valor_multa
        return Decimal(valor_total_multa).quantize(Decimal("0.00")) or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_multa.short_description = _(u"Valor total de multa")


    def valor_total_encargos(self):

        valor_encargos = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor_encargos += ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).encargos_calculados()
        return valor_encargos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_encargos.short_description = _(u"Valor total de encargos")


    def valor_total_descontos(self):

        valor_descontos = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor_descontos += ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).valor_desconto()
        return valor_descontos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_descontos.short_description = _(u"Valor total de descontos")


    def valor_total_cobrado(self):

        valor_cobrado = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor_cobrado += ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).valor_total()
        return valor_cobrado or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_cobrado.short_description = _(u"Valor total cobrado")


    def valor_total_pago(self):

        valor_pago = Pagamento.objects.filter(parcelas_contas_pagar__contas_pagar=self.pk).aggregate(Sum('valor'))
        valor_pago = valor_pago["valor__sum"]
        return valor_pago or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_pago.short_description = _(u"Valor total pago")


    def link_pagamentos_conta(self):
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_pagar'})
        return u"<a href='%(url)spagamento/pagamentos_conta/%(pk)s' class='modal-rel-pagamentos modal-main-custom' rel='modal:open'>%(valor)s<span class='icon-share icon-alpha5 hint--bottom hint--bounce' style='vertical-align: text-bottom; margin-left: 10px;' rel='tooltip' data-hint='%(desc)s %(pk)s'></span></a>" % {'url': url, 'pk': self.pk, 'valor': self.valor_total_pago(), 'desc': _(u"Visualize todos os pagamentos efetuados da conta")}
    link_pagamentos_conta.allow_tags = True
    link_pagamentos_conta.short_description = _(u"Valor total pago")


    def valor_total_a_pagar(self):

        valor_a_pagar = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor_a_pagar += ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).valor_a_pagar()
        return valor_a_pagar or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_a_pagar.short_description = _(u"Valor total a pagar")


    def prazo_primeira_parcela(self, data, num_parcela):
        u"""
        Método que define a data de vencimento da primeira parcela baseado na parametrização da forma de pagamento.

        Parâmetros passados (data_da_compra, número_da_parcela) 
        """

        if self.forma_pagamento.tipo_carencia == 'M' and num_parcela == 0:
            data = date_add_months(data, self.forma_pagamento.carencia)
            return data
         
        if self.forma_pagamento.tipo_carencia == 'S' and num_parcela == 0:
            data = date_add_week(data, self.forma_pagamento.carencia)
            return data

        if self.forma_pagamento.tipo_carencia == 'D' and num_parcela == 0:
            data = date_add_days(data, self.forma_pagamento.carencia)
            return data

        else:
            return data


    def prazo_entre_parcelas(self, data):
        u"""
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_compra) 
        """

        if self.forma_pagamento.tipo_prazo == 'M':
            data = date_add_months(data, self.forma_pagamento.prazo_entre_parcelas)
            return data

        if self.forma_pagamento.tipo_prazo == 'S':
            data = date_add_week(data, self.forma_pagamento.prazo_entre_parcelas)
            return data

        if self.forma_pagamento.tipo_prazo == 'D':
            data = date_add_days(data, self.forma_pagamento.prazo_entre_parcelas)
            return data


    def valor_parcela(self, num_parcela, total):
        u"""
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da compra recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_compra)
        """

        quant_parc = self.forma_pagamento.quant_parcelas
        valor_parcela = round(total / quant_parc, 2)

        if (num_parcela + 1) == quant_parc:
            soma_parcelas = valor_parcela * num_parcela
            valor_parcela = Decimal(total).quantize(Decimal("0.00")) - Decimal(soma_parcelas).quantize(Decimal("0.00"))
            return valor_parcela
        else:
            return valor_parcela


    def pagamento_primeira_parcela(self, num_parcela):
        u"""
        Método que define como pago a primeira parcela de uma conta, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """

        if self.forma_pagamento.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        u"""
        Método que trata a geração e cálculo de contas à pagar.
        """

        data = self.data.date()
        quantidade_parcelada = self.forma_pagamento.quant_parcelas
        
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
                parcelas_conta.status = self.pagamento_primeira_parcela(i)
                parcelas_conta.num_parcelas = i + 1
                parcelas_conta.contas_pagar = self
                parcelas_conta.save()

            # Insere o pagamento de uma compra que tenha o prazo de carência 0(zero) na parametrização da forma de pagamento. 
            try:
                parcela_paga = ParcelasContasPagar.objects.get(contas_pagar=self, status=True)
                Pagamento(  data=data, 
                            valor=parcela_paga.valor, 
                            juros=0.00, 
                            multa=0.00,
                            desconto=0.00, 
                            parcelas_contas_pagar=parcela_paga
                            ).save()
            except ParcelasContasPagar.DoesNotExist:
                pass
        
        else:
            # tratar cancelamento de compra efetuada
            super(ContasPagar, self).save(*args, **kwargs)


from contas_pagar.models.parcela_conta_pagar import ParcelasContasPagar
from contas_pagar.models.pagamento import Pagamento