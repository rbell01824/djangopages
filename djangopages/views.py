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

from loremipsum import get_paragraph

from django.views.generic import View
from django.views.generic import ListView

from djangopages.dpage import *

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
        page = DPage()
        # Initial tests
        # page.objs.append(Text('This text comes from dpage.Text'))
        # page.objs.append(Markdown('**Bold Markdown Text**'))
        # page.objs.append(HTML('<h3>H3 text from DPageHTML</h3>'))

        # test layout facility
        # xr1 = Text('This text comes from dpage.Text')
        # xr2 = Markdown('**Bold Markdown Text**')
        # xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
        # page.layout(rc12(xr1, xr2, xr3))

        # test layout facility
        x1 = Text('Row 1: This text comes from dpage.Text')
        x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
        x22 = HTML('<p>Row 2 col 2: </p><h3>H3 text from DPageHTML</h3>')
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(get_paragraph()))
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(get_paragraph()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(get_paragraph()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(get_paragraph()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(get_paragraph()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(get_paragraph()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(get_paragraph()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(get_paragraph()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(get_paragraph()))
        # page.layout(r(c3(x41), c9(x42)))
        page.layout(rc12(x1),
                    rc6(x21, x22),
                    rc(x3),
                    # r(c3(x41), c9(x42)),
                    r(c3(x51), c9(r(x521),
                                  r(x522),
                                  rc4(x5231, x5232, x5233))))
        return page.render()

