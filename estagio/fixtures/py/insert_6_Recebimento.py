#-*- coding: UTF-8 -*-
# from fixtures.py.insert_6_Recebimento import *
from django.utils.timezone import utc
from numpy import random as np

from datetime import timedelta
import random

from contas_receber.models import ParcelasContasReceber, Recebimento
from caixa.models import Caixa
from configuracoes.models import Parametrizacao
from utilitarios.funcoes_data import dia_util


print('Etapa 6 - Início do procedimento de inserção de Recebimentos.')

caixa_aberto = Caixa.objects.filter(status=1).values()[0]

if caixa_aberto["status"]:

    # Busca todas as parcelas que ainda não foram quitadas e que a conta na qual se originam está com status 'Aberta'
    lista_parcelas = ParcelasContasReceber.objects.filter(status=False, contas_receber__status=False).values_list('pk', 'contas_receber__data')

    for p in lista_parcelas:

        pula_parcela = bool(np.choice([True, False], p=[0.6, 0.4]))
        if pula_parcela:
            continue

        quantidade_recebimentos = int(np.choice([1, 2, 3], p=[0.8, 0.15, 0.05]))

        for i in range(quantidade_recebimentos):
            
            ultimo_recebimento = Recebimento.objects.filter(parcelas_contas_receber__pk=p[0]).values_list('data').order_by('-data')

            parcela = ParcelasContasReceber.objects.get(pk=p[0])
            valor_a_receber = parcela.valor_a_receber()
            valor_a_receber_juros = parcela.calculo_juros()
            valor_a_receber_multa = parcela.calculo_multa()

            if not ultimo_recebimento:
                data_recebimento = p[1] + timedelta(days=random.randint(0,50))

                # Trata valor dos recebimentos de acordo com o percentual do valor mínimo definido nas configurações do sistema
                if quantidade_recebimentos != 1:
                    perc_valor_minimo_recebimento = Parametrizacao.objects.all().values_list('perc_valor_minimo_recebimento')[0][0]
                    valor_a_receber = round((parcela.valor_total() * perc_valor_minimo_recebimento) / 100, 2)
            else:
                data_recebimento = ultimo_recebimento[0][0] + timedelta(days=random.randint(0,10))
                
                # Divide o valor a ser recebido caso ainda haja nova iteração
                if (quantidade_recebimentos == 3 and (i == 0 or i == 1)) or (quantidade_recebimentos == 2 and i == 0):
                    valor_a_receber = valor_a_receber / 2

            #Insere registro de recebimento 
            Recebimento(data=data_recebimento.replace(tzinfo=utc), 
                        valor=valor_a_receber, 
                        juros=valor_a_receber_juros, 
                        multa=valor_a_receber_multa,
                        desconto=0.00,
                        parcelas_contas_receber=parcela
                        ).save()