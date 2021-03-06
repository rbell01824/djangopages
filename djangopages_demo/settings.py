#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/7/14 - Initial creation

Django settings for djangopages_demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/7/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

########################################################################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2as*)!##mb4*%321=%*y%yu#qiqevn@(9lfnc&mcqju)c^onqw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'django_extensions',
    #
    # apps to support djangopages
    #
    # 'bootstrap3',                   # toto 1: probably deprecated but leave for time being
    'chartkick',
    # 'django_tables2',               # todo 1: probably deprecated but leave for time being
    'taggit',
    'taggit_suggest',
    # 'django_ace',                   # todo 1: probably deprecated but leave for time being
    #
    # djangopages proper
    #
    'djangopages',
    'graphpages',                    # todo 1: deprecated but leave for time being
    #
    # start of demo applications
    #
    'djangopages_demo',
    'chartkick_demo',
    'django_tables2_demo',
    'test_data',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'djangopages_demo.urls'

WSGI_APPLICATION = 'djangopages_demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = '/home/richabel/ProjDjangoPages/static/'
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

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s:%(funcName)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + "/logfile",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}

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

from djangopages.settings import *

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
