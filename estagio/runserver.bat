:: Nomeia a janela do prompt
TITLE Estagio
:: seta o tamanho da janela
::mode con:cols=120 lines=42

:: Acesso a pasta onde é possível iniciar o ambiente de desenvolvimento do contexto
cd ..\..\Scripts\
:: executa o arquivo para ativação do ambiente
call activate
:: volta a pasta do projeto e roda o projeto do contexto
cd ..\Projetos\estagio
python manage.py runserver
pause

:: Inicia o prompt novamente
start