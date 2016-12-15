#-*- coding: UTF-8 -*-
# from fixtures.py.insert_2_Venda import *
from django.utils.timezone import utc
from numpy import random as np

import random
from datetime import timedelta, datetime

from venda.models import Venda, ItensVenda
from movimento.models import Produtos
from pessoal.models import Cliente
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from contas_receber.models import Recebimento
from caixa.models import Caixa
from utilitarios.funcoes_data import dia_util


class ProcessoGeraVenda(object):

    def calcula_valor_total_item_venda(self, quantidade, valor_unitario, desconto):
        valor_item_venda = valor_unitario * quantidade
        valor_percentual_desconto = (valor_item_venda * desconto) / 100
        valor_total_item_venda = valor_item_venda - valor_percentual_desconto
        return valor_total_item_venda

    def define_percentual_desconto(self):
        # Define um percentual de desconto, com 70% de probabilidade de retornar 0% de desconto.
        return np.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50], p=[0.7, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03])

    def gera_venda(self):
        print('Etapa 2 - Início do procedimento de inserção de Vendas.')
        
        lista_clientes = Cliente.objects.filter(status=1)
        lista_formas_pagamento = FormaPagamento.objects.filter(status=1)
        lista_grupos_encargo = GrupoEncargo.objects.filter(status=1)
        lista_produtos = Produtos.objects.filter(status=1)

        caixa_aberto = Caixa.objects.filter(status=1).values()[0]
        data_atual = datetime.utcnow().replace(microsecond=0).replace(tzinfo=utc)

        if caixa_aberto["status"]:
            data = caixa_aberto["data_abertura"]

            # Equanto a data de abertura do caixa não for igual a data atual...
            while not data >= data_atual:
                
                data = data + timedelta(days=random.randint(0,10))
                data = dia_util(data)

                # Quebra iteração caso data de geração do registro seja maior que data atual
                if data > data_atual:
                    break
                
                # ...Será realizado numa quantidade aleatória de vezes a inserção de uma venda no banco de dados
                for i in range(random.randint(0,10)):
                    cliente = random.choice(lista_clientes)
                    forma_pagamento = random.choice(lista_formas_pagamento)
                    grupo_encargo = random.choice(lista_grupos_encargo)
                    
                    lista_quantidade_produto = []
                    lista_itens_venda = []
                    valor_venda = 0
                    for ic in range(random.randint(1,15)):
                        produto = random.choice(lista_produtos)
                        quantidade = random.randint(1,10)

                        # Valida quantidade de itens em estoque
                        #---------------------------------------------------------------------------------------------------
                        valida_itens_estoque = Produtos.objects.filter(pk=produto.pk).values_list('pk', 'quantidade')[0]
                        try:
                            quant_itens_interacao = [ q[1] for q in lista_quantidade_produto if q[0] == produto.pk ][0] or 0
                            existe_item_lista_quantidade_produto = True
                        except IndexError:
                            quant_itens_interacao = 0
                            existe_item_lista_quantidade_produto = False

                        if ((valida_itens_estoque[1] - (quant_itens_interacao + quantidade)) < 0):
                            continue

                        else:
                            if existe_item_lista_quantidade_produto:
                                for lqp in lista_quantidade_produto:
                                    if (lqp[0] == produto.pk):
                                        item_produto, item_quantidade = lqp[0], lqp[1] + quantidade
                                        lista_quantidade_produto.remove(lqp)
                                        lista_quantidade_produto.append(((item_produto),(item_quantidade)))
                            else:
                                lista_quantidade_produto.append(((produto),(quantidade)))
                        #---------------------------------------------------------------------------------------------------

                        valor_unitario = Produtos.objects.get(pk=produto.pk).preco_venda
                        percentual_desconto = int(self.define_percentual_desconto())

                        valor_total = self.calcula_valor_total_item_venda(quantidade, valor_unitario, percentual_desconto)
                        valor_venda += valor_total

                        itens_venda = ItensVenda()
                        itens_venda.produto = produto
                        itens_venda.quantidade = quantidade
                        itens_venda.valor_unitario = valor_unitario
                        itens_venda.desconto = percentual_desconto
                        itens_venda.valor_total = valor_total
                        itens_venda.remove_estoque = False

                        # Insere os itens na lista antes de registrá-los
                        lista_itens_venda.append(itens_venda)

                    # cálculo do valor total da compra
                    percentual_desconto = int(self.define_percentual_desconto())
                    valor_a_descontar = (valor_venda * percentual_desconto) / 100
                    valor_venda = valor_venda - valor_a_descontar

                    # Determina se é pedido ou não, com probabilidade de 70% para que não seja.
                    pedido = str(np.choice(['S', 'N'], p=[0.7, 0.3]))
                    if pedido == 'S':
                        data_pedido = data
                        status_pedido = bool(np.choice([True, False], p=[0.2, 0.8]))
                        if status_pedido:
                            data_venda = data
                        else:
                            data_venda = None
                    else:
                        status_pedido = False
                        data_pedido = None
                        data_venda = data

                    venda = Venda(  total=valor_venda,
                                    data_venda=data_venda,
                                    data_pedido=data_pedido,
                                    data_cancelamento=None,
                                    desconto=percentual_desconto,
                                    status=False,
                                    cliente=cliente,
                                    forma_pagamento=forma_pagamento, 
                                    grupo_encargo=grupo_encargo,
                                    observacao=u'Criado à partir de procedimento de geração automática de registros.',
                                    pedido=pedido,
                                    status_pedido=status_pedido
                                    )

                    [ venda.save() for _ in range(2) ]


                    for ic in lista_itens_venda:
                        ic.vendas = venda
                        # Suplo save para que seja acrescido ao estoque, atendendo as condições declaradas no método save()
                        [ ic.save() for _ in range(2) ]


        # Cancela alguns registros de venda/pedido de venda
        vendas = Venda.objects.filter(status=False)
        for i in vendas:
            conta_gerada = Recebimento.objects.filter(parcelas_contas_receber__contas_receber__vendas=i.pk).exists()
            if not conta_gerada:
                cancela = bool(np.choice([True, False], p=[0.3, 0.7]))
                if cancela:
                    c = Venda.objects.get(pk=i.pk)
                    c.status = False
                    c.data_cancelamento = (c.data_venda or c.data_pedido) + timedelta(days=random.randint(0,10))
                    c.botao_acionado = '_addcancelavenda'
                    c.save()