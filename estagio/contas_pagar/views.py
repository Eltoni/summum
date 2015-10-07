#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from contas_pagar.models import Pagamento, ParcelasContasPagar, ContasPagar
from contas_pagar.forms import PagamentoForm
from django.utils.translation import ugettext_lazy as _
import json
from django.shortcuts import *
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.contrib.admin.models import LogEntry, ADDITION
from django.utils.encoding import force_text
from django.contrib.contenttypes.models import ContentType
from caixa.models import Caixa
from configuracoes.models import *


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
    }
    return render_to_response('admin/pagamentos_conta.html', data, context_instance=RequestContext(request))


@csrf_exempt
def efetiva_pagamento_parcela(request, id_parcela):
    if request.method == "POST":
        form = PagamentoForm(request.POST)

        # Checa a situação do caixa
        if not Caixa.objects.filter(status=1).exists():
            pagamento_confirmado = 0
            message = force_text(_(u"Não há caixa aberto. Para efetivar um pagamento é necessário ter o caixa aberto."))
            return HttpResponse(json.dumps({"message": message, 'pagamento_confirmado': pagamento_confirmado,}))

        # Checa a situação do valor do pagamento
        perc_valor_minimo_pagamento = Parametrizacao.objects.all().values_list('perc_valor_minimo_pagamento')[0][0]
        parcela = ParcelasContasPagar.objects.get(pk=id_parcela)
        valor_minimo_pagamento = round((parcela.valor_total() * perc_valor_minimo_pagamento) / 100, 2)
        primeiro_pagamento = Pagamento.objects.filter(parcelas_contas_pagar=id_parcela).exists()
        if Decimal(request.POST['valor']).quantize(Decimal("0.00")) < valor_minimo_pagamento and not primeiro_pagamento:
            pagamento_confirmado = 0
            message = force_text(_(u"Primeiro pagamento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: R$ %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_pagamento, 'valor_minimo': valor_minimo_pagamento})
            return HttpResponse(json.dumps({"message": message, 'pagamento_confirmado': pagamento_confirmado,}))


        if form.is_valid():
            pagamento_obj = form.save()

            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(pagamento_obj).pk,
                object_id       = pagamento_obj.pk,
                object_repr     = force_text(pagamento_obj), 
                action_flag     = ADDITION
            )

            pagamento_confirmado = 1
            message = force_text(_(u'Pagamento da parcela "%(p)s" efetuado com sucesso!') % {'p': id_parcela})

        return HttpResponse(json.dumps({'message': message, 'pagamento_confirmado': pagamento_confirmado,}))

    dados_pagamento = ParcelasContasPagar.objects.get(pk=id_parcela)
    juros = Decimal(dados_pagamento.calculo_juros()).quantize(Decimal("0.00"))
    multa = Decimal(dados_pagamento.calculo_multa()).quantize(Decimal("0.00"))
    valor = Decimal(dados_pagamento.valor_a_pagar()).quantize(Decimal("0.00"))
    data = {'form':PagamentoForm(initial={ 'parcelas_contas_pagar': id_parcela,
                                           'juros': juros,
                                           'multa': multa,
                                           'valor': valor,})}
    return render_to_response('admin/efetiva_pagamento_parcela.html', data, RequestContext(request))