#-*- coding: UTF-8 -*-
from django.conf import settings
from datetime import date

ADMIN_NAME = settings.ADMIN_NAME.encode('utf-8').decode("utf-8")

class TextosEmail(object):
    ano_atual = date.today().year
    
    headerEmailInterno = u'<div style="color:#fff; font-size: 18px; text-shadow: 0 -1px #121414;\
                            background-color: #373b3d; padding: 10px;">%(ADMIN_NAME)s</div><hr>' % {'ADMIN_NAME': ADMIN_NAME,}
                    
    footerEmailInterno = u'<hr>\
                            <div style="color: #666; background-color: #d5d7d8;\
                            font-size: 11px; line-height: 1.5em;\
                            text-shadow: 0 1px rgba(255,255,255,0.5); height:60px;">\
                            <div style="border-top: 5px solid #e1e3e5;">\
                            <div style="padding: 9px 20px 0 0; float: right;text-align: right;">\
                                Copyright © %(ano_atual)s Versão - Estágio\
                            </div>\
                            <div style="padding: 15px 0 0 0; margin: 0 auto; width: 200px;text-align: center;">\
                                %(ADMIN_NAME)s\
                            </div>\
                            </div>\
                            </div>' % {'ano_atual': ano_atual, 'ADMIN_NAME': ADMIN_NAME,}