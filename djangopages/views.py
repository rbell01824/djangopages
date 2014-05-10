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

from django.views.generic import View
from django.views.generic import ListView

from djangopages.libs import DPage, DPageText, DPageMarkdown, DPageHTML

########################################################################################################################
#
# Development test class based view
#
########################################################################################################################


class DevTestView(View):
    """
    View class for dev testing.
    """
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
        Execute the graph method and display the results.
        :param request:
        """
        dpage = DPage()
        dpage.objs.append(DPageText('This text comes from DPageText'))
        dpage.objs.append(DPageMarkdown('**Bold Markdown Text**'))
        dpage.objs.append(DPageHTML('<h3>H3 text from DPageHTML</h3>'))
        return dpage.render()

