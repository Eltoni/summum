#-*- coding: UTF-8 -*-
from django.conf import settings
from django.db import connection, transaction
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import os
import runpy


class Command(BaseCommand):
    """
        Uso:
        python manage.py reset_project              : Executa todos os trabalhos do procedimento 
        python manage.py reset_project --arquivos   : Executa somente o código que atualiza os arquivos estáticos do projeto
        python manage.py reset_project --dados      : Executa somente o código que elimina e recria todas as tabelas do projeto
    """

    help = u'Elimina todas as tabelas; Recria as tabelas; Atualiza os arquivos estáticos e reinsere os dados padrões de teste'

    def add_arguments(self, parser):

        # (optional) arguments
        parser.add_argument('--dados',
            action='store_true',
            dest='dados',
            default=False,
            help='Elimina e recria todas as tabelas do banco de dados do projeto., inserindo os dados iniciais de todas as fixtures.')
        parser.add_argument('--not_fixtures_py',
            action='store_true',
            dest='not_fixtures_py',
            default=False,
            help='Elimina e recria todas as tabelas do banco de dados do projeto, inserindo os dados iniciais da fixture sql.')
        parser.add_argument('--arquivos',
            action='store_true',
            dest='arquivos',
            default=False,
            help='Atualiza os arquivos estáticos do projeto e das bibliotecas utilizadas pelo mesmo.')


    def handle(self, *args, **options):
        if options['arquivos'] or (not options['arquivos'] and not options['dados'] and not options['not_fixtures_py']):
            
            # verbosity: especificca a quantidade de notifiação e depurações retornados no shell; interactive: Evita a confirmação da execução do procedimento pelo usuário
            # Instala os arquivos estáticos necessários para a geração dos gráficos | Python NVD3
            call_command('bower_install', verbosity=0, interactive=False)
            # Coleta os arquivos estáticos | Django
            call_command('collectstatic', verbosity=0, interactive=False)

        if options['dados'] or (not options['arquivos'] and not options['dados'] and not options['not_fixtures_py']):
            
            # Elimina todas as tabelas do banco de dados | Django Extensions
            call_command('reset_db', verbosity=0, interactive=False)
            # Recria as tabelas do banco de dados do projeto | Django
            call_command('migrate', verbosity=0)
            # Carrega as fixtures do sistema.
            call_command('loaddata', 'fixture', verbosity=0)

            # Finaliza o procedimento caso o comando not_fixtures_py tenha sido especificado
            if options['not_fixtures_py']:
                return

            # Executa os scripts .py existentes no caminho declarado no atributo FIXTURES_PY do settings.py
            print('\n Iniciando procedimento de execução dos scripts Python:')
            files_py = settings.FIXTURES_PY
            for file in os.listdir(files_py):
                if file.endswith(".py"):
                    runpy.run_path(os.path.join(files_py, file))