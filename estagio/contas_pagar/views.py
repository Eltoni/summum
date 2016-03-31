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
import pytz
from datetime import datetime


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


@csrf_exempt
def efetiva_pagamento_parcela(request, id_parcela):
    if request.method == "POST":
        form = PagamentoForm(request.POST)

        # Checa a situação do caixa
        if not Caixa.objects.filter(status=1).exists():
            pagamento_confirmado = 0
            message = force_text(_(u"Não há caixa aberto. Para efetivar um pagamento é necessário ter o caixa aberto."))
            resposta = {"message": message, 'pagamento_confirmado': pagamento_confirmado,}
            return HttpResponse(json.dumps({"resposta" : resposta}), content_type="text/javascript")

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

        resposta = {'message': message, 'pagamento_confirmado': pagamento_confirmado,}
        return HttpResponse(json.dumps({"resposta" : resposta}), content_type="text/javascript")

    dados_pagamento = ParcelasContasPagar.objects.get(pk=id_parcela)
    juros = Decimal(dados_pagamento.calculo_juros()).quantize(Decimal("0.00"))
    multa = Decimal(dados_pagamento.calculo_multa()).quantize(Decimal("0.00"))
    valor = Decimal(dados_pagamento.valor_a_pagar()).quantize(Decimal("0.00"))
    data = {'form':PagamentoForm(initial={ 'parcelas_contas_pagar': id_parcela,
                                           'juros': juros,
                                           'multa': multa,
                                           'valor': valor,
                                           'data': datetime.utcnow().replace(tzinfo=pytz.utc)})}
    return render_to_response('admin/efetiva_pagamento_parcela.html', data, RequestContext(request))