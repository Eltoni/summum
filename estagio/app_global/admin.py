#-*- coding: UTF-8 -*-
from django.contrib import admin
from django.contrib.admin.views.main import IS_POPUP_VAR


class GlobalAdmin(admin.ModelAdmin):
    """ Classe admin criada para que seja herdada para outras classes admin das aplicações.
        Com ela é possível definir os campos que serão exibidos exclusivamente na paginação de modelos em janelas popups
    """

    popup_list_display = ()
    popup_list_filter = ()

    def get_list_display(self, request):
        if IS_POPUP_VAR in request.GET and self.popup_list_display: # return list_display if not set
            return self.popup_list_display
        else:
            return self.list_display

    def get_list_filter(self, request):
        if IS_POPUP_VAR in request.GET:                             # return empty tuple if not set
            return self.popup_list_filter
        else:
            return self.list_filter