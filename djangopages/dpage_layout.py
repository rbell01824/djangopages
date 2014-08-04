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
        Render objects in column of width width.  Render each content object in a column of width width.
        """
        out = ''
        for con in self.content:
            out += self.template.format(width=self.width, content=render_objects(con))
        return out


class ColumnX(Column):
    """
    Render objects in a single column of width width.  Render all the objects then wrap in a column of width width.
    """
    def render(self, **kwargs):
        """
        Render objects in a single column of width width.
        :param kwargs:
        """
        out = self.template.format(width=self.width, content=render_objects(self.content))
        return out


def column(*content, **kwargs):
    """
    Convenience function for Column.
    """
    return Column(*content, **kwargs)
C = functools.partial(column)
C1 = functools.partial(column, width=1)
C2 = functools.partial(column, width=2)
C3 = functools.partial(column, width=3)
C4 = functools.partial(column, width=4)
C5 = functools.partial(column, width=5)
C6 = functools.partial(column, width=6)
C7 = functools.partial(column, width=7)
C8 = functools.partial(column, width=8)
C9 = functools.partial(column, width=9)
c10 = functools.partial(column, width=10)
c11 = functools.partial(column, width=11)
C12 = functools.partial(column, width=12)


# noinspection PyPep8Naming
def columnX(*content, **kwargs):
    """
    Convenience function for ColumnX.
    """
    return ColumnX(*content, **kwargs)
CX = functools.partial(columnX)
C1X = functools.partial(columnX, width=1)
C2X = functools.partial(columnX, width=2)
C3X = functools.partial(columnX, width=3)
C4X = functools.partial(columnX, width=4)
C5X = functools.partial(columnX, width=5)
C6X = functools.partial(columnX, width=6)
C7X = functools.partial(columnX, width=7)
C8X = functools.partial(columnX, width=8)
C9X = functools.partial(columnX, width=9)
c10X = functools.partial(columnX, width=10)
c11X = functools.partial(columnX, width=11)
C12X = functools.partial(columnX, width=12)


class Row(Content):
    """
    Wrap each content object in a row in a row.
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
        Render each object in row
        """
        out = ''
        for con in self.content:
            out += self.template.format(content=render_objects(con))
        return out


class RowX(Row):
    """
    Wrap all concatenation of all content in a row.
    """
    def render(self, **kwargs):
        """
        Render all objects in a row
        """
        out = self.template.format(content=render_objects(self.content))
        return out


def row(*content, **kwargs):
    """
    Convenience function for Row.
    """
    return Row(*content, **kwargs)
R = functools.partial(row)


# noinspection PyPep8Naming
def rowX(*content, **kwargs):
    """
    Convenience function for RowX.
    """
    return RowX(*content, **kwargs)
RX = functools.partial(rowX)


class RowColumn(Row, Column):
    """
    Create a rowcolumn class.  Wrap content in a row wrapping a column.

    Equivalent to: Row(Column(content).render()).render()
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
        Render RowColumn
        :param kwargs:
        """
        out = Column(*self.content, template=self.col_template, **self.kwargs).render()
        out = Row(out, template=self.row_template, **self.kwargs).render()
        return out


class RowColumnX(Row, ColumnX):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.  Wrap content in a row wrapping a column.

        Equivalent to: Row(ColumnX(content).render()).render()
        """
        super(RowColumnX, self).__init__(*content, **kwargs)
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content

    def render(self, **kwargs):
        """
        Render RowColumnX
        :param kwargs:
        """
        out = ColumnX(*self.content, template=self.col_template, **self.kwargs).render()
        out = Row(out, template=self.row_template, **self.kwargs).render()
        return out


class RowXColumn(RowX, Column):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.

        Equivalent to: RowX(Column(content).render()).render()
        """
        super(RowXColumn, self).__init__(*content, **kwargs)
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
        out = RowX(out, template=self.row_template, **self.kwargs).render()
        return out


class RowXColumnX(RowX, ColumnX):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.

        Equivalent to: RowX(ColumnX(content).render()).render()
        """
        super(RowXColumnX, self).__init__(*content, **kwargs)
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content

    def render(self, **kwargs):
        """
        Render RowColumnX
        :param kwargs:
        """
        out = ColumnX(*self.content, template=self.col_template, **self.kwargs).render()
        out = RowX(out, template=self.row_template, **self.kwargs).render()
        return out


