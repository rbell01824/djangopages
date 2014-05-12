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


def devtest():
    """
    Example of programmatic dpage.
    """
    # test layout facility
    page = DPage()
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
                r(c3(x41), c9(r(x42))),
                r(c3(x51), c9(r(x521),
                              r(x522),
                              rc4(x5231, x5232, x5233))))
    return page.render()


class DevTest0(DPage):
    """
    Example of class based dpage
    """
    pass


class DevTest1(DPage):
    """
    Class based dpage with render method overridden.  Objs style interface.
    """

    def render(self):
        """
        Override render to generate output from here
        """
        self.form = None
        self.objs.append(Text('This text comes from dpage.Text'))
        self.objs.append(Markdown('**Bold Markdown Text**'))
        self.objs.append(HTML('<h3>H3 text from DPageHTML</h3>'))
        content = self.render_objs()
        return render_to_response(self.template,
                                  {'content': content})


class DevTest2(DPage):
    """
    Basic test of layout facility.
    """

    def render(self):
        """
        Override
        """
        xr1 = Text('This text comes from dpage.Text')
        xr2 = Markdown('**Bold Markdown Text**')
        xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
        self.layout(rc12(xr1, xr2, xr3))
        return render_to_response(self.template,
                                  {'content': self.content})


class DevTest3(DPage):
    """
    Complex render test
    """

    def render(self):
        """
        Override
        """
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
        self.layout(rc12(x1),
                    rc6(x21, x22),
                    rc(x3),
                    r(c3(x41), c9(r(x42))),
                    r(c3(x51), c9(r(x521),
                                  r(x522),
                                  rc4(x5231, x5232, x5233))))
        return self.render_self()


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
        return DevTest3().render()

