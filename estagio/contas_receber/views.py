#-*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from contas_receber.models import Recebimento, ParcelasContasReceber, ContasReceber
from contas_receber.forms import RecebimentoForm
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


def retorna_recebimentos_parcela(request, id_parcela):
    u""" Retorna os recebimentos efetuados para a parcela do contexto. """
    recebimentos = Recebimento.objects.filter(parcelas_contas_receber=id_parcela).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber')
    parcela = ParcelasContasReceber.objects.get(pk=id_parcela)

    data = {
        'title': _(u"Recebimentos da parcela"),
        'app_name': parcela._meta.app_label,
        'opts': parcela._meta,
        'has_change_permission': False,
        'original': parcela,
        'recebimentos': recebimentos,
        'parcela': id_parcela,
    }
    return render_to_response('admin/recebimentos_parcela.html', data, context_instance=RequestContext(request))


def retorna_recebimentos_conta(request, id_conta):
    u""" Retorna os recebimentos efetuados para a conta do contexto. """
    recebimentos = Recebimento.objects.filter(parcelas_contas_receber__contas_receber=id_conta).values_list('pk', 'data', 'valor', 'juros', 'multa', 'desconto', 'parcelas_contas_receber__contas_receber')
    conta = ContasReceber.objects.get(pk=id_conta)

    data = {
        'title': _(u"Recebimentos da conta"),
        'app_name': conta._meta.app_label,
        'opts': conta._meta,
        'has_change_permission': False,
        'original': conta,
        'recebimentos': recebimentos,
        'conta': id_conta,
    }
    return render_to_response('admin/recebimentos_conta.html', data, context_instance=RequestContext(request))


@csrf_exempt
def efetiva_recebimento_parcela(request, id_parcela):
    if request.method == "POST":
        form = RecebimentoForm(request.POST)

        # Checa a situação do caixa
        if not Caixa.objects.filter(status=1).exists():
            recebimento_confirmado = 0
            message = force_text(_(u"Não há caixa aberto. Para efetivar um recebimento é necessário ter o caixa aberto."))
            return HttpResponse(json.dumps({"message": message, 'recebimento_confirmado': recebimento_confirmado,}))

        # Checa a situação do valor do recebimento
        perc_valor_minimo_recebimento = Parametrizacao.objects.all().values_list('perc_valor_minimo_recebimento')[0][0]
        parcela = ParcelasContasReceber.objects.get(pk=id_parcela)
        valor_minimo_recebimento = round((parcela.valor_total() * perc_valor_minimo_recebimento) / 100, 2)
        primeiro_recebimento = Recebimento.objects.filter(parcelas_contas_receber=id_parcela).exists()
        if Decimal(request.POST['valor']).quantize(Decimal("0.00")) < valor_minimo_recebimento and not primeiro_recebimento:
            recebimento_confirmado = 0
            message = force_text(_(u"Primeiro recebimento deve ser de no mínimo %(perc_valor_minimo)s%% do valor da parcela. Valor mínimo: R$ %(valor_minimo)s.") % {'perc_valor_minimo': perc_valor_minimo_recebimento, 'valor_minimo': valor_minimo_recebimento})
            return HttpResponse(json.dumps({"message": message, 'recebimento_confirmado': recebimento_confirmado,}))


        if form.is_valid():
            recebimento_obj = form.save()

            LogEntry.objects.log_action(
                user_id         = request.user.pk, 
                content_type_id = ContentType.objects.get_for_model(recebimento_obj).pk,
                object_id       = recebimento_obj.pk,
                object_repr     = force_text(recebimento_obj), 
                action_flag     = ADDITION
            )

            recebimento_confirmado = 1
            message = force_text(_(u'Recebimento da parcela "%(p)s" efetuado com sucesso!') % {'p': id_parcela})

        return HttpResponse(json.dumps({'message': message, 'recebimento_confirmado': recebimento_confirmado,}))

    dados_recebimento = ParcelasContasReceber.objects.get(pk=id_parcela)
    juros = Decimal(dados_recebimento.calculo_juros()).quantize(Decimal("0.00"))
    multa = Decimal(dados_recebimento.calculo_multa()).quantize(Decimal("0.00"))
    valor = Decimal(dados_recebimento.valor_a_receber()).quantize(Decimal("0.00"))
    data = {'form':RecebimentoForm(initial={'parcelas_contas_receber': id_parcela,
                                            'juros': juros,
                                            'multa': multa,
                                            'valor': valor,
                                            'data': datetime.utcnow().replace(tzinfo=pytz.utc)})}
    return render_to_response('admin/efetiva_recebimento_parcela.html', data, RequestContext(request))