#-*- coding: UTF-8 -*-
from import_export import fields, resources
from contas_receber.models import ContasReceber, ParcelasContasReceber
from decimal import Decimal
from django.utils.translation import gettext
#classe usada pelo import_export
class ContasReceberResource(resources.ModelResource):

    class Meta:
        model = ContasReceber
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, contasreceber):
        return '%s' % (contasreceber.data.strftime('%d/%m/%Y'))

    def dehydrate_cliente(self, contasreceber):
        return '%s' % (contasreceber.cliente.nome)

    def dehydrate_forma_pagamento(self, contasreceber):
        return '%s' % (contasreceber.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, contasreceber):
        return '%s' % (contasreceber.grupo_encargo.nome)

    def dehydrate_valor_total(self, contasreceber):
        return '%s' % (Decimal(contasreceber.valor_total).quantize(Decimal("0.00")))



class ParcelasContasReceberResource(resources.ModelResource):
    status_parcela = fields.Field()
    encargos_calculados = fields.Field()
    valor_total = fields.Field()
    valor_pago = fields.Field()
    valor_a_receber = fields.Field()
    cliente = fields.Field()

    class Meta:
        model = ParcelasContasReceber
        fields = ('id', 'num_parcelas', 'vencimento', 'valor', 'encargos_calculados', 'valor_total', 'valor_pago', 'valor_a_receber', 'status_parcela', 'contas_receber', 'cliente')
        export_order = fields

    def dehydrate_vencimento(self, parcelascontasreceber):
        return '%s' % (parcelascontasreceber.vencimento.strftime('%d/%m/%Y'))

    def dehydrate_valor(self, parcelascontasreceber):
        return '%s' % (Decimal(parcelascontasreceber.valor).quantize(Decimal("0.00")))

    def dehydrate_encargos_calculados(self, parcelascontasreceber):
        return Decimal(parcelascontasreceber.encargos_calculados()).quantize(Decimal("0.00"))

    def dehydrate_valor_total(self, parcelascontasreceber):
        return Decimal(parcelascontasreceber.valor_total()).quantize(Decimal("0.00"))

    def dehydrate_valor_pago(self, parcelascontasreceber):
        return Decimal(parcelascontasreceber.valor_pago()).quantize(Decimal("0.00"))

    def dehydrate_valor_a_receber(self, parcelascontasreceber):
        return Decimal(parcelascontasreceber.valor_a_receber()).quantize(Decimal("0.00"))

    def dehydrate_status_parcela(self, parcelascontasreceber):
        return gettext(parcelascontasreceber.status_parcela()[1])

    def dehydrate_cliente(self, parcelascontasreceber):
        return '%s' % (parcelascontasreceber.contas_receber.cliente.nome)