#!/usr/bin/env python

"""

11/18/13 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '11/18/13'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"
__status__ = "dev"

from django.conf.urls import patterns, include, url

from test_data.views import ListCIAView
from test_data.views import ListCountriesView
from test_data.views import Demo8aView
from test_data.views import Demo8bView
from test_data.views import Demo8cView
from test_data.views import Demo8dView

urlpatterns = patterns('',
                       url(r'demo8a$', Demo8aView.as_view(), name='demo8a'),
                       url(r'demo8b$', Demo8bView.as_view(), name='demo8b'),
                       url(r'demo8c$', Demo8cView.as_view(), name='demo8c'),
                       url(r'demo8d$', Demo8dView.as_view(), name='demo8d'),
                       url(r'^cia$', ListCIAView.as_view(), name='cia_list', ),
                       url(r'^countries$', ListCountriesView.as_view(), name='countries_list', ),
                       )
