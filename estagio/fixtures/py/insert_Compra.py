#-*- coding: UTF-8 -*-
# from fixtures.py.insert_Compra import *
import random, decimal
from datetime import timedelta
from datetime import datetime
import time
from django.utils.timezone import utc
from compra.models import Compra, ItensCompra
from movimento.models import Produtos
from pessoal.models import Fornecedor
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from caixa.models import Caixa, MovimentosCaixa
from utilitarios.funcoes_data import dia_util
from numpy import random as np


def calcula_valor_total_item_compra(quantidade, valor_unitario, desconto):
    valor_item_compra = valor_unitario * quantidade
    valor_percentual_desconto = (valor_item_compra * desconto) / 100
    valor_total_item_compra = valor_item_compra - valor_percentual_desconto
    return valor_total_item_compra

def define_percentual_desconto():
    # Define um percentual de desconto, com 70% de probabilidade de retornar 0% de desconto.
    return np.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50], p=[0.7, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03])


lista_fornecedores = Fornecedor.objects.filter(status=1)
lista_formas_pagamento = FormaPagamento.objects.filter(status=1)
lista_grupos_encargo = GrupoEncargo.objects.filter(status=1)
lista_produtos = Produtos.objects.filter(status=1)

caixa_aberto = Caixa.objects.filter(status=1).values()[0]

if caixa_aberto["status"]:
    data = caixa_data_abertura = caixa_aberto["data_abertura"]
    data_atual = datetime.utcnow().replace(microsecond=0).replace(tzinfo=utc)

    # Equanto a data de abertura do caixa não for igual a data atual...
    while not data >= data_atual:
        
        data = data + timedelta(days=random.randint(0,10))
        data = dia_util(data)
        
        # ...Será realizado numa quantidade aleatória de vezes a inserção de uma compra no banco de dados
        for i in range(random.randint(0,10)):
            fornecedor = random.choice(lista_fornecedores)
            forma_pagamento = random.choice(lista_formas_pagamento)
            grupo_encargo = random.choice(lista_grupos_encargo)
            
            lista_itens_compra = []
            valor_compra = 0
            for ic in range(random.randint(0,15)):
                produto = random.choice(lista_produtos)
                quantidade = random.randint(1,10)
                valor_unitario = Produtos.objects.get(pk=produto.pk).preco
                percentual_desconto = define_percentual_desconto()

                valor_total = calcula_valor_total_item_compra(quantidade, valor_unitario, percentual_desconto)
                valor_compra += valor_total

                itens_compra = ItensCompra()
                itens_compra.produto = produto
                itens_compra.quantidade = quantidade
                itens_compra.valor_unitario = valor_unitario
                itens_compra.desconto = percentual_desconto
                itens_compra.valor_total = valor_total
                itens_compra.add_estoque = False

                # Insere os itens na lista antes de registrá-los
                lista_itens_compra.append(itens_compra)

            # cálculo do valor total da compra
            percentual_desconto = define_percentual_desconto()
            valor_a_descontar = (valor_compra * percentual_desconto) / 100
            valor_compra = valor_compra - valor_a_descontar

            # Determina se é pedido ou não, com probabilidade de 70% para que não seja.
            pedido = np.choice(['S', 'N'], p=[0.7, 0.3])
            if pedido == 'S':
                status_pedido = np.choice([True, False], p=[0.2, 0.8])
                data_pedido = data
                data_compra = None
                
            else:
                status_pedido = False
                data_pedido = None
                data_compra = data

            compra = Compra(total=valor_compra,
                            data_compra=data_compra,
                            data_pedido=data_pedido,
                            data_cancelamento=None,
                            desconto=percentual_desconto,
                            status=False,
                            fornecedor=fornecedor, 
                            forma_pagamento=forma_pagamento, 
                            grupo_encargo=grupo_encargo,
                            observacao=u'Criado à partir de procedimento de geração automática de registros.',
                            pedido=pedido,
                            status_pedido=status_pedido
                            )

            [ compra.save() for _ in range(2) ]


            for ic in lista_itens_compra:
                ic.compras = compra
                # Suplo save para que seja acrescido ao estoque, atendendo as condições declaradas no método save()
                [ ic.save() for _ in range(2) ]

