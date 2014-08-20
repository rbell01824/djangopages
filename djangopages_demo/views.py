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

from djangopages.dpage import *
from djangopages.dpage_layout import *
from djangopages.dpage_bootstrap3 import *
from djangopages.dpage_graphs import *
from djangopages.dpage_texthtml import *
from django.http import HttpResponseNotFound
from django.views.generic import View

########################################################################################################################

from django.shortcuts import render


def index(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)


class DPagesList2(DPage):
    """ List the available DPage(s) """
    title = 'DjangoPages List 2'
    description = 'List the test/demo DPages'
    tags = ['list_test']

    def get(self, *args, **kwargs):
        """ List available pages """
        t = '<a href="/dpages/{name}" ' \
            'class="btn btn-default btn-xs" ' \
            'role="button" ' \
            'style="width:400px;text-align:left;margin-bottom:2px;">' \
            '{text}' \
            '</a><br/>\n'
        # noinspection PyUnresolvedReferences
        pages = DPage.pages_list
        out = ''
        for page in pages:
            # get the class definition for this page
            cls = page['cls']
            # make a link button object to execute an instance of the class
            # lnk = Link('/dpages/{name}'.format(name=cls.__name__), cls.title)
            # lnkbtn = Button(lnk, btn_size='btn-xs')
            # Output a line with the link button, test title, and test description
            line = t.format(name=cls.__name__, text=cls.title)
            out += line
        self.content = out
        return self
