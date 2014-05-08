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

from djangopages_demo.views import index
# from djangopages_demo.views import GraphPageListView               # fixme:

urlpatterns = patterns('',

    # url(r'^test_data/', include('test_data.urls')),               # fixme:
    # url(r'^display_graph_pages$', GraphPageListView.as_view(), name=GraphPageListView),               # fixme:
    # url(r'^graphpages/', include('graphpages.urls')),               # fixme:
    url(r'^chartkick/', include('chartkick_demo.urls')),
    # url(r'^admin/', include(admin.site.urls)),               # fixme:

    url(r'^$', login_required(index), name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', login, {'template_name': 'admin/login.html'}),
)

urlpatterns += staticfiles_urlpatterns()
