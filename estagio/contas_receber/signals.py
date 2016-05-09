#-*- coding: UTF-8 -*-
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal

from contas_receber.models import ParcelasContasReceber, Recebimento
from caixa.models import Caixa, MovimentosCaixa


def update_movimento_caixa_recebimento(sender, instance, **kwargs):
    """ 
    Método para ïnserir na tabela de movimentos_de_caixa os movimentos de entrada financeira.
    O mesmo age sobre o Movimento de Caixa e o Caixa, fazendo todo o cálculo para controle dessas entidades.

    Criada em 09/10/2014. 
    """

    # Não prossegue com o processamento caso não entre valor no caixa.
    if instance.valor <= 0:
        return

    # Busca o id da conta à receber e da compra vinculado ao recebimento instanciado
    conta = ParcelasContasReceber.objects.filter(pk=instance.parcelas_contas_receber.pk).select_related('contas_receber__contasreceber').values_list('contas_receber__pk', 'contas_receber__vendas')[0]
    
    # Condição que monta a descrição que é salvo no registro do movimento. Condiciona para descrições distintas caso o recebimento seja de uma conta avulsa, ou de uma conta vinculada a uma compra
    if conta[1]:
        descricao = _(u"Recebimento: %(recebimento)s, proveniente da parcela: %(parcela)s, da conta a receber: %(conta_receber)s, da venda: %(venda)s.") % {'recebimento': instance.pk, 'parcela': instance.parcelas_contas_receber.pk, 'conta_receber': conta[0], 'venda': conta[1]}
    
    else:
        conta_avulsa = ParcelasContasReceber.objects.filter(pk=instance.parcelas_contas_receber.pk).select_related('contas_receber__contasreceber').values_list('contas_receber__descricao', flat=True)[0]
        descricao = _(u"Recebimento avulso. %(recebimento)s") % {'recebimento': conta_avulsa[:50]}

    # Insere os itens de saída de movimentos de caixa
    movimento_caixa = MovimentosCaixa(  descricao=descricao, 
                                        valor=Decimal(instance.valor).quantize(Decimal("0.00")),
                                        data=instance.data, 
                                        tipo_mov='Crédito', 
                                        caixa=Caixa.objects.get(status=1),
                                        recebimento=instance
                                        )
    # Não insere duas vezes se o recebimento existir e se o mesmo tiver o mesmo valor
    if MovimentosCaixa.objects.filter(recebimento__pk=instance.pk).exists():
        pass
    else:
        movimento_caixa.save()

# registro da signal
post_save.connect(update_movimento_caixa_recebimento, sender=Recebimento, dispatch_uid="update_movimento_caixa_recebimento")