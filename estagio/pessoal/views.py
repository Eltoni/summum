from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from pessoal.models import Cliente
 
# Create your views here.
 
def get_dados_usuario(request, id):
    usuario = User.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  usuario)
    return HttpResponse(retorno, content_type="text/javascript")


def cliente_financeiro(request):
    cliente = Cliente.objects.filter() 

    data = {
        'title': 'Financeiro - Cliente',
        'cliente': cliente,
    }

    return render_to_response('admin/cliente_financeiro.html', data, context_instance=RequestContext(request))


def cliente_detalhe_financeiro(request, id_cliente):
    cliente = Cliente.objects.get(pk=id_cliente) 

    data = {
        'title': 'Detalhes financeiros - Cliente',
        'cliente': cliente,
    }

    return render_to_response('admin/cliente_detalhes_financeiros.html', data, context_instance=RequestContext(request))

