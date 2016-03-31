#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from venda.models import Venda
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
from django.utils.timezone import utc


@python_2_unicode_compatible
class ContasReceber(models.Model):
    u""" 
    Classe ContasReceber. 

    Criada em 22/09/2014. 
    """

    data = models.DateTimeField(verbose_name=_(u"Data de geração"))
    valor_total = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor total"))
    status = models.BooleanField(default=False, verbose_name=_(u"Conta fechada"), help_text=_(u"Se desmarcado, indica que há parcelas em aberto, caso contrário, a conta foi fechada."))
    descricao = models.TextField(blank=True, verbose_name=_(u"Descrição")) 
    vendas = models.ForeignKey(Venda, on_delete=models.PROTECT, null=True, verbose_name=_(u"Venda")) 
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, null=True, verbose_name=_(u"Cliente"))
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT, verbose_name=_(u"Forma de pagamento"))
    grupo_encargo = models.ForeignKey(GrupoEncargo, blank=False, null=False, verbose_name=_(u"Grupo de encargo"), on_delete=models.PROTECT)

    class Meta:
        verbose_name = _(u"Conta a Receber")
        verbose_name_plural = _(u"Contas a Receber")
        permissions = ((u"pode_exportar_contasreceber", _(u"Exportar Contas a Receber")),)


    def clean(self):
        """ 
        Bloqueia o registro de uma conta a receber quando não há caixa aberto.
        """
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar um cadastro de uma conta a receber avulsa, é necessário ter o caixa aberto."))

        if not Caixa.objects.filter(status=1).exists() and self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Alterações numa conta a receber só podem ser efetivadas após a abertura do caixa."))


    def __str__(self):
        return u'%s' % (self.id)


    def venda_associada(self):
        if self.vendas:
            try:
                url = pode_ver_link(self.usuario_sessao, 'venda', 'venda', self.vendas.pk)
            except:
                url = '#'
            return u"<a href='%s'>%s</a>" % (url, self.vendas)
        return '-'
    venda_associada.allow_tags = True
    venda_associada.short_description = _(u"Venda")
    venda_associada.admin_order_field = 'vendas'


    def cliente_associado(self):
        if self.cliente:
            url = pode_ver_link(self.usuario_sessao, 'pessoal', 'cliente', self.cliente.pk)
            return u"<a href='%s'>%s</a>" % (url, self.cliente)
        return '-'
    cliente_associado.allow_tags = True
    cliente_associado.short_description = _(u"Cliente")
    cliente_associado.admin_order_field = 'cliente'


    def forma_pagamento_associada(self):
        choices_tp = self.forma_pagamento._meta.get_field_by_name('tipo_prazo')[0].flatchoices
        tp = dict(choices_tp).get(self.forma_pagamento.tipo_prazo)
        choices_tp = self.forma_pagamento._meta.get_field_by_name('tipo_carencia')[0].flatchoices
        tc = dict(choices_tp).get(self.forma_pagamento.tipo_carencia)
        if self.forma_pagamento:
            url = pode_ver_link(self.usuario_sessao, 'parametros_financeiros', 'formapagamento', self.forma_pagamento.pk)
            return u"<a href='%s' rel='tooltip' data-hint='%s: %s&#10;&#10;%s: %s (%s)&#10;&#10;%s: %s (%s)' class='hint--right hint--bounce'>%s</a>" % ( url, 
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
            return u"<a href='%s' rel='tooltip' data-hint='%s: %s&#10;&#10;%s: %s&#10;&#10;%s: %s' class='hint--right hint--bounce'>%s</a>" % ( url, 
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
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor = ParcelasContasReceber.objects.get(pk=parcelas[i][0]).calculo_juros()
            valor_juros = 0 if not valor else valor
            valor_total_juros += valor_juros
        return Decimal(valor_total_juros).quantize(Decimal("0.00")) or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_juros.short_description = _(u"Valor total de juros")


    def valor_total_multa(self):

        valor_total_multa = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor = ParcelasContasReceber.objects.get(pk=parcelas[i][0]).calculo_multa()
            valor_multa = 0 if not valor else valor
            valor_total_multa += valor_multa
        return Decimal(valor_total_multa).quantize(Decimal("0.00")) or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_multa.short_description = _(u"Valor total de multa")


    def valor_total_encargos(self):

        valor_encargos = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor_encargos += ParcelasContasReceber.objects.get(pk=parcelas[i][0]).encargos_calculados()
        return valor_encargos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_encargos.short_description = _(u"Valor total de encargos")



    def valor_total_encargos_pagos(self):

        valor_encargos = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor_encargos += ParcelasContasReceber.objects.get(pk=parcelas[i][0]).encargos_pagos()
        return valor_encargos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_encargos_pagos.short_description = _(u"Valor total de encargos pagos")


    def valor_total_encargos_a_pagar(self):

        valor_encargos = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor_encargos += ParcelasContasReceber.objects.get(pk=parcelas[i][0]).encargos_a_pagar()
        return valor_encargos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_encargos_a_pagar.short_description = _(u"Valor total de encargos pagos")


    def valor_total_descontos(self):

        valor_descontos = 0
        quant_parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')[i][0]
            valor_descontos += ParcelasContasReceber.objects.get(pk=retorna_id_parcelas).valor_desconto()
        return valor_descontos or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_descontos.short_description = _(u"Valor total de descontos")


    def valor_total_cobrado(self):

        valor_cobrado = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor_cobrado += ParcelasContasReceber.objects.get(pk=parcelas[i][0]).valor_total()
        return valor_cobrado or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_cobrado.short_description = _(u"Valor total cobrado")


    def valor_total_recebido(self):

        valor_recebido = Recebimento.objects.filter(parcelas_contas_receber__contas_receber=self.pk).aggregate(Sum('valor'))
        valor_recebido = valor_recebido["valor__sum"]
        return valor_recebido or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_recebido.short_description = _(u"Valor total recebido")


    def link_recebimentos_conta(self):
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_receber'})
        return u"<a href='%(url)srecebimento/recebimentos_conta/%(pk)s' class='modal-rel-recebimentos modal-main-custom'>%(valor)s<span class='icon-share icon-alpha5 hint--bottom hint--bounce' style='vertical-align: text-bottom; margin-left: 10px;' rel='tooltip' data-hint='%(desc)s %(pk)s'></span></a>" % {'url': url, 'pk': self.pk, 'valor': self.valor_total_recebido(), 'desc': _(u"Visualize todos os recebimentos da conta")}
    link_recebimentos_conta.allow_tags = True
    link_recebimentos_conta.short_description = _(u"Valor total recebido")


    def valor_total_a_receber(self):

        valor_a_receber = 0
        parcelas = ParcelasContasReceber.objects.filter(contas_receber=self.pk).values_list('pk')
        for i in range(len(parcelas)):
            valor_a_receber += ParcelasContasReceber.objects.get(pk=parcelas[i][0]).valor_a_receber()
        return valor_a_receber or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_a_receber.short_description = _(u"Valor total a receber")


    def prazo_primeira_parcela(self, data, num_parcela):
        """
        Método que define a data de vencimento da primeira parcela baseado na parametrização da forma de pagamento.

        Parâmetros passados (data_da_venda, número_da_parcela) 
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
        """
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_venda) 
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
        """
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da venda recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_venda)
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
        """
        Método que define como pago a primeira parcela de uma conta, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """

        if self.forma_pagamento.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo de contas à receber.
        """

        data = self.data.date()
        quantidade_parcelada = self.forma_pagamento.quant_parcelas
        
        if self.pk is None:
            # Chama a função save original para o save atual do modelo
            super(ContasReceber, self).save(*args, **kwargs)

            # Insere as parcelas do contas à receber
            for i in range(quantidade_parcelada):                
                parcelas_conta = ParcelasContasReceber()
                data = self.prazo_primeira_parcela(data, i)
                parcelas_conta.vencimento = data
                data = self.prazo_entre_parcelas(data)
                parcelas_conta.valor = self.valor_parcela(i, self.valor_total)
                parcelas_conta.status = self.pagamento_primeira_parcela(i)
                parcelas_conta.num_parcelas = i + 1
                parcelas_conta.contas_receber = self
                parcelas_conta.save()

            # Insere o recebimento de uma venda que tenha o prazo de carência 0(zero) na parametrização da forma de pagamento. 
            try:
                parcela_paga = ParcelasContasReceber.objects.get(contas_receber=self, status=True)
                Recebimento(data=self.data.replace(tzinfo=utc), 
                            valor=parcela_paga.valor, 
                            juros=0.00, 
                            multa=0.00,
                            desconto=0.00, 
                            parcelas_contas_receber=parcela_paga
                            ).save()
            except ParcelasContasReceber.DoesNotExist:
                pass
        
        else:
            # tratar cancelamento de venda efetuada
            super(ContasReceber, self).save(*args, **kwargs)


from contas_receber.models.parcela_conta_receber import ParcelasContasReceber
from contas_receber.models.recebimento import Recebimento
