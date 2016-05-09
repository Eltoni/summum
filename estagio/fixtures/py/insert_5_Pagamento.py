#-*- coding: UTF-8 -*-
# from fixtures.py.insert_5_Pagamento import *
from django.utils.timezone import utc
from numpy import random as np

from datetime import datetime, timedelta
import random

from contas_pagar.models import ParcelasContasPagar, Pagamento
from caixa.models import Caixa


class ProcessoGeraPagamento(object):

    def gera_pagamento(self):
        print('Etapa 5 - Início do procedimento de inserção de Pagamentos.')

        caixa_aberto = Caixa.objects.filter(status=1).values()[0]
        data_atual = datetime.utcnow().replace(microsecond=0).replace(tzinfo=utc)

        if caixa_aberto["status"]:

            # Busca todas as parcelas que ainda não foram quitadas e que a conta na qual se originam está com status 'Aberta'
            lista_parcelas = ParcelasContasPagar.objects.filter(status=False, contas_pagar__status=False).values_list('pk', 'contas_pagar__data')

            for p in lista_parcelas:

                pula_parcela = bool(np.choice([True, False], p=[0.6, 0.4]))
                if pula_parcela:
                    continue

                quantidade_pagamentos = int(np.choice([1, 2, 3], p=[0.8, 0.15, 0.05]))

                for i in range(quantidade_pagamentos):
                    
                    ultimo_pagamento = Pagamento.objects.filter(parcelas_contas_pagar__pk=p[0]).values_list('data').order_by('-data')

                    parcela = ParcelasContasPagar.objects.get(pk=p[0])
                    valor_a_pagar = parcela.valor_a_pagar()
                    valor_a_pagar_juros = parcela.calculo_juros()
                    valor_a_pagar_multa = parcela.calculo_multa()

                    if not ultimo_pagamento:
                        data_pagamento = p[1] + timedelta(days=random.randint(0,50))
                    else:
                        data_pagamento = ultimo_pagamento[0][0] + timedelta(days=random.randint(0,10))
                    
                    # # Caso a data de pagamento calculado seja maior que a data atual, é definida a data atual como data de pagamento
                    # quant_dias = data_pagamento.date() - data_atual.date()
                    # dias_diferenca = abs(quant_dias.days)

                    # if dias_diferenca > 0:
                    #     data_pagamento = data_atual


                    # Divide o valor a ser recebido caso ainda haja nova iteração
                    if (quantidade_pagamentos == 3 and (i == 0 or i == 1)) or (quantidade_pagamentos == 2 and i == 0):
                        valor_a_pagar = valor_a_pagar / 2

                    #Insere registro de recebimento 
                    Pagamento(  data=data_pagamento.replace(tzinfo=utc), 
                                valor=valor_a_pagar, 
                                juros=valor_a_pagar_juros, 
                                multa=valor_a_pagar_multa,
                                desconto=0.00,
                                parcelas_contas_pagar=parcela
                                ).save()