#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.apps import apps


def checa_foreignkey_habilitada(request, app_name, model_name, id):
    model = apps.get_model(app_name, model_name)
    try:
        status = model.objects.get(id=id)
        try:
            condition = model._meta.get_field_by_name('status')[0]._get_val_from_obj(status)
            if not condition:
                status = False
            else:
                status = True
        except:
            status = True
    except:
        status = False
    
    return HttpResponse(status, content_type="text/javascript")