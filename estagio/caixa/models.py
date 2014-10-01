#-*- coding: UTF-8 -*-
from django.db import models
from contas_pagar.models import Pagamento
from django.core.exceptions import ValidationError


class Caixa(models.Model):
    status = models.BooleanField(default=False, help_text=u'Selecione o Checkbox para indicar se o caixa está aberto.')
    data = models.DateField()
    valor_entrada = models.DecimalField(max_digits=20, decimal_places=2)
    valor_saida = models.DecimalField(max_digits=20, decimal_places=2)
    valor_total = models.DecimalField(max_digits=20, decimal_places=2)
    valor_inicial = models.DecimalField(max_digits=20, decimal_places=2)
    diferenca = models.DecimalField(max_digits=20, decimal_places=2)
    valor_fechamento = models.DecimalField(max_digits=20, decimal_places=2)

    def __unicode__(self):
        return u'%s' % (self.id)
        
    def clean(self):
        """ 
        Não permite que seja aberto dois caixas ao mesmo tempo. Para abrir um caixa, não pode haver obrigatóriamente um outro com status ativo.
        Caso um usuário tente abri-lo nesse contexto, receberá mensagem informando o erro e o id do caixa atualmente aberto.
        """
        try:
            caixa_aberto = Caixa.objects.filter(status=1).exclude(pk=self.id)
        except Caixa.DoesNotExist:
            caixa_aberto = False

        if caixa_aberto and self.status == 1:
            raise ValidationError('Já há um caixa aberto. Para abrir este, é necessário fechar o caixa atualmente aberto (Caixa: %s).' % caixa_aberto[0])
        


class MovimentosCaixa(models.Model):
    descricao = models.CharField(max_length=45)
    valor = models.CharField(max_length=45)
    data = models.DateTimeField()
    tipo_mov = models.CharField(max_length=45)
    caixa = models.ForeignKey(Caixa)
    pagamento = models.ForeignKey(Pagamento, blank=True, null=True)
    #recebimento = models.ForeignKey(Recebimento, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.id)


