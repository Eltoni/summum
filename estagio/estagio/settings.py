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
HOME_PATH = os.path.expanduser('~')


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
    'app_global',
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
    'salmonella',
    'djangobower',
    'django_nvd3',
    'sorl.thumbnail',
    'selectable',
    'daterange_filter',
    'selectable_filter',
    'debug_toolbar',
    'geoposition',
    'suit_redactor',
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

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

LANGUAGE_CODE = 'pt-br'

ugettext = lambda s: s
LANGUAGES = (
    ('pt-br', ugettext('Português')),
    ('en', ugettext('Inglês')),
)

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1



# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'estagio/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'estagio/static')


STATIC_URL = '/static/'


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# É possível informar vários diretórios para fornecer os arquivos estáticos do projeto
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'djangobower.finders.BowerFinder',
)


# Django Suit
# -----------
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

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
        {'label': u'Autenticação', 'app':'auth'},
        {'app':'localidade', 'icon':'icon-globe'},
        {'app':'pessoal', 'icon':'icon-user'},
        {'label': u'Movimentos', 'app':'movimento', 'models': ('produtos', 'marca', 'categoria')},
        {'label': u'Parâmetros', 'app':'parametros_financeiros', 'icon':'icon-barcode', 'models': ('formapagamento', 'grupoencargo')},
        {'app':'compra', 'icon':'icon-shopping-cart'}, 
        {'label': u'Venda', 'app':'venda', 'icon':'icon-shopping-cart', 'models': ('venda', 'entregavenda')},
        {'label': u'Contas à pagar', 'icon':'icon-folder-close', 'app':'contas_pagar', 'models': ('contaspagar', 'parcelascontaspagar', 'pagamento')},
        {'label': u'Contas à receber', 'icon':'icon-folder-open', 'app':'contas_receber', 'models': ('contasreceber', 'parcelascontasreceber', 'recebimento')},
        {'app':'caixa', 'icon':'icon-inbox'},
        {'label': u'Configurações', 'icon':'icon-wrench', 'app':'configuracoes'},
        # Separator
        '-',
        '-',
        {'label': u'relatórios', 'icon':'icon-th-list', 'permissions': 'movimento.visualizar_relatorios', 'models': [
            {'label': u'Venda', 'url': '/#'},
        ]},
    )
}


# django Selectable
# -----------
SELECTABLE_MAX_LIMIT = 10


# Django Nvd3
# -----------
BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'estagio/static/components')

BOWER_PATH = HOME_PATH + '/AppData/Roaming/npm/bower.cmd'

BOWER_INSTALLED_APPS = (
    'd3#3.3.13',
    'nvd3#1.7.1',
)

# Email configuration
DEFAULT_FROM_EMAIL = 'gustavo.sdo@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gustavo.sdo@gmail.com'
EMAIL_HOST_PASSWORD = 'msfcxksqacshqhry'
EMAIL_PORT = 587