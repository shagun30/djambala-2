# -*- coding: utf-8 -*-
"""
/dms/settings.py

Konfiguation des Django Content Management Systems

Hans Rauch
hans.rauch@gmx.net

Die Programme des dms-Systems koennen frei genutzt und den spezifischen
Beduerfnissen entsprechend angepasst werden.
"""

from ConfigParser import RawConfigParser
from django.utils.translation import ugettext as _

config = RawConfigParser()
config.read('/data/django_projects/dms.ini')

DEFAULT_CHARSET = 'utf-8'

# Django settings for dms project.

#DEBUG = False
#TEMPLATE_DEBUG = DEBUG
DEBUG = config.getboolean('debug','DEBUG')
TEMPLATE_DEBUG = config.getboolean('debug','TEMPLATE_DEBUG')

#ADMINS = (
#    (config.get('email', 'ADMIN_NAME'), config.get('email', 'ADMIN_EMAIL')),
#)
ADMINS = eval(config.get('email', 'ADMIN'))
SERVER_EMAIL = config.get('email', 'SERVER_EMAIL')
EMAIL_HOST = config.get('email', 'EMAIL_HOST')
EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
CONTROL_EMAIL = config.get('email', 'CONTROL_EMAIL')
BULK_EMAIL_PATH = config.get('email', 'BULK_EMAIL_PATH')

MANAGERS = ADMINS

DATABASE_ENGINE   = ''  # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME     = ''  # Or path to database file if using sqlite3.
DATABASE_USER     = ''  # Not used with sqlite3.
DATABASE_PASSWORD = ''  # Not used with sqlite3.
DATABASE_HOST     = ''  # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT     = ''  # Set to empty string for default. Not used with sqlite3.

DATABASE_ENGINE   = config.get('database', 'DATABASE_ENGINE')
DATABASE_NAME     = config.get('database', 'DATABASE_NAME')
DATABASE_USER     = config.get('database', 'DATABASE_USER')
DATABASE_PASSWORD = config.get('database', 'DATABASE_PASSWORD')
DATABASE_HOST     = config.get('database', 'DATABASE_HOST')
DATABASE_PORT     = config.get('database', 'DATABASE_PORT')

try:
  DATABASE_SCHOOL_ENGINE   = config.get('db_schul_db', 'DATABASE_ENGINE')
  DATABASE_SCHOOL_NAME     = config.get('db_schul_db', 'DATABASE_NAME')
  DATABASE_SCHOOL_USER     = config.get('db_schul_db', 'DATABASE_USER')
  DATABASE_SCHOOL_PASSWORD = config.get('db_schul_db', 'DATABASE_PASSWORD')
  DATABASE_SCHOOL_HOST     = config.get('db_schul_db', 'DATABASE_HOST')
  DATABASE_SCHOOL_PORT     = config.get('db_schul_db', 'DATABASE_PORT')
except:
  DATABASE_SCHOOL_ENGINE   = ''
  DATABASE_SCHOOL_NAME     = ''
  DATABASE_SCHOOL_USER     = ''
  DATABASE_SCHOOL_PASSWORD = ''
  DATABASE_SCHOOL_HOST     = ''
  DATABASE_SCHOOL_PORT     = ''

#OTHER_DATABASES = {
#  'schul_db': {
#                'DATABASE_ENGINE'  : config.get('db_schul_db', 'DATABASE_ENGINE'),
#                'DATABASE_NAME'    : config.get('db_schul_db', 'DATABASE_NAME'),
#                'DATABASE_USER'    : config.get('db_schul_db', 'DATABASE_USER'),
#                'DATABASE_PASSWORD': config.get('db_schul_db', 'DATABASE_PASSWORD'),
#                'DATABASE_HOST'    : config.get('db_schul_db', 'DATABASE_HOST'),
#                'DATABASE_PORT'    : config.get('db_schul_db', 'DATABASE_PORT'),
#                'MODELS'           : ['DmsSchulstamm', 'DmsSchulstelle', 'DmsSchulrec']
#  },
#  'vm_db': {
#                'DATABASE_ENGINE'  : config.get('schul_db', 'DATABASE_ENGINE'),
#                'DATABASE_NAME'    : config.get('schul_db', 'DATABASE_NAME'),
#                'DATABASE_USER'    : config.get('schul_db', 'DATABASE_USER'),
#                'DATABASE_PASSWORD': config.get('schul_db', 'DATABASE_PASSWORD'),
#                'DATABASE_HOST'    : config.get('schul_db', 'DATABASE_HOST'),
#                'DATABASE_PORT'    : config.get('schul_db', 'DATABASE_PORT'),
#                'MODELS'           : ['dms_fortbildung']
#  }
#}

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/data/django_projects/dms_projekt/media/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = config.get('admin_media', 'PREFIX')

# Make this unique, and don't share it with anybody.
#SECRET_KEY = ''
SECRET_KEY = config.get('secrets','SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

#CACHE_BACKEND = 'memcached://127.0.0.1:11211'
#CACHE_BACKEND = 'locmem:///'
#CACHE_BACKEND = 'db://cache_tb'

#CACHE_BACKEND = 'file:///var/tmp/django_cache'
CACHE_BACKEND = config.get('cache', 'CACHE_METHOD')
CACHE_MIDDLEWARE_SECONDS = 3600  # 1 Stunde
CACHE_MIDDLEWARE_KEY_PREFIX = 'site_01_'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    #'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dms.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.CacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'dms.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/data/django_projects/dms_projekt/templates',
    '/data/django_projects/dms_projekt/templates_css',
    '/data/django_projects/dms_projekt/dms/templates',
    '/data/django_projects/dms_projekt/dms/templates_css',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    #"django.core.context_processors.debug",
    "django.core.context_processors.i18n",
)

