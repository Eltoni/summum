#-*- coding: UTF-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
import pytz

import json
from decimal import Decimal
from datetime import datetime

from contas_pagar.models import ContasPagar, ParcelasContasPagar, Pagamento
from contas_pagar.forms import PagamentoForm
from caixa.funcoes import caixa_aberto


def retorna_pagamentos_parcela(request, id_parcela):
    u""" Retorna os pagamentos efetuados para a parcela do contexto. """
    pagamentos = Pagamento.objects.filter(parcelas_contas_pagar=id_parcela).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar')
    parcela = ParcelasContasPagar.objects.get(pk=id_parcela)

    data = {
        'title': _(u"Pagamentos da parcela"),
        'app_name': parcela._meta.app_label,
        'opts': parcela._meta,
        'has_change_permission': False,
        'original': parcela,
        'pagamentos': pagamentos,
        'parcela': id_parcela,
    }
    return render_to_response('admin/pagamentos_parcela.html', data, context_instance=RequestContext(request))


def retorna_pagamentos_conta(request, id_conta):
    u""" Retorna os pagamentos efetuados para a conta do contexto. """
    pagamentos = Pagamento.objects.filter(parcelas_contas_pagar__contas_pagar=id_conta).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_pagar__contas_pagar')
    conta = ContasPagar.objects.get(pk=id_conta)

    data = {
        'title': _(u"Pagamentos da conta"),
        'app_name': conta._meta.app_label,
        'opts': conta._meta,
        'has_change_permission': False,
        'original': conta,
        'pagamentos': pagamentos,
        'conta': id_conta,
    }
    return render_to_response('admin/pagamentos_conta.html', data, context_instance=RequestContext(request))



class EfetivaPagamentoParcela(View):
    form_class = PagamentoForm
    template_name = 'admin/efetiva_pagamento_parcela.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(EfetivaPagamentoParcela, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        id_parcela = self.kwargs['id_parcela']
        dados_pagamento = ParcelasContasPagar.objects.get(pk=id_parcela)
        juros = Decimal(dados_pagamento.calculo_juros()).quantize(Decimal("0.00"))
        multa = Decimal(dados_pagamento.calculo_multa()).quantize(Decimal("0.00"))
        valor = Decimal(dados_pagamento.valor_a_pagar()).quantize(Decimal("0.00"))

        initial = { 
            'parcelas_contas_pagar': id_parcela,
            'juros': juros,
            'multa': multa,
            'valor': valor,
            'data': datetime.utcnow().replace(tzinfo=pytz.utc)
        }
        
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        id_parcela = self.kwargs['id_parcela']

        # Checa a situação do caixa
        if not caixa_aberto():
            texto = force_text(_(u'Não há caixa aberto. Para efetivar um pagamento é necessário ter o caixa aberto.'))
            resposta = {
                "message": texto, 
                'pagamento_confirmado': 0,
            }
            resposta = json.dumps({"resposta" : resposta})
            return HttpResponse(resposta, content_type="text/javascript")

        if form.is_valid():
            pagamento_obj = form.save()

            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(pagamento_obj).pk,
                object_id       = pagamento_obj.pk,
                object_repr     = force_text(pagamento_obj), 
                action_flag     = ADDITION
            )

            texto = force_text(_(u'Pagamento da parcela "%(p)s" efetuado com sucesso!') % {'p': id_parcela})
            resposta = {
                'message': texto, 
                'pagamento_confirmado': 1,
            }
            resposta = json.dumps({"resposta" : resposta})
            return HttpResponse(resposta, content_type="text/javascript")

        texto = force_text(_(u'Falha ao efetivar a transação. Favor, acione o suporte.'))
        resposta = {
            'message': texto, 
            'pagamento_confirmado': 0,
        }
        resposta = json.dumps({"resposta" : resposta})
        return HttpResponse(resposta, content_type="text/javascript")