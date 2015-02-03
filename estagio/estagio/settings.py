#-*- coding: UTF-8 -*-
"""
Django settings for estagio project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Caminho para o fixtures. Arquivo que popula os dados iniciais das tabelas da base de dados
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#$*7&2zayxbai-=@jdvn=r=mtsh^u-wh&_l@9v84%0&^&7wm-p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Modulos do sistema
    'pessoal',
    'localidade',
    'parametros_financeiros',
    'movimento',
    'compra',
    'venda',
    'contas_pagar',
    'contas_receber',
    'caixa',
    'configuracoes',
    'utilitarios',
    # Bibliotecas em uso pelo projeto
    'import_export',
    'smart_selects',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'estagio.urls'

WSGI_APPLICATION = 'estagio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    #     'NAME': 'intraead.db',                      # Or path to database file if using sqlite3.
    #     # The following settings are not used with sqlite3:
    #     'USER': '',
    #     'PASSWORD': '',
    #     'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
    #     'PORT': '',                      # Set to empty string for default.
    # },

    'default': {
        'ENGINE': 'django.db.backends.mysql',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'estagio',                        # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                               # Set to empty string for default.
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_URL = '/static/'


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# É possível informar vários diretórios para fornecer os arquivos estáticos do projeto
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# Django Suit
# -----------

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# Django Suit configuration example
SUIT_CONFIG = {
    'SEARCH_URL': '/auth/user/',
    # header
    'ADMIN_NAME': 'Sistema de Controle',
    'HEADER_DATE_FORMAT': 'l, j \d\e F \d\e Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    'MENU': (
        # Keep original label and models
        {'label': u'Autenticação', 'app':'auth'},
        'localidade',
        'pessoal',
        {'label': u'Movimentos', 'app':'movimento'},
        {'label': u'Parâmetros', 'app':'parametros_financeiros'},
        'compra',
        'venda',
        {'label': u'Contas à pagar', 'app':'contas_pagar', 'models': ('contaspagar', 'parcelascontaspagar', 'pagamento')},
        {'label': u'Contas à receber', 'app':'contas_receber', 'models': ('contasreceber', 'parcelascontasreceber', 'recebimento')},
        'caixa',
        {'label': u'Configurações', 'app':'configuracoes'},
        # Separator
        '-',
    )
}


# Email configuration
DEFAULT_FROM_EMAIL = 'gustavo.sdo@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gustavo.sdo@gmail.com'
EMAIL_HOST_PASSWORD = 'msfcxksqacshqhry'
EMAIL_PORT = 587