def rowcolumn(*content, **kwargs):
    """
    Convenience function for RowColumn.
    """
    return RowColumn(*content, **kwargs)
RC = functools.partial(rowcolumn, width=12)
RC1 = functools.partial(rowcolumn, width=1)
RC2 = functools.partial(rowcolumn, width=2)
RC3 = functools.partial(rowcolumn, width=3)
RC4 = functools.partial(rowcolumn, width=4)
RC5 = functools.partial(rowcolumn, width=5)
RC6 = functools.partial(rowcolumn, width=6)
RC7 = functools.partial(rowcolumn, width=7)
RC8 = functools.partial(rowcolumn, width=8)
RC9 = functools.partial(rowcolumn, width=9)
RC10 = functools.partial(rowcolumn, width=10)
RC11 = functools.partial(rowcolumn, width=11)
RC12 = functools.partial(rowcolumn, width=12)


# noinspection PyPep8Naming
def rowXcolumn(*content, **kwargs):
    """
    Convenience function for RowXColumn.
    """
    return RowXColumn(*content, **kwargs)
RXC = functools.partial(rowXcolumn, width=12)
RXC1 = functools.partial(rowXcolumn, width=1)
RXC2 = functools.partial(rowXcolumn, width=2)
RXC3 = functools.partial(rowXcolumn, width=3)
RXC4 = functools.partial(rowXcolumn, width=4)
RXC5 = functools.partial(rowXcolumn, width=5)
RXC6 = functools.partial(rowXcolumn, width=6)
RXC7 = functools.partial(rowXcolumn, width=7)
RXC8 = functools.partial(rowXcolumn, width=8)
RXC9 = functools.partial(rowXcolumn, width=9)
RXC10 = functools.partial(rowXcolumn, width=10)
RXC11 = functools.partial(rowXcolumn, width=11)
RXC12 = functools.partial(rowXcolumn, width=12)


# noinspection PyPep8Naming
def rowcolumnX(*content, **kwargs):
    """
    Convenience function for RowColumnX
    """
    return RowColumnX(*content, **kwargs)
RCX = functools.partial(rowcolumnX, width=12)
RC1X = functools.partial(rowcolumnX, width=1)
RC2X = functools.partial(rowcolumnX, width=2)
RC3X = functools.partial(rowcolumnX, width=3)
RC4X = functools.partial(rowcolumnX, width=4)
RC5X = functools.partial(rowcolumnX, width=5)
RC6X = functools.partial(rowcolumnX, width=6)
RC7X = functools.partial(rowcolumnX, width=7)
RC8X = functools.partial(rowcolumnX, width=8)
RC9X = functools.partial(rowcolumnX, width=9)
RC10X = functools.partial(rowcolumnX, width=10)
RC11X = functools.partial(rowcolumnX, width=11)
RC12X = functools.partial(rowcolumnX, width=12)


# noinspection PyPep8Naming
def rowXcolumnX(*content, **kwargs):
    """
    Convenience function for RowXColumnX
    """
    return RowXColumnX(*content, **kwargs)
RXCX = functools.partial(rowXcolumnX, width=12)
RXC1X = functools.partial(rowXcolumnX, width=1)
RXC2X = functools.partial(rowXcolumnX, width=2)
RXC3X = functools.partial(rowXcolumnX, width=3)
RXC4X = functools.partial(rowXcolumnX, width=4)
RXC5X = functools.partial(rowXcolumnX, width=5)
RXC6X = functools.partial(rowXcolumnX, width=6)
RXC7X = functools.partial(rowXcolumnX, width=7)
RXC8X = functools.partial(rowXcolumnX, width=8)
RXC9X = functools.partial(rowXcolumnX, width=9)
RXC10X = functools.partial(rowXcolumnX, width=10)
RXC11X = functools.partial(rowXcolumnX, width=11)
RXC12X = functools.partial(rowXcolumnX, width=12)
