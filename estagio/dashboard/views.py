#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView

import pandas as pd

from movimento.models import Produtos
from configuracoes.models import Parametrizacao
from caixa.models import MovimentosCaixa


class DashboardMainView(TemplateView):
    template_name = 'admin/main.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardMainView, self).get_context_data(**kwargs)

        parametrizacao = Parametrizacao.objects.values_list('qtde_minima_produtos_em_estoque', 'evento_calendario')[0]
        evento_calendario = parametrizacao[1]
        quantidade_minima = parametrizacao[0]

        try:
            produtos_esgotando = Produtos.objects.filter(status=True, quantidade__lte=quantidade_minima).values_list('id', 'nome', 'quantidade').order_by('quantidade', 'id')
        except:
            produtos_esgotando = None 

        # Início do bloco - Manipula os dados que serão utilizados no gráfico de movimentos financeiros
        #----------------------------------------------------------------------------------------------
        mov = MovimentosCaixa.objects.all().values()                                                        # retorna todos os movimentos de caixa
        mv_df = pd.DataFrame.from_records(mov)                                                              # gera o DataFrame do dicionário
        mv_df = mv_df.drop(['descricao', 'caixa_id', 'id', 'pagamento_id', 'recebimento_id'], axis=1)       # remove colunas desnecessárias do DataFrame
        mv_df['data'] = mv_df['data'].dt.date                                                               # converte coluna data para o formato date
        mv_df['valor'] = mv_df['valor'].fillna(0)                                                           # converte valores NaN (nulos) para 0.0
        mv_df_gr = mv_df.groupby([mv_df['data'], mv_df['tipo_mov']], as_index=False).sum()                  # agrupa por data e tipo de movimento, e soma os valores de movimento 
        mv_df_gr = mv_df.groupby([mv_df['data'], mv_df['tipo_mov']], as_index=False).sum()

        credito = mv_df_gr[mv_df_gr['tipo_mov'] == 'Crédito']                                               # filtra por todos os movimentos de débito. Numa condição com múltiplos filtros, basta utilizar: e[(e['tipo_mov_x'] == 'Débito') & (e['tipo_mov_y'] == 'Crédito')]
        debito = mv_df_gr[mv_df_gr['tipo_mov'] == 'Débito']                                                 # filtra por todos os movimentos de crédito

        all_credito = pd.merge(credito, debito, on='data', how='left')                                      # simula um LEFT JOIN retornando todos os movimentos do tipo Crédito. Outras opções de união são row=['left';'outer']
        all_credito['tipo_mov_y'] = all_credito['tipo_mov_y'].fillna('Débito')                              # converte valores NaN (nulos) para Débito
        all_credito['valor_y'] = all_credito['valor_y'].fillna(0)                                           # converte valores NaN (nulos) para 0

        all_debito = pd.merge(credito, debito, on='data', how='right')                                      # simula um RIGHT JOIN retornando todos os movimentos do tipo Débito
        all_debito['tipo_mov_x'] = all_debito['tipo_mov_x'].fillna('Crédito')                               # converte valores NaN (nulos) para Crédito
        all_debito['valor_x'] = all_debito['valor_x'].fillna(0)                                             # converte valores NaN (nulos) para 0

        all_movimentos = pd.concat([all_credito, all_debito]).drop_duplicates()                             # simula um UNION dos créditos e débitos descartando resultados duplicadas
        all_movimentos = all_movimentos.sort_values(by=['data']).reset_index(drop=True)                     # ordena o resultado pela data do movimento e reindexa o índice

        all_movimentos = all_movimentos.to_dict()

        data_movimento = [ i.strftime('%d/%m/%Y') for i in list(all_movimentos['data'].values()) ]
        credito_movimento = [ float(i) for i in list(all_movimentos['valor_x'].values()) ]
        debito_movimento = [ float(i) for i in list(all_movimentos['valor_y'].values()) ]

        grafico_mov_dia = all_movimentos or None
        #----------------------------------------------------------------------------------------------
        # Fim do bloco
        
        if self.request.user.has_perm('schedule.add_event'): 
            editar_evento = 'true'
        else:
            editar_evento = 'false'

        context['title'] = 'Dashboard'
        context['produtos_esgotando'] = produtos_esgotando
        context['quantidade_minima'] = quantidade_minima

        context['evento_calendario'] = evento_calendario
        context['editar_evento'] = editar_evento

        context['data_movimento'] = data_movimento
        context['debito_movimento'] = debito_movimento
        context['credito_movimento'] = credito_movimento
        context['grafico_mov_dia'] = grafico_mov_dia

        return context


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.render_to_response(context=context)