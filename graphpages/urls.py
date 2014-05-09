#!/usr/bin/env python
# coding=utf-8

""" Some description here

2/21/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '2/21/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"


from django.conf.urls import patterns, url

from graphpages.views import GraphPageView

urlpatterns = patterns('',
                       url(r'graphpage/(?P<graph_pk>.+)$', GraphPageView.as_view(), name='graphpage'),
                       )
