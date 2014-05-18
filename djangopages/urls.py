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

from django.conf.urls import patterns, include, url

from djangopages.views import DevTestView, DevTestViewTest

########################################################################################################################

urlpatterns = patterns('',
                       url(r'^$', DevTestViewTest.as_view(), name='devtest'),
                       url(r'^test1$', DevTestView.as_view(test='test1'), name='devtest1'),
                       url(r'^test2$', DevTestView.as_view(test='test2'), name='devtest2'),
                       url(r'^test3$', DevTestView.as_view(test='test3'), name='devtest3'),
                       url(r'^test4$', DevTestView.as_view(test='test4'), name='devtest4'),
                       url(r'^test5$', DevTestView.as_view(test='test5'), name='devtest5'),
                       url(r'^test6$', DevTestView.as_view(test='test6'), name='devtest6'),
                       url(r'^test7$', DevTestView.as_view(test='test7'), name='devtest7'),
                       )
