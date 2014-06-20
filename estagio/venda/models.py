from django.db import models


class Recebimento(models.Model):
    u""" 
    Classe Recebimento. 
    Criada para registrar todas as entradas financeiras do estabelecimento.
    Os registros de recebimentos entrarão automaticamente na tabela. 
    Contudo, também será possível cadastrar recebimentos manualmente, pensando em casos em que valores são recebidos, eventualmente, sem a venda ter sido cadastrada.

    Criada em 15/06/2014. 
    """

    data = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2)
    juros = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    desconto = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(verbose_name=u'Ativo')
    # estornada = models.BooleanField(verbose_name=u'Estornada?')
    # data_estorno = models.DateField(auto_now_add=True, verbose_name=u'Data do estorno')
    # parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber)

