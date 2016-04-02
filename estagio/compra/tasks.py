#-*- coding: UTF-8 -*-
from django.utils.timezone import utc
from celery import shared_task

import datetime

from compra.models import Compra
from configuracoes.models import Parametrizacao


@shared_task
def cancela_pedido_compra_vencido():

    periodo_venc_pedido = Parametrizacao.objects.values_list('periodo_venc_pedido_compra')[0][0]
    compras = Compra.objects.filter(pedido='S', status_pedido=False).exclude(status=True).values_list('pk')
    data = datetime.datetime.utcnow().replace(tzinfo=utc)

    if periodo_venc_pedido:
        for c in compras:
            compra = Compra.objects.get(pk=c[0])
            dias_pedido = data - compra.data_pedido
            if dias_pedido.days > periodo_venc_pedido:
                compra.status = True
                compra.data_cancelamento = data
                compra.save()
