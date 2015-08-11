#-*- coding: UTF-8 -*-
from django.db import models
from pessoal.models import Cliente
from venda.models import Venda
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days, date_settings_timezone
from utilitarios.calculos_encargos import calculo_composto, calculo_simples
from utilitarios.funcoes import pode_ver_link
from django.core.exceptions import ValidationError
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from configuracoes.models import *


@python_2_unicode_compatible
class ContasReceber(models.Model):
    u""" 
    Classe ContasReceber. 

    Criada em 22/09/2014. 
    """

    data = models.DateField(verbose_name=_(u"Data"))
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
        tc = dict(choices_tp).get(self.forma_pagamento.tipo_prazo)
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
        return format_html('<a href="{0}recebimento/recebimentos_conta/{1}" target="_blank">{2}<span class="icon-share icon-alpha5 hint--bottom hint--bounce" style="vertical-align: text-bottom; margin-left: 10px;" rel="tooltip" data-hint="{3} {1}"</span></a>', url, self.pk, self.valor_total_recebido(), _(u"Visualize todos os recebimentos da conta"))
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
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo_primeira_parcela = self.forma_pagamento_conta.carencia

        if self.forma_pagamento_conta.tipo_carencia == 'M' and num_parcela == 0:
            data = date_add_months(data, prazo_primeira_parcela)
            return data
         
        if self.forma_pagamento_conta.tipo_carencia == 'S' and num_parcela == 0:
            data = date_add_week(data, prazo_primeira_parcela)
            return data

        if self.forma_pagamento_conta.tipo_carencia == 'D' and num_parcela == 0:
            data = date_add_days(data, prazo_primeira_parcela)
            return data

        else:
            return data


    def prazo_entre_parcelas(self, data):
        """
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_venda) 
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        prazo = self.forma_pagamento_conta.prazo_entre_parcelas

        if self.forma_pagamento_conta.tipo_prazo == 'M':
            data = date_add_months(data, prazo)
            return data

        if self.forma_pagamento_conta.tipo_prazo == 'S':
            data = date_add_week(data, prazo)
            return data

        if self.forma_pagamento_conta.tipo_prazo == 'D':
            data = date_add_days(data, prazo)
            return data


    def valor_parcela(self, num_parcela, total):
        """
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da venda recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_venda)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quant_parc = self.forma_pagamento_conta.quant_parcelas
        valor_parcela = round(total / quant_parc, 2)

        if (num_parcela + 1) == quant_parc:
            soma_parcelas = valor_parcela * num_parcela
            valor_parcela = Decimal(total).quantize(Decimal("0.00")) - soma_parcelas
            return valor_parcela
        else:
            return valor_parcela


    def pagamento_primeira_parcela(self, num_parcela):
        """
        Método que define como pago a primeira parcela de uma conta, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)

        if self.forma_pagamento_conta.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        """
        Método que trata a geração e cálculo de contas à receber.
        """
        data = datetime.date.today()

        forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quantidade_parcelada = forma_pagamento_conta.quant_parcelas
        
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
                Recebimento(data=data, 
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



@python_2_unicode_compatible
class ParcelasContasReceber(models.Model):
    u""" 
    Classe ParcelasContasReceber. 

    Criada em 22/09/2014.  
    """
    
    vencimento = models.DateField(verbose_name=_(u"Vencimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor")) 
    status = models.BooleanField(default=False, verbose_name=_(u"Status"))
    num_parcelas = models.IntegerField(verbose_name=_(u"Nº Parcela"))
    contas_receber = models.ForeignKey(ContasReceber, on_delete=models.PROTECT, verbose_name=_(u"Conta a receber"))

    class Meta:
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

        data = datetime.date.today()

        if self.pk and self.vencimento < data:
            existe_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).exists()
            if not existe_recebimento:
                dias_vencidos = data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                data_primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).values_list('data')[0][0]
                dias_vencidos = date_settings_timezone(data_primeiro_recebimento) - self.vencimento
                dias_vencidos = dias_vencidos.days

            return dias_vencidos
        return 0
    quant_dias_vencidos.short_description = _(u"Quantidade de dias vencidos")


    def calculo_juros(self):
        u""" 
        Retorna o valor cálculado dos juros de acordo com a parametrização feita no grupo de encargos selecionado para a conta a pagar 
        """

        data = datetime.date.today()

        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk and self.vencimento < data:
            
            parametros_grupo_encargo = GrupoEncargo.objects.filter(pk=self.contas_receber.grupo_encargo.pk).values_list('juros', 'tipo_juros')[0]
            # Percentual de multa
            percentual_juros = parametros_grupo_encargo[0] / 100
            
            # quantidade de dias em atraso
            existe_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).exists()
            if not existe_recebimento:
                dias_vencidos = data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                data_primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).values_list('data')[0][0]
                dias_vencidos = date_settings_timezone(data_primeiro_recebimento) - self.vencimento
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
            
            percentual_multa = GrupoEncargo.objects.filter(pk=self.contas_receber.grupo_encargo.pk).values_list('multa')[0][0]
            percentual_multa = percentual_multa / 100

            # quantidade de dias em atraso
            existe_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).exists()
            if not existe_recebimento:
                dias_vencidos = data - self.vencimento
                dias_vencidos = dias_vencidos.days
            else: 
                data_primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.pk).values_list('data')[0][0]
                dias_vencidos = date_settings_timezone(data_primeiro_recebimento) - self.vencimento
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


    def encargos_pagos(self):
        u""" 
        Retorna o valor pago dos encargos cobrados da parcela
        """
        if self.pk:
            encargos_pagos = Decimal(self.valor_pago() - self.valor).quantize(Decimal("0.00"))
            if encargos_pagos < 0.00:
                return Decimal(0.00).quantize(Decimal("0.00"))
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
                return Decimal(0.00).quantize(Decimal("0.00"))
            else:
                return encargos_a_pagar
        return 0.00
    encargos_a_pagar.short_description = _(u"Encargos a Pagar")


    def valor_total(self):
        u""" 
        Retorna o valor total da parcela com os encargos cálculados (valor juro + valor multa + valor parcela) 
        """

        # Após a atualização para o Django 1.7.7, é preciso checar se está o objeto está instanciado (if self.pk) 
        if self.pk:
            valor_total = Decimal(self.valor + self.encargos_calculados()).quantize(Decimal("0.00"))
            return valor_total or 0.00
        return 0.00
    valor_total.short_description = _(u"Valot Total")


    def valor_pago(self):

        valor_pago = Recebimento.objects.filter(parcelas_contas_receber=self.pk).aggregate(Sum('valor'))
        valor_pago = valor_pago["valor__sum"]
        return valor_pago or Decimal(0.00).quantize(Decimal("0.00"))
    valor_pago.short_description = _(u"Valor Pago")


    def valor_a_receber(self):
        parcela_recebimentos = Recebimento.objects.filter(parcelas_contas_receber=self.pk).aggregate(Sum('valor'))
        parcela_recebimentos = parcela_recebimentos["valor__sum"]
        valor_a_receber = Decimal(self.valor_total()).quantize(Decimal("0.00")) - (Decimal(0.00).quantize(Decimal("0.00")) if not parcela_recebimentos else parcela_recebimentos)
        return valor_a_receber
    valor_a_receber.short_description = _(u"Valor a Receber")


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


    def link_recebimentos_parcela(self):
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_receber'})
        return format_html('<a href="{0}recebimento/recebimentos_parcela/{1}" target="_blank" style="color: {2};">{3}<span class="icon-share icon-alpha5 hint--bottom hint--bounce" style="position: relative; float: right; right: 20%;" rel="tooltip" data-hint="{4} {1}"</span></a>', url, self.pk, self.status_parcela()[0], self.valor_pago(), _(u"Visualize todos os recebimentos da parcela"))
    link_recebimentos_parcela.allow_tags = True
    link_recebimentos_parcela.short_description = _(u"Valor Pago")


    def link_recebimento(self):
        #return u"<a href='../../recebimento/add' target='_blank'>Receber</a>"
        url = reverse("admin:contas_receber_recebimento_add")
        return u"<a href='%s?id_parcela=%s' target='_blank' name='_return_id_parcela'>Receber</a>" % (url, self.pk)
    link_recebimento.allow_tags = True
    link_recebimento.short_description = u''


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



@python_2_unicode_compatible
class Recebimento(models.Model):
    u""" 
    Classe Recebimento. 
    Criada para registrar todas as entradas financeiras do estabelecimento.
    Os registros de recebimentos entrarão automaticamente na tabela. 

    Criada em 15/06/2014. 
    """

    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber, on_delete=models.PROTECT, verbose_name=_(u"Recebimento de parcela"))

    class Meta:
        verbose_name = _(u"Recebimento")
        verbose_name_plural = _(u"Recebimentos")


    def __str__(self):
        return u'%s' % (self.id)


    def clean(self):
        u""" 
        Bloqueia os recebimentos parciais que forem abaixo do percentual mínimo parametrizado nas configurações do sistema.
        Bloqueia somente o primeiro pagamento da parcela.

        Bloqueia a tentativa de efetuar um recebimento enquanto não houver caixa aberto no sistema.
        Bloqueia quaisquer alterações num registro de recebimento enquanto não houver caixa aberto no sistema.
        """
        # Checa a situação do caixa
        from caixa.models import Caixa
        if not Caixa.objects.filter(status=1).exists() and not self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Para efetivar um recebimento é necessário ter o caixa aberto."))

        if not Caixa.objects.filter(status=1).exists() and self.pk:
            raise ValidationError(_(u"Não há caixa aberto. Alterações num recebimento só podem ser efetivados após a abertura do caixa."))

        # Checa a situação do valor do recebimento
        perc_valor_minimo_recebimento = Parametrizacao.objects.all().values_list('perc_valor_minimo_pagamento')[0][0]
        
        parcela = ParcelasContasReceber.objects.get(pk=self.parcelas_contas_receber.pk)
        valor_minimo_recebimento = round((parcela.valor_total() * perc_valor_minimo_recebimento) / 100, 2)
        primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=self.parcelas_contas_receber.pk).exists()
        if self.valor < valor_minimo_recebimento and not primeiro_recebimento:
            raise ValidationError(_(u"Primeiro recebimento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_recebimento, 'valor_minimo': valor_minimo_recebimento})


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