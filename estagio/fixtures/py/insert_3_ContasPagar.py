#-*- coding: UTF-8 -*-
# from fixtures.py.insert_3_ContasPagar import *
import random, decimal
from datetime import timedelta
from datetime import datetime
import time
from django.utils.timezone import utc
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from contas_pagar.models import ContasPagar, Pagamento
from caixa.models import Caixa, MovimentosCaixa
from utilitarios.funcoes_data import dia_util


print('Etapa 3 - Início do procedimento de inserção de Contas a Pagar.')

format_date = '%Y-%m-%d %I:%M:%S %p'

lista_fornecedores = Fornecedor.objects.filter(status=1)
lista_formas_pagamento = FormaPagamento.objects.filter(status=1)
lista_grupos_encargo = GrupoEncargo.objects.filter(status=1)
caixa_aberto = Caixa.objects.filter(status=1).values()[0]

if caixa_aberto["status"]:
    caixa_data_abertura = caixa_aberto["data_abertura"]
    data_atual = datetime.utcnow().replace(microsecond=0).replace(tzinfo=utc)

    quant_dias = caixa_data_abertura.date() - data_atual.date()
    qt_a_gerar = abs(quant_dias.days)
    
    data = caixa_data_abertura
    while not data >= data_atual:
        
        data = data + timedelta(days=random.randint(0,10))
        data = dia_util(data)
        
        for i in range(random.randint(0,10)):
            fornecedor = random.choice(lista_fornecedores)
            forma_pagamento = random.choice(lista_formas_pagamento)
            grupo_encargo = random.choice(lista_grupos_encargo)
            valor_total = decimal.Decimal(random.random() * 1000).quantize(decimal.Decimal('.01'))
            
            conta = ContasPagar(data=data, 
                                valor_total=valor_total, 
                                descricao=u'Criado à partir de procedimento de geração automática de registros.',
                                compras=None, 
                                fornecedores=fornecedor, 
                                forma_pagamento=forma_pagamento, 
                                grupo_encargo=grupo_encargo, 
                                status=False
                                )
            conta.save()



# Atualiza as datas de pagamentos e movimentos de caixa
lista_pagamentos = Pagamento.objects.filter(parcelas_contas_pagar__contas_pagar__descricao__contains='Criado à partir de procedimento de geração automática de registros.', 
                                            parcelas_contas_pagar__contas_pagar__forma_pagamento__carencia=0,
                                            parcelas_contas_pagar__num_parcelas=1
                                            ).values_list('pk', 'data', 'parcelas_contas_pagar__contas_pagar__data')
for l in lista_pagamentos:
    if l[1].date() != l[2]:
        r = Pagamento.objects.get(pk=l[0])
        r.data = l[2]
        r.save()
        m = MovimentosCaixa.objects.get(pagamento__pk=l[0])
        m.data = l[2]
        m.save()

