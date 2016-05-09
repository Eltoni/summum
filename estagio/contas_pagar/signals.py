#-*- coding: UTF-8 -*-
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from contas_pagar.models import ParcelasContasPagar, Pagamento
from caixa.models import Caixa, MovimentosCaixa


def update_movimento_caixa_pagamento(sender, instance, **kwargs):
    """ 
    Método para inserir na tabela de movimentos_de_caixa os movimentos de saída financeira.
    O mesmo age sobre o Movimento de Caixa e o Caixa, fazendo todo o cálculo para controle dessas entidades.

    Criada em 01/10/2014. 
    """

    # Não prossegue com o processamento caso não saia valor do caixa.
    if instance.valor <= 0:
        return

    # Busca o id da conta à pagar e da compra vinculado ao pagamento instanciado
    conta = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__pk', 'contas_pagar__compras')[0]
    
    # Condição que monta a descrição que é salvo no registro do movimento. Condiciona para descrições distintas caso o pagamento seja de uma conta avulsa, ou de uma conta vinculada a uma compra
    if conta[1]:
        descricao = _(u"Pagamento: %(pagamento)s, proveniente da parcela: %(parcela)s, da conta a pagar: %(conta_pagar)s, da compra: %(compra)s.") % {'pagamento': instance.pk, 'parcela': instance.parcelas_contas_pagar.pk, 'conta_pagar': conta[0], 'compra': conta[1]}
    
    else:
        conta_avulsa = ParcelasContasPagar.objects.filter(pk=instance.parcelas_contas_pagar.pk).select_related('contas_pagar__contaspagar').values_list('contas_pagar__descricao', flat=True)[0]
        descricao = _(u"Pagamento avulso. %(pagamento)s") % {'pagamento': conta_avulsa[:50]}

    # Insere os itens de saída de movimentos de caixa
    movimento_caixa = MovimentosCaixa(  descricao=descricao, 
                                        valor=Decimal(instance.valor).quantize(Decimal("0.00")),
                                        data=instance.data, 
                                        tipo_mov='Débito', 
                                        caixa=Caixa.objects.get(status=1),
                                        pagamento=instance
                                        )
    # Não insere duas vezes se o pagamento existir e se o mesmo tiver o mesmo valor
    if MovimentosCaixa.objects.filter(pagamento__pk=instance.pk).exists():
        pass
    else:
        movimento_caixa.save()

# registro da signal
post_save.connect(update_movimento_caixa_pagamento, sender=Pagamento, dispatch_uid="update_movimento_caixa_pagamento")