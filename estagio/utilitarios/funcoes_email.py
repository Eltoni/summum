#-*- coding: UTF-8 -*-
from datetime import date
        
class TextosEmail(object):
    ano_atual = date.today().year
    
    headerEmailInterno = u'<div style="color:#fff; font-size: 18px; text-shadow: 0 -1px #121414;\
                            background-color: #373b3d; padding: 10px;">Sistema de Controle</div><hr>'
                    
    footerEmailInterno = u'<hr>\
                            <div style="color: #666; background-color: #d5d7d8;\
                            font-size: 11px; line-height: 1.5em;\
                            text-shadow: 0 1px rgba(255,255,255,0.5); height:60px;">\
                            <div style="border-top: 5px solid #e1e3e5;">\
                            <div style="padding: 9px 20px 0 0; float: right;text-align: right;">\
                                Copyright © %(ano_atual)s Versão - Estágio\
                            </div>\
                            <div style="padding: 15px 0 0 0; margin: 0 auto; width: 200px;text-align: center;">\
                                Sistema de Controle\
                            </div>\
                            </div>\
                            </div>' % {'ano_atual': ano_atual}