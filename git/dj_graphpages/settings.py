"""
Django settings for dj_graphpages project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '27@9*07$@h4djs^7=r!b%ijhtc$946n3uzmjm0q&)g$13dz1f$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # 'django_admin_bootstrapped.bootstrap3',
    # 'django_admin_bootstrapped',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'django_extensions',
    'dj_graphpages',
    'graphpages',
    'chartkick',
    'chartkick_demo',
    'bootstrap3',
    # 'bootstrapform',
    'test_data',
    'taggit',
    'taggit_suggest',
    'django_ace',
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dj_graphpages.urls'

WSGI_APPLICATION = 'dj_graphpages.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = ''
STATIC_URL = '/static/'

import chartkick

STATICFILES_DIRS = (
    chartkick.js(),
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

# Django Suit configuration example
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Graph Pages - demo/demo',
    'HEADER_DATE_FORMAT': 'l, jS F Y',
    'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,     # Default True
    'CONFIRM_UNSAVED_CHANGES': True,    # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    'MENU_ICONS': {
        # 'sites': 'icon-leaf',
        # 'auth': 'icon-lock',
    },
    'MENU_OPEN_FIRST_CHILD': True,      # Default True
    'MENU_EXCLUDE': ('auth', 'sites'),
    # 'MENU': (
    #     #'sites',
    #     # {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     # {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Graph Pages', 'icon': 'icon-signal', 'models': ('graphpages.graphpage',)},
    #     {'label': 'Graph Tags', 'icon': 'icon-tags', 'models': ('graphpages.graphpagetags',)},
    #     {'label': 'Support', 'icon': 'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}

GRAPHPAGE_FORMPAGEHEADER ='{% extends "base.html" %}\n' \
                          '{% block content %}\n' \
                          '<div class="container-fluid">\n'
GRAPHPAGE_FORMPAGEFOOTER = '</div>\n' \
                           '{% endblock content %}'
GRAPHPAGE_CONFIG = {
    'graphpageheader': '{% extends "base.html" %}\n'
                       '{% load chartkick %}\n'
                       '{% block content %}\n'
                       '<div class="container-fluid">\n',
    'graphpagefooter': '</div>\n'
                       '{% endblock content %}',
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# Define template tags to include by default.
# The tag must be <application>.templatetags.<template tag lib>
# See https://djangosnippets.org/snippets/342/
TEMPLATE_TAGS = ('chartkick.templatetags.chartkick',
                 'graphpages.templatetags.graphpage_tags')
