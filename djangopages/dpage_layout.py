#!/usr/bin/env python
# coding=utf-8

"""
Layout Widgets
==============

.. module:: dpage_layout
   :synopsis: Provides DjangoPage widgets to create bootstrap 3 layouts

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create bootstrap 3 responsive
grid layouts.

8/4/14 - Initial creation


**Widgets**
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

from djangopages.dpage import DWidget

########################################################################################################################
#
# Layout support classes and methods.
#
########################################################################################################################


class Column(DWidget):
    """ Outputs a bootstrap 3 column

    | Synonym: C(...), useful abbreviation

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict

    additional kwargs

    :param width: column width, default 12
    :type width: int

    | Additional synonyms:
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

    """
    template = '<!-- Start of dpage col -->\n' \
               '<div {classes} {style}>\n' \
               '    {content} '  \
               '</div>\n' \
               '<!-- End of dpage col -->\n'

    def __init__(self, *content, **kwargs):
        """
        Initialize Column object.  Wraps content objects in a column of width width.  Width defaults to 12.
        """
        super(Column, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        width = kwargs.get('width', 12)
        classes = self.add_classes(classes, 'col-md-{}'.format(width))
        out = ''
        for c in content:
            out += template.format(content=c, classes=classes, style=style)
        return out
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
    """
    Wrap content in a row.
    """
    template = '<!-- Start of dpage row -->\n' \
               '<div {classes} {style}>\n' \
               '    {content}\n' \
               '</div>\n' \
               '<!-- End of dpage row -->\n'

    def __init__(self, content, classes='', style='', template=None):
        """
        Wrap content objects in row.
        """
        super(Row, self).__init__(content, classes, style, template)
        return

    def render(self, **kwargs):
        """
        Wrap content in a row
        """
        # extra = 'row'.format()
        # content, classes, style, template = self.render_setup(extra_classes=extra)
        # out = template.format(classes=classes, style=style, content=content)
        # return out
        if isinstance(self.content, list):              # if list, iterate over elements
            out = ''
            for con in self.content:
                r = Row(con, self.classes, self.style, self.template)
                out += r.render()
            return out
        else:
            extra = 'row'.format()
            content, classes, style, template = self.render_setup(extra_classes=extra)
            out = template.format(classes=classes, style=style, content=content)
            return out
R = functools.partial(Row)


class RowColumn(Row, Column):
    """
    Equivalent to Row(Column(content, width, classes, style, template))
    """
    # todo 2: add styles for row

    def __init__(self, content, width=12, classes='', style='', template=None):
        """
        Initialize RowColumn object.
        """
        super(RowColumn, self).__init__(content, classes, style, template)
        self.width = width

    def render(self):
        """
        Render RowColumn
        """
        if isinstance(self.content, list):              # if list, iterate over elements
            out = ''
            for con in self.content:
                c = Column(con, width=self.width,
                           classes=self.classes, style=self.style, template=self.template)
                out += Row(c).render()
            return out
        else:
            content, classes, style, template = self.render_setup()
            c = Column(content, width=self.width,
                       classes=self.classes, style=self.style, template=self.template)
            out = Row(c).render()
            return out

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


# class XRowColumn(XRow, Column):
#     """
#     Equivalent to Row(Column(content))
#     """
#     def __init__(self, *content, **kwargs):
#         """
#         Initialize RowColumn object.
#         """
#         super(RowColumn, self).__init__(*content, **kwargs)
#         self.row_template = kwargs.pop('row_template', Row.template)
#         self.col_template = kwargs.pop('col_template', Column.template)
#         self.kwargs = kwargs
#         self.content = content
#
#     def render(self, **kwargs):
#         """
#         Render RowColumnX
#         :param kwargs:
#         """
#         out = Column(*self.content, template=self.col_template, **self.kwargs).render()
#         out = Row(out, template=self.row_template, **self.kwargs).render()
#         return out
#
