#-*- coding: UTF-8 -*-

from __future__ import absolute_import
# Isto fará com que o aplicativo seja sempre importado quando Django for carregado
from estagio.celery import app as celery_app


#Cria diretório das dependências caso o mesmo não exista
import os
if not os.path.exists('estagio/static/components/components'):
    os.makedirs('estagio/static/components/components')



# import subprocess
# subprocess.call('START /B celery -A estagio beat', shell=True)
# subprocess.call('START /B celery -A estagio worker', shell=True)

