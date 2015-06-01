#-*- coding: UTF-8 -*-
#Cria diretório das dependências caso o mesmo não exista

import os
if not os.path.exists('estagio/static/components/components'):
    os.makedirs('estagio/static/components/components')