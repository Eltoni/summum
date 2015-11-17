:: Acesso a pasta onde é possível iniciar o ambiente de desenvolvimento do contexto
cd ..\..\Scripts\
:: executa o arquivo para ativação do ambiente
call activate
:: volta a pasta do projeto e roda o projeto do contexto
cd ..\Projetos\estagio


:: Inicia os serviços consumidos pelo Celery
del "estagio\logs\celerybeat.pid"
start cmd /k celery -A estagio beat -l info -s estagio/logs/ -f estagio/logs/celerybeat.log --pidfile=estagio/logs/celerybeat.pid
start cmd /k celery -A estagio worker -l info -f estagio/logs/celeryworker.log

:: Define o diretório atual na variável "current_path"
:: Inicia o serviço Redis
:: Retorna para o diretório do projeto
set current_path=%cd%
cd C:\Program Files (x86)\Redis
start cmd /k redis-server.exe
cd %current_path%

