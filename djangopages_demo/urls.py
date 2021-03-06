#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/7/14 - Initial creation

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

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from djangopages_demo.views import index, DemoList
from djangopages.pages.views import DPagesList, DPageView
from graphpages.views import GraphPageListView

urlpatterns = patterns('',
    url(r'^dpages/$', DPagesList.as_view(), name='DPagesList'),
    url(r'^dpages/(.*$)', DPageView.as_view(), name='dpagesview'),
    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$', GraphPageListView.as_view(), name=GraphPageListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^chartkick/', include('chartkick_demo.urls')),
    url(r'^table2/', include('django_tables2_demo.urls')),
    url(r'^$', login_required(index), name='index'),
    url(r'^demo', DemoList.as_view(), name='DpagesList2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
)
urlpatterns += staticfiles_urlpatterns()
