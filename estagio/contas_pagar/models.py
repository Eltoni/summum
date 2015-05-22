#-*- coding: UTF-8 -*-
from django.db import models
from compra.models import Compra
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from utilitarios.funcoes_data import date_add_months, date_add_week, date_add_days, date_settings_timezone
from utilitarios.calculos_encargos import calculo_composto, calculo_simples
from django.core.exceptions import ValidationError
import datetime
from decimal import Decimal
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _


class ContasPagar(models.Model):
    u""" 
    Classe ContasPagar. 

    Criada em 22/09/2014. 
    """

    data = models.DateField(verbose_name=_(u"Data")) 
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
        pass
        # from caixa.models import Caixa
        # if not Caixa.objects.filter(status=1).exists() and not self.pk:
        #     raise ValidationError(_(u"Não há caixa aberto. Para efetivar um cadastro de uma conta a pagar avulsa, é necessário ter o caixa aberto."))

        # if not Caixa.objects.filter(status=1).exists() and self.pk:
        #     raise ValidationError(_(u"Não há caixa aberto. Alterações numa conta a pagar só podem ser efetivadas após a abertura do caixa."))


    def __unicode__(self):
        return u'%s' % (self.id)


    def compra_associada(self):
        if self.compras:
            url = reverse("admin:compra_compra_change", args=[self.compras])
            return u"<a href='%s' target='_blank'>%s</a>" % (url, self.compras)
        return '-'
    compra_associada.allow_tags = True
    compra_associada.short_description = _(u"Compra")


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


    def valor_total_cobrado(self):

        valor_cobrado = 0
        quant_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).count()
        for i in range(quant_parcelas):
            retorna_id_parcelas = ParcelasContasPagar.objects.filter(contas_pagar=self.pk).values_list('pk')[i][0]
            valor_cobrado += ParcelasContasPagar.objects.get(pk=retorna_id_parcelas).valor_total()
        return valor_cobrado or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_cobrado.short_description = _(u"Valor total cobrado")


    def valor_total_pago(self):

        valor_pago = Pagamento.objects.filter(parcelas_contas_pagar__contas_pagar=self.pk).aggregate(Sum('valor')).items()[0][1]
        return valor_pago or Decimal(0.00).quantize(Decimal("0.00"))
    valor_total_pago.short_description = _(u"Valor total pago")


    def link_pagamentos_conta(self):
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_pagar'})
        return format_html('<a href="{0}pagamento/pagamentos_conta/{1}" target="_blank">{2}<span class="icon-share icon-alpha5" style="vertical-align: text-bottom; margin-left: 10px;" rel="tooltip" title="Visualize todos os pagamentos efetuados da conta {1}"</span></a>', url, self.pk, self.valor_total_pago())
        # return u"<a href='%spagamento/pagamentos_conta/%s' target='_blank'>%s</a>" % (url, self.pk, self.valor_total_pago())
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
        u"""
        Método que define o prazo entre data baseado na parametrização da forma de pagamento.
        Permite trabalhar com data com prazos semanais e mensais.

        Parâmetros passados (data_da_compra) 
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
        u"""
        Método que calcula os valores das mensalidades para que na divisão das parcelas, não fique restando valores decimais nos centavos gerados.
        Caso ocorra, a última parcela da compra recebe o valor restante.

        Parâmetros passados (número_da_parcela, valor_total_da_compra)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quant_parc = self.forma_pagamento_conta.quant_parcelas
        valor_parcela = round(total / quant_parc, 2)

        if (num_parcela + 1) == quant_parc:
            soma_parcelas = valor_parcela * num_parcela
            valor_parcela = float(total) - soma_parcelas
            return valor_parcela
        else:
            return valor_parcela


    def pagamento_primeira_parcela(self, num_parcela):
        u"""
        Método que define como pago a primeira parcela de uma conta, caso a carência parametrizada na forma de pagamento seja 0(zero).

        Parâmetros passados (número_da_parcela)
        """
        self.forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)

        if self.forma_pagamento_conta.carencia == 0 and num_parcela == 0:
            return True
        else:
            return False


    def save(self, *args, **kwargs):
        u"""
        Método que trata a geração e cálculo de contas à pagar.
        """
        data = datetime.date.today()

        forma_pagamento_conta = FormaPagamento.objects.get(pk=self.forma_pagamento.pk)
        quantidade_parcelada = forma_pagamento_conta.quant_parcelas
        
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



