#!/usr/bin/env python
# coding=utf-8

"""
Widget Base Classes
*******************

.. module:: widgets
   :synopsis: Provides DjangoPage widgets to create text

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create text on pages.

8/4/14 - Initial creation

Overview
========

Widgets create content, including layouts, for DjangoPages. For example::

    Text(('Paragraph 1 text', 'Paragraph 2 text'), para=True)       # outputs two paragraphs
    Text('Sentence 1')                                              # outputs 'Sentence 1'

Widgets may contain other widgets. A DjangoPage will commonly contain code like this::

    Column(                             # outputs a bootstrap 3 column
            MD('##Some heading'),       # outputs a markdown level 2 heading
            LI()                        # outputs 1 loremipsum paragraph
           )

Widgets ultimately are responsible for returning well formed error free HTML based on the widget's
arguments. Widgets are rather simple code generators and you are free to create/extend widgets.

You can see many examples DWidget examples in djangopages.widgets.

.. note:: Of necessity, widgets MUST be classes!  This allows widgets to accept other widgets
    as arguments a key feature/requirement for declarative page definition.

Base Classes
============
"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '8/24/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

import functools

########################################################################################################################
#
# Widgets
#
########################################################################################################################


class DWidget(object):
    """ DWidget(s) provide content & layout for DPage(s)

    DWidget provides a default render and generate methods.

    .. Note:: **Derived classes must override generate and/or (if needed) render.**

    .. Note:: If you need to force rendering, generaton of object's HTML, of the widget you can
        code **widget(...).render()** or use the convenience method **X(widget(...))**.

    .. Note:: **widget().generate()** will generate HTML **without** evaluating imbedded objects.

    DWidget implements

    * __add__
    * __radd__
    * __mul__
    * __str__
    * __repr__

    as a convenience.

    .. note:: add (+) and mul (*) force immediate rendering of the widget.
    """
    def __init__(self, *args):
        # log.debug('-----in dwidget init')
        self.args = args
        # log.debug('-----done dwidget init')
        return

    def render(self):
        """ Render arguments and invoke the widget's generate method to actually create the output HTML.

        .. note:: When Django processes the DPage's response it will detect that it is **not** a
            response object and invoke this render method.  This will recursively evaluate any embeded
            widgets (the typical case).  This behavior is essential to widget processing.

        .. sourcecode:: python

            render()

        :return: widgets HTML
        :rtype: str

        .. note:: Widgets may, though probably shouldn't, override the default render method.
        """

        # log.debug('##### in dwidget render')
        args = tuple()
        for a in self.args:
            args += (_render(a),)
        self.args = args
        out = self.generate()
        # log.debug('##### done dwidget render')
        return out

    # noinspection PyMethodOverriding
    def generate(self):
        """ generate helper """
        # log.debug('!!!!! in DWidget generate')
        content_name, template, xargs = self.args
        if content_name and isinstance(xargs[content_name], (list, tuple)):
            rtn = ''
            content = xargs.pop(content_name)
            for c in content:
                xargs[content_name] = c
                rtn += self.__class__(**xargs).render()
            return rtn
        rtn = template.format(**xargs)
        return rtn

    def __add__(self, other):
        return self.render() + other

    def __radd__(self, other):
        return other + self.render()

    def __mul__(self, other):
        return self.render() * other

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()


class DWidgetT(DWidget):
    """ Base class for widget template objects.

    Many widgets need helper objects that simply format based on arguments.  DWidgetT supports that need.

    :param template: template for output
    :type template: str or unicode
    :param args: arguments for template
    :type args: dict
    :return: template formated with arguments
    :rtype: unicode
    """
    def __init__(self, template, args):
        super(DWidgetT, self).__init__(template, args)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Return template formatted with arguments
        :return: Template formatted with arguments
        :rtype: unicode
        """
        template, xargs = self.args
        rtn = template.format(**xargs)
        return rtn

########################################################################################################################
#
# Support Routines
#
#######################################################################################################################


def _render(content):
    """ Render the content.  As a general rule this internal method should **not** be used.  However,
    there are exceptions.

    .. sourcecode:: python

        _render(content)

    | Synonym: X

    :param content: content to render
    :type content: varies
    :return: the rendered content
    :rtype: varies
    """
    # log.debug('in _render with <<{}>> type {}'.format(content, type(content)))
    if isinstance(content, basestring):
        return content
    if hasattr(content, 'render'):
        return content.render()
    if isinstance(content, (int, long, float)):
        return content
    if isinstance(content, tuple):
        tpl = tuple()
        for con in content:
            tpl += (_render(con),)
        return tpl
    if isinstance(content, list):
        lst = list()
        for con in content:
            lst.append(_render(con))
        return lst
    return content
X = functools.partial(_render)


# def _renderstr(content):
#     """ Render content, concatenate result basestrings.
#
#     .. sourcecode:: python
#
#         _renderstr(content)
#
#
#     | Synonym: XS(...)
#
#     :param content: content to render
#     :return: rendered content
#     :rtype: basestring
#     """
#     rtn = _render(content)
#     out = ''
#     for r in rtn:
#         if isinstance(r, basestring):
#             out += r
#     return out
# XS = functools.partial(_renderstr)
