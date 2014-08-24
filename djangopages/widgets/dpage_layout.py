#!/usr/bin/env python
# coding=utf-8

"""
Layout Bootstrap Widgets
************************

.. module:: dpage_layout
   :synopsis: Provides DjangoPage widgets to create bootstrap layouts

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create bootstrap responsive
grid layouts.

8/4/14 - Initial creation

Widgets
=======
"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '8/4/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

import functools
from djangopages.widgets.widgets import DWidget

########################################################################################################################
#
# Layout support classes and methods.
#
########################################################################################################################


class Column(DWidget):
    """ Outputs a bootstrap column

    .. sourcecode:: python

        Column(MD('##Markdown in a bootstrap column'))

    | Shortcuts:
    | C(...), useful abbreviation
    | C1(...), default width 1
    | C2(...), default width 2
    | C3(...), default width 3
    | C4(...), default width 4
    | C5(...), default width 5
    | C6(...), default width 6
    | C7(...), default width 7
    | C8(...), default width 8
    | C9(...), default width 9
    | C10(...), default width 10
    | C11(...), default width 12
    | C121(...), default width 11

    Typically the Column widget is used within a Row widget.

    .. sourcecode:: python

        Row(Column(MD("##Bootstrap row', '##Bootstrap column', 'Other text in row/column')))
    """
    def __init__(self, content, width=12, classes='', style='', template=None):
        super(Column, self).__init__(content, width, classes, style, template)
        return

    # noinspection PyMethodOverriding
    @staticmethod
    def generate(content, width, classes, style, template):
        """ Outputs a bootstrap column

        :param content: content
        :type content: str or unicode or tuple or DWidget
        :param width: bootstrap width, see bootstrap docs
        :type width: int
        :param classes: classes to add to output
        :type classes: str or unicode or DWidget
        :param style: styles to add to output
        :type style: str or unicode or DWidget
        :param template: override template
        :type template: str or unicode or DWidget
        :return: HTML for bootstrap column
        :rtype: unicode
        """
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Column(c, width, classes, style, template)
            return rtn
        classes = 'class="col-md-{width} {classes}" '.format(width=width, classes=classes)
        if style:
            style = 'style="{}" '.format(style)
        if template:
            return template.format(content=content)
        template = '<!-- Start of dpage col -->\n' \
                   '<div {classes} {style}>\n' \
                   '    {content}\n'  \
                   '</div>\n' \
                   '<!-- End of dpage col -->\n'
        rtn = template.format(content=content, classes=classes, style=style)
        return rtn
C = functools.partial(Column)
C1 = functools.partial(Column, width=1)
C2 = functools.partial(Column, width=2)
C3 = functools.partial(Column, width=3)
C4 = functools.partial(Column, width=4)
C5 = functools.partial(Column, width=5)
C6 = functools.partial(Column, width=6)
C7 = functools.partial(Column, width=7)
C8 = functools.partial(Column, width=8)
C9 = functools.partial(Column, width=9)
C10 = functools.partial(Column, width=10)
C11 = functools.partial(Column, width=11)
C12 = functools.partial(Column, width=12)


class Row(DWidget):
    """ Outputs a bootstrap row

    .. sourcecode:: python

        Row(Column(MD(("##Bootstrap row', '##Bootstrap column', 'Other text in row/column'))))

    | Shortcut: R(...), useful abbreviation

    """
    def __init__(self, content, classes='', style='', template=None):
        super(Row, self).__init__(content, classes, style, template)
        return

    # noinspection PyMethodOverriding
    @staticmethod
    def generate(content, classes, style, template):
        """ Outputs a bootstrap row

        :param content: content
        :type content: str or unicode or tuple or DWidget
        :param classes: classes to add to output
        :type classes: str or unicode or DWidget
        :param style: styles to add to output
        :type style: str or unicode or DWidget
        :param template: override template
        :type template: str or unicode or DWidget
        :return: HTML for bootstrap row
        :rtype: unicode
        """
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Row(c, classes, style, template)
            return rtn
        classes = 'class="row {classes}" '.format(classes=classes)
        if style:
            style = 'style="{}" '.format(style)
        if template:
            return template.format(content=content)
        template = '<!-- Start of dpage row -->\n' \
                   '<div {classes} {style}>\n' \
                   '    {content}\n' \
                   '</div>\n' \
                   '<!-- End of dpage row -->\n'
        rtn = template.format(content=content, classes=classes, style=style)
        return rtn
R = functools.partial(Row)


class RowColumn(DWidget):
    """ Equivalent to Row(Column(...))

    .. sourcecode:: python

        RC(MD(("##Bootstrap row', '##Bootstrap column', 'Other text in row/column')))

    .. note:: **All** parameters are passed to Column.  Row uses defaults.

    | Shortcuts:
    | RC(...), default width 12
    | RC1(...), default width 1
    | RC2(...), default width 2
    | RC3(...), default width 3
    | RC4(...), default width 4
    | RC5(...), default width 5
    | RC6(...), default width 6
    | RC7(...), default width 7
    | RC8(...), default width 8
    | RC9(...), default width 9
    | RC10(...), default width 10
    | RC11(...), default width 12
    | RC12(...), default width 11
    """
    def __init__(self, content, width=12, classes='', style='', template=None):
        super(RowColumn, self).__init__(content, width, classes, style, template)
        return

    # noinspection PyMethodOverriding
    @staticmethod
    def generate(content, width, classes, style, template):
        """ Equivalent to Row(Column(...))

        :param content: content
        :type content: str or unicode or tuple
        :param width: bootstrap width, see bootstrap docs
        :type width: int
        :param classes: classes to add to output
        :type classes: str or unicode
        :param style: styles to add to output
        :type style: str or unicode
        :param template: override column template
        :type template: str or unicode

        """
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Row(Column(c, width, classes, style, template))
            return rtn
        rtn = Row(Column(content, width, classes, style, template))
        return rtn
RC = functools.partial(RowColumn, width=12)
RC1 = functools.partial(RowColumn, width=1)
RC2 = functools.partial(RowColumn, width=2)
RC3 = functools.partial(RowColumn, width=3)
RC4 = functools.partial(RowColumn, width=4)
RC5 = functools.partial(RowColumn, width=5)
RC6 = functools.partial(RowColumn, width=6)
RC7 = functools.partial(RowColumn, width=7)
RC8 = functools.partial(RowColumn, width=8)
RC9 = functools.partial(RowColumn, width=9)
RC10 = functools.partial(RowColumn, width=10)
RC11 = functools.partial(RowColumn, width=11)
RC12 = functools.partial(RowColumn, width=12)