class ParcelasContasPagar(models.Model):
    u""" 
    Classe ParcelasContasPagar. 

    Criada em 22/09/2014.  
    """

    vencimento = models.DateField(verbose_name=_(u"Vencimento"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor")) 
    status = models.BooleanField(default=False, verbose_name=_(u"Status"))
    num_parcelas = models.IntegerField(verbose_name=_(u"Nº Parcela"))
    contas_pagar = models.ForeignKey(ContasPagar, on_delete=models.PROTECT, verbose_name=_(u"Conta à pagar"))

    class Meta:
        verbose_name = _(u"Parcela de Conta à Pagar")
        verbose_name_plural = _(u"Parcelas de Contas à Pagar")


    def __unicode__(self):
        return u'%s' % (self.id)


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

        valor_pago = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor')).items()[0][1]
        return valor_pago or Decimal(0.00).quantize(Decimal("0.00"))
    valor_pago.short_description = _(u"Valor Pago")


    def valor_a_pagar(self):
        parcela_pagamentos = Pagamento.objects.filter(parcelas_contas_pagar=self.pk).aggregate(Sum('valor')).items()[0][1]
        valor_a_pagar = Decimal(self.valor_total()).quantize(Decimal("0.00")) - (Decimal(0.00).quantize(Decimal("0.00")) if not parcela_pagamentos else parcela_pagamentos)
        return valor_a_pagar
    valor_a_pagar.short_description = _(u"Valor a Pagar")


    def link_pagamentos_parcela_cores(self):
        data = datetime.date.today()
        if self.valor_pago() >= self.valor_total():
            return '#2DB218 !important' #Pago

        if self.valor_total() > self.valor_pago() and self.valor_pago() > 0.00:
            return '#355EED !important' #Pago Parcial

        if self.vencimento < data:
            return '#E8262A !important' #Vencido

        else: 
            return '#333333 !important' #Em aberto


    def link_pagamentos_parcela(self):
        #return u"<a href='../../pagamento/add' target='_blank'>Pagar</a>"
        url = reverse('admin:app_list', kwargs={'app_label': 'contas_pagar'})
        # return u"<a href='%spagamento/pagamentos_parcela/%s' target='_blank' name='_return_id_parcela'>%s</a>" % (url, self.pk, self.valor_pago())
        return format_html('<a href="{0}pagamento/pagamentos_parcela/{1}" target="_blank" style="color: {2};">{3}<span class="icon-share icon-alpha5" style="position: relative; float: right; right: 20%;" rel="tooltip" title="Visualize todos os pagamentos efetuados da parcela {1}"</span></a>', url, self.pk, self.link_pagamentos_parcela_cores(), self.valor_pago())
    link_pagamentos_parcela.allow_tags = True
    link_pagamentos_parcela.short_description = _(u"Valor Pago")


    def link_pagamento(self):
        #return u"<a href='../../pagamento/add' target='_blank'>Pagar</a>"
        url = reverse("admin:contas_pagar_pagamento_add")
        return u"<a href='%s?id_parcela=%s' target='_blank' name='_return_id_parcela'>Pagar</a>" % (url, self.pk)
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



class Pagamento(models.Model):
    u""" 
    Classe Pagamento. 
    Criada para registrar todas as saídas financeiras do estabelecimento.
    Os registros de pagamentos entrarão automaticamente na tabela. 
    Contudo, também será possível cadastrar pagamentos manualmente, pensando em casos em que valores são pagos, eventualmente, sem a compra ter sido cadastrada.

    Criada em 16/06/2014. 
    """
    
    data = models.DateTimeField(auto_now_add=True, verbose_name=_(u"Data"))
    valor = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_(u"Valor"))
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Juros"))
    multa = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Multa"))
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True, verbose_name=_(u"Desconto"))
    parcelas_contas_pagar = models.ForeignKey(ParcelasContasPagar, on_delete=models.PROTECT, verbose_name=_(u"Pagamento de parcela"))
    
    def __unicode__(self):
        return u'%s' % (self.id)


    def clean(self):
        u""" 
        Bloqueia os pagamentos parciais que forem abaixo do percentual mínimo parametrizado nas configurações do sistema.
        Bloqueia somente o primeiro pagamento da parcela.

        Bloqueia a tentativa de efetuar um pagamento enquanto não houver caixa aberto no sistema.
        Bloqueia quaisquer alterações num registro de pagamento enquanto não houver caixa aberto no sistema.
        """
        pass
        # Checa a situação do caixa
        # from caixa.models import Caixa
        # if not Caixa.objects.filter(status=1).exists() and not self.pk:
        #     raise ValidationError(_(u"Não há caixa aberto. Para efetivar um pagamento é necessário ter o caixa aberto."))

        # if not Caixa.objects.filter(status=1).exists() and self.pk:
        #     raise ValidationError(_(u"Não há caixa aberto. Alterações num pagamento só podem ser efetivados após a abertura do caixa."))

        # # Checa a situação do valor do pagamento
        # from configuracoes.models import *
        # perc_valor_minimo_pagamento = Parametrizacao.objects.all().values_list('perc_valor_minimo_pagamento')[0][0]
        
        # parcela = ParcelasContasPagar.objects.get(pk=self.parcelas_contas_pagar.pk)
        # valor_minimo_pagamento = round((parcela.valor_total() * perc_valor_minimo_pagamento) / 100, 2)
        # primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=self.parcelas_contas_pagar.pk).exists()
        # if self.valor < valor_minimo_pagamento and not primeiro_pagamento:
        #     raise ValidationError(_(u"Primeiro pagamento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_pagamento, 'valor_minimo': valor_minimo_pagamento})


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
            