INSTALLED_APPS = (
    'dms.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    #'django.contrib.databrowse',
    'dms',
    'dms.wiki',
    'dms.edufolder',
    'dms.elixier',
    'dms.mediasurvey',
    'dms.survey',
    'dms.fortbildung',
    'dms.resource',
    #'dms.agenda',
)

SESSION_COOKIE_DOMAIN = config.get('session_cookie', 'DOMAIN')
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTHENTICATION_BACKENDS = (
    'dms.auth.backends.ModelBackend',
)

MY_DOMAINS = eval(config.get('domain', 'MY'))
SEARCH_DOMAIN = config.get('domain', 'SEARCH')
CURRICULUM_DOMAIN = config.get('domain', 'CURRICULUM')
MP3_DOMAIN = config.get('domain', 'MP3')
MP3_DOWNLOAD = config.get('domain', 'MP3_DOWNLOAD')

MEDIEN_ROOT = '/data/django_projects/dms_projekt/dms/media/'
MEDIEN_URL = config.get('host_url', 'BASE_SITE_URL') + '/dms_media/'
HELP_URL = config.get('help', 'URL')
BASE_SITE_URL = config.get('host_url', 'BASE_SITE_URL')
DOWNLOAD_PATH = config.get('download', 'DOWNLOAD_PATH')
FREEMIND_PATH = config.get('download', 'FREEMIND_PATH')
DOWNLOAD_URL  = config.get('download', 'DOWNLOAD_URL')
DOWNLOAD_PROTECTED_PATH = config.get('download', 'DOWNLOAD_PROTECTED_PATH')

DB_SEARCHENGINE   = config.get('search_engine', 'DB_PATH')
RPC_SEARCHENGINE  = config.get('search_engine', 'XMLRPC_URL')
PDF_TO_TEXT       = config.get('search_engine', 'PDF_TO_TEXT')
WORD_TO_TEXT      = config.get('search_engine', 'WORD_TO_TEXT')

TMP_PATH          = config.get('pdf_confirm', 'TMP_PATH')
START_OF_LETTER   = config.get('pdf_confirm', 'START_OF_LETTER')
ADDRESS           = config.get('pdf_confirm', 'ADDRESS')
SENDER_EMAIL      = config.get('pdf_confirm', 'SENDER_EMAIL')
REPLY_EMAIL       = config.get('pdf_confirm', 'REPLY_EMAIL')
BACKUP_EMAIL      = config.get('pdf_confirm', 'BACKUP_EMAIL')
COMMUNITY_URL     = config.get('pdf_confirm', 'COMMUNITY_URL')

BOTTOM_OF_LETTER  = config.get('pdf_saved_infos', 'BOTTOM_OF_LETTER')
ORGANISATION      = config.get('pdf_saved_infos', 'ORGANISATION')
ADDRESS_OF_LETTER = config.get('pdf_saved_infos', 'ADDRESS_OF_LETTER')
KONTACT_NAME      = config.get('pdf_saved_infos', 'KONTACT_NAME')
KONTACT_PHONE     = config.get('pdf_saved_infos', 'KONTACT_PHONE')
KONTACT_FAX       = config.get('pdf_saved_infos', 'KONTACT_FAX')
KONTACT_EMAIL     = config.get('pdf_saved_infos', 'KONTACT_EMAIL')
GOOD_BYE          = config.get('pdf_saved_infos', 'GOOD_BYE')
INST_LOGO_PATH    = config.get('pdf_saved_infos', 'INST_LOGO_PATH')

EDUFOLDER_SOURCE  = config.get('edu_folder', 'ELIXIER_SRC')
EDUFOLDER_LANGUAGE= 'de'
EDUFOLDER_BASE_PATH = config.get('edu_folder', 'BASE_PATH')
ELIXIER_LOGOS_PATH= config.get('edu_folder', 'ELIXIER_LOGO_PATH')
ELIXIER_LOGOS_URL = DOWNLOAD_URL + ELIXIER_LOGOS_PATH
EDUFOLDER_INST_LOGO_URL = ELIXIER_LOGOS_URL + config.get('edu_folder', 'ELIXIER_INST_LOGO')
EDUFOLDER_TRAINING_URL =  config.get('edu_folder', 'TRAINING_URL')

LDAP_AUTH_USER = config.get('ldap', 'AUTH_USER')
LDAP_AUTH_USER_PASSWORD = config.get('ldap', 'AUTH_USER_PASSWORD')
#LDAP_MASTER = config.get('ldap', 'AUTH_MASTER')
#LDAP_MASTER_PASSWORD = config.get('ldap', 'AUTH_MASTER_PASSWORD')
LDAP_HOST = config.get('ldap', 'AUTH_LDAP_HOST')
LDAP_PORT = config.get('ldap', 'AUTH_LDAP_PORT')
LDAP_DN = config.get('ldap', 'AUTH_LDAP_DN')
LDAP_MODE = eval(config.get('ldap', 'AUTH_LDAP_MODE'))

CSS_ORG = config.get('css', 'CSS_ORG_NAME')

ORG = eval(config.get('org_apps', 'ORG'))
ORG_DB = eval(config.get('org_apps', 'ORG_DB'))

HOME_PATH = config.get('home', 'PATH')
HOME_QUOTA = eval(config.get('home', 'QUOTA'))
HAS_HOMES = eval(config.get('home', 'HAS_HOMES'))

EXERCISE_LAYOUT = eval(config.get('exercisefolder', 'LAYOUT'))
