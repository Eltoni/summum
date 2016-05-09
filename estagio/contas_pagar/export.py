#-*- coding: UTF-8 -*-
from django.utils.translation import gettext
from import_export import fields, resources
from decimal import Decimal
from contas_pagar.models import ContasPagar, ParcelasContasPagar

#classe usada pelo import_export
class ContasPagarResource(resources.ModelResource):

    class Meta(object):
        model = ContasPagar
        #exclude = ('nome', 'estado')

    def dehydrate_data(self, contaspagar):
        return '%s' % (contaspagar.data.strftime('%d/%m/%Y'))

    def dehydrate_fornecedores(self, contaspagar):
        return '%s' % (contaspagar.fornecedores.nome)

    def dehydrate_forma_pagamento(self, contaspagar):
        return '%s' % (contaspagar.forma_pagamento.nome)

    def dehydrate_grupo_encargo(self, contaspagar):
        return '%s' % (contaspagar.grupo_encargo.nome)

    def dehydrate_valor_total(self, contaspagar):
        return '%s' % (Decimal(contaspagar.valor_total).quantize(Decimal("0.00")))



class ParcelasContasPagarResource(resources.ModelResource):
    status_parcela = fields.Field()
    encargos_calculados = fields.Field()
    valor_total = fields.Field()
    valor_pago = fields.Field()
    valor_a_pagar = fields.Field()
    fornecedores = fields.Field()

    class Meta(object):
        model = ParcelasContasPagar
        fields = ('id', 'num_parcelas', 'vencimento', 'valor', 'encargos_calculados', 'valor_total', 'valor_pago', 'valor_a_pagar', 'status_parcela', 'contas_pagar', 'fornecedores')
        export_order = fields

    def dehydrate_vencimento(self, parcelascontaspagar):
        return '%s' % (parcelascontaspagar.vencimento.strftime('%d/%m/%Y'))

    def dehydrate_valor(self, parcelascontaspagar):
        return '%s' % (Decimal(parcelascontaspagar.valor).quantize(Decimal("0.00")))

    def dehydrate_encargos_calculados(self, parcelascontaspagar):
        return Decimal(parcelascontaspagar.encargos_calculados()).quantize(Decimal("0.00"))

    def dehydrate_valor_total(self, parcelascontaspagar):
        return Decimal(parcelascontaspagar.valor_total()).quantize(Decimal("0.00"))

    def dehydrate_valor_pago(self, parcelascontaspagar):
        return Decimal(parcelascontaspagar.valor_pago()).quantize(Decimal("0.00"))

    def dehydrate_valor_a_receber(self, parcelascontaspagar):
        return Decimal(parcelascontaspagar.valor_a_pagar()).quantize(Decimal("0.00"))

    def dehydrate_status_parcela(self, parcelascontaspagar):
        return gettext(parcelascontaspagar.status_parcela()[1])

    def dehydrate_fornecedores(self, parcelascontaspagar):
        return '%s' % (parcelascontaspagar.contas_pagar.fornecedores.nome)