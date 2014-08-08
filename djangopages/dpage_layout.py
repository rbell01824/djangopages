#!/usr/bin/env python
# coding=utf-8

""" django pages layout support routines

8/4/14 - Initial creation

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

from djangopages.dpage import Content, render_objects

########################################################################################################################
#
# Layout support classes and methods.  Really just syntactic sugar to make layout much easier.
#
########################################################################################################################


class Column(Content):
    """
    Wrap *content objects in column of width width=nn.  Content is rendered and wrapped in a single
    bootstrap 3 column of width width.
    """
    template = '<!-- Start of dpage col -->\n' \
               '<div class="col-md-{width}">\n' \
               '    {content} '  \
               '</div>\n' \
               '<!-- End of dpage col -->\n'
    width = 12

    def __init__(self, *content, **kwargs):
        """
            Initialize Column object.  Wraps content objects in a column of width width.  Width defaults to 12.

            ex. Column('aaa', 'bbb', width=6)

                Creates two columns of width 6.  The first contains 'aaa'.  The second contains 'bbb'.

            Generally it is much more convenient to use the Cn functions to create columns.

            ex. C6( 'aaa', 'bbb' )

            The following Cn functions are available: C, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12.

            kwargs:
                width=12                set the column width
                template='some str'     override the default template

            :param content: Content to wrap in a column of width width
            :type content: object or collections.iterable
            :param kwargs: Use to override default width of 12.  Other uses RFU.
            :type kwargs: dict
            :return: Column object
            :rtype: Column object
            """
        super(Column, self).__init__()
        self.content = content
        self.width = kwargs.pop('width', Column.width)
        self.template = kwargs.pop('template', Column.template)
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Wrap content in a column.
        """
        out = self.template.format(width=self.width, content=render_objects(self.content))
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


class XColumn(Column):
    """
    Wrap each content object in a column.
    """
    def render(self, **kwargs):
        """
        Wrap each content object in a column.
        """
        out = ''
        for con in self.content:
            out += self.template.format(width=self.width, content=render_objects(con))
        return out
XC = functools.partial(XColumn)
XC1 = functools.partial(XColumn, width=1)
XC2 = functools.partial(XColumn, width=2)
XC3 = functools.partial(XColumn, width=3)
XC4 = functools.partial(XColumn, width=4)
XC5 = functools.partial(XColumn, width=5)
XC6 = functools.partial(XColumn, width=6)
XC7 = functools.partial(XColumn, width=7)
XC8 = functools.partial(XColumn, width=8)
XC9 = functools.partial(XColumn, width=9)
XC10 = functools.partial(XColumn, width=10)
XC11 = functools.partial(XColumn, width=11)
XC12 = functools.partial(XColumn, width=12)


class Row(Content):
    """
    Wrap content in a row.
    """
    template = '<!-- Start of dpage row -->\n' \
               '<div class="row">\n' \
               '    {content}\n' \
               '</div>\n' \
               '<!-- End of dpage row -->\n'

    def __init__(self, *content, **kwargs):
        """
            Wrap *content objects in row.

            :param content: Content to wrap in a row
            :type content: object or collections.iterable
            :param kwargs: RFU
            :type kwargs: dict
            :return: Row object
            :rtype: Row object
            """
        super(Row, self).__init__()
        self.content = content
        self.template = kwargs.pop('template', Row.template)
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Wrap content in a row
        """
        out = self.template.format(content=render_objects(self.content))
        return out
R = functools.partial(Row)


class XRow(Row):
    """
    Wrap each content object in a row.
    """
    def render(self, **kwargs):
        """
        Render each content object in row
        """
        out = ''
        for con in self.content:
            out += self.template.format(content=render_objects(con))
        return out
XR = functools.partial(XRow)


class RowColumn(Row, Column):
    """
    Equivalent to Row(Column(content))
    """
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumn object.
        """
        super(RowColumn, self).__init__(*content, **kwargs)
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content

    def render(self, **kwargs):
        """
        Render RowColumnX
        :param kwargs:
        """
        out = Column(*self.content, template=self.col_template, **self.kwargs).render()
        out = Row(out, template=self.row_template, **self.kwargs).render()
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
