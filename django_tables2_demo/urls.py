#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/18/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/18/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"


from django.conf.urls import patterns, url

from .views import table2

urlpatterns = patterns('',
                       url(r'^$', table2, name='table2_demo'),
                       )
