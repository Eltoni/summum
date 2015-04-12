from django.shortcuts import render

from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
 
# Create your views here.
 
def get_dados_usuario(request, id):
    usuario = User.objects.all().filter(id=id)
    retorno = serializers.serialize("json",  usuario)
    return HttpResponse(retorno, content_type="text/javascript")