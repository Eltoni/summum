from venda.models import Venda
from celery import shared_task
from configuracoes.models import Parametrizacao
import datetime
from django.utils.timezone import utc


@shared_task
def cancela_pedido_venda_vencido():

    periodo_venc_pedido = Parametrizacao.objects.values_list('periodo_venc_pedido_venda')[0][0]
    vendas = Venda.objects.filter(pedido='S', status_pedido=False).exclude(status=True).values_list('pk')
    data = datetime.datetime.utcnow().replace(tzinfo=utc)

    if periodo_venc_pedido:
        for c in vendas:
            venda = Venda.objects.get(pk=c[0])
            dias_pedido = data - venda.data_pedido
            if dias_pedido.days > periodo_venc_pedido:
                venda.botao_acionado = '_addcancelavenda'
                venda.data_cancelamento = data
                venda.save()
