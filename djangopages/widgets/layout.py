#!/usr/bin/env python
# coding=utf-8

"""
Layout Widgets Overview
***********************

.. module:: layout
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


class WList(DWidget):
    """ Renders list of widgets.

    .. sourcecode:: python

            WList(MD(...), T(...), ...)

    | Shortcuts:
    | WL = functools.partial(WList)

    :param content: content to output
    :type content: list of DWidget(s)
    """
    def __init__(self, *content):
        super(WList, self).__init__(*content)
        return

    def generate(self):
        content = self.args
        rtn = '\n'.join(content)
        return rtn
WL = functools.partial(WList)


class Layout(DWidget):
    """ Renders list of widgets.

    .. sourcecode:: python

            Layout(row1, row2, ...)

    | Shortcuts:

    :param content: content to output
    :type content: list of DWidget(s)
    """
    def __init__(self, *content):
        super(Layout, self).__init__(*content)
        return

    def generate(self):
        content = self.args
        rtn = ''
        for r in content:
            if isinstance(r, tuple):
                rtn += Row('\n'.join(r))
            else:
                rtn += Row(r)
        return rtn
L = functools.partial(WList)


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

    :param content: content
    :type content: str or unicode or tuple or DWidget
    :param width: bootstrap width, see bootstrap docs
    :type width: int
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for bootstrap column
    :rtype: unicode

    Typically the Column widget is used within a Row widget.

    .. sourcecode:: python

        Row(Column(MD("##Bootstrap row', '##Bootstrap column', 'Other text in row/column')))
    """
    # todo 2: convert to use default generate
    def __init__(self, content, width=12, classes='', style=''):
        super(Column, self).__init__(content, width, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Outputs a bootstrap column """
        content, width, classes, style = self.args
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Column(c, width, classes, style)
            return rtn
        classes = 'class="col-md-{width} {classes}" '.format(width=width, classes=classes)
        if style:
            style = 'style="{}" '.format(style)
        template = '\n<!-- DWidget col -->\n' \
                   '<div {classes} {style}>\n' \
                   '    {content}\n'  \
                   '</div>\n' \
                   '<!-- / DWidget col -->\n'
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

    :param content: content
    :type content: str or unicode or tuple or DWidget
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for bootstrap row
    :rtype: unicode
    """
    # todo 2: convert to use default generate
    def __init__(self, content, classes='', style=''):
        super(Row, self).__init__(content, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Outputs a bootstrap row """
        content, classes, style = self.args
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Row(c, classes, style)
            return rtn
        classes = 'class="row {classes}" '.format(classes=classes)
        if style:
            style = 'style="{}" '.format(style)
        template = '\n<!-- DWidget row -->\n' \
                   '<div {classes} {style}>\n' \
                   '    {content}\n' \
                   '</div>\n' \
                   '<!-- / DWidget row -->\n'
        rtn = template.format(content=content, classes=classes, style=style)
        return rtn
R = functools.partial(Row)


class RowColumn(DWidget):
    """ Equivalent to Row(Column(...))

    .. sourcecode:: python

        RC(MD(("##Bootstrap row', '##Bootstrap column', 'Other text in row/column')))

    .. note:: RowColumn generates **one** row with multiple columns.

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


    :param content: content
    :type content: str or unicode or tuple
    :param width: bootstrap width, see bootstrap docs
    :type width: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for Row(Column(...))
    :rtype: unicode
    """
    def __init__(self, content, width=12, classes='', style=''):
        super(RowColumn, self).__init__(content, width, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Equivalent to Row(Column(...)) """
        template = '\n<!-- DWidget RowColumn -->\n' \
                   '{rc}\n' \
                   '<!-- / DWidget RowColumn -->\n'
        content, width, classes, style = self.args
        if isinstance(content, tuple):
            cols = ''
            for c in content:
                cols += Column(c, width, classes, style).render()
            rtn = Row(cols).render()
        else:
            rtn = Row(Column(content, width, classes, style)).render()
        rtn = template.format(rc=rtn)
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


class RowRowColumn(DWidget):
    """ Equivalent to Row(Column(...)).  Unlike RowColumn, generates a Row for **each** Column.

    .. sourcecode:: python

        RC(MD(("##Bootstrap row', '##Bootstrap column', 'Other text in row/column')))
        
    .. note:: Generates a Row for **each** column.

    .. note:: **All** parameters are passed to Column.  Row uses defaults.

    | Shortcuts:
    | RRC(...), default width 12
    | RRC1(...), default width 1
    | RRC2(...), default width 2
    | RRC3(...), default width 3
    | RRC4(...), default width 4
    | RRC5(...), default width 5
    | RRC6(...), default width 6
    | RRC7(...), default width 7
    | RRC8(...), default width 8
    | RRC9(...), default width 9
    | RRC10(...), default width 10
    | RRC11(...), default width 12
    | RRC12(...), default width 11


    :param content: content
    :type content: str or unicode or tuple
    :param width: bootstrap width, see bootstrap docs
    :type width: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for Row(Column(...))
    :rtype: unicode
    """
    def __init__(self, content, width=12, classes='', style=''):
        super(RowRowColumn, self).__init__(content, width, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Equivalent to Row(Column(...)) """
        template = '\n<!-- DWidget RowRowColumn -->\n' \
                   '{rrc}\n' \
                   '<!-- / DWidget RowRowColumn -->\n'
        content, width, classes, style = self.args
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                col = Column(c, width, classes, style).render()
                rtn += Row(col).render()
        else:
            rtn = Row(Column(content, width, classes, style)).render()
        rtn = template.format(rrc=rtn)
        return rtn
RRC = functools.partial(RowRowColumn, width=12)
RRC1 = functools.partial(RowRowColumn, width=1)
RRC2 = functools.partial(RowRowColumn, width=2)
RRC3 = functools.partial(RowRowColumn, width=3)
RRC4 = functools.partial(RowRowColumn, width=4)
RRC5 = functools.partial(RowRowColumn, width=5)
RRC6 = functools.partial(RowRowColumn, width=6)
RRC7 = functools.partial(RowRowColumn, width=7)
RRC8 = functools.partial(RowRowColumn, width=8)
RRC9 = functools.partial(RowRowColumn, width=9)
RRC10 = functools.partial(RowRowColumn, width=10)
RRC11 = functools.partial(RowRowColumn, width=11)
RRC12 = functools.partial(RowRowColumn, width=12)
