#-*- coding: UTF-8 -*-
# python manage.py runscript fixtures.py.run_fixtures --script-args=contas_pagar pagamento
from fixtures.py.insert_1_Compra import ProcessoGeraCompra
from fixtures.py.insert_2_Venda import ProcessoGeraVenda
from fixtures.py.insert_3_ContasPagar import ProcessoGeraContasPagar
from fixtures.py.insert_4_ContasReceber import ProcessoGeraContasReceber
from fixtures.py.insert_5_Pagamento import ProcessoGeraPagamento
from fixtures.py.insert_6_Recebimento import ProcessoGeraRecebimento

def run(*args):
    if 'compra' in args or not args:
        ProcessoGeraCompra().gera_compra()
    if 'venda' in args or not args:
        ProcessoGeraVenda().gera_venda()
    if 'contas_pagar' in args or not args:
        ProcessoGeraContasPagar().gera_contas_pagar()
    if 'contas_receber' in args or not args:
        ProcessoGeraContasReceber().gera_contas_receber()
    if 'pagamento' in args or not args:
        ProcessoGeraPagamento().gera_pagamento()
    if 'recebimento' in args or not args:
        ProcessoGeraRecebimento().gera_recebimento()