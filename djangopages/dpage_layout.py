#!/usr/bin/env python
# coding=utf-8

"""
Layout Bootstrap 3 Widgets
==========================

.. module:: dpage_layout
   :synopsis: Provides DjangoPage widgets to create bootstrap 3 layouts

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create bootstrap 3 responsive
grid layouts.

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

########################################################################################################################
#
# Layout support classes and methods.
#
########################################################################################################################


# noinspection PyPep8Naming
def Column(content, width=12, classes='', style='', template=None):
    """ Outputs a bootstrap 3 column

    .. sourcecode:: python

        Column(MD('##Markdown in a bootstrap 3 column'))

    :param content: content
    :type content: str or unicode or tuple
    :param width: bootstrap 3 width, see bootstrap 3 docs
    :type width: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :param template: override template
    :type template: str or unicode

    | Synonyms:
    | Synonym: C(...), useful abbreviation
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

        Row(Column(MD("##Bootstrap 3 row', '##Bootstrap 3 column', 'Other text in row/column')))
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

#
# class Row(DWidget):
#     """ Outputs a bootstrap 3 row
#
#     .. sourcecode:: python
#
#         Row(Column(MD("##Bootstrap 3 row', '##Bootstrap 3 column', 'Other text in row/column')))
#
#     | Synonym: R(...), useful abbreviation
#
#     :param content: content
#     :type content: basestring or tuple or DWidget
#     :param kwargs: standard kwargs
#     :type kwargs: dict
#     """
#     template = '<!-- Start of dpage row -->\n' \
#                '<div {classes} {style}>\n' \
#                '    {content}\n' \
#                '</div>\n' \
#                '<!-- End of dpage row -->\n'
#
#     def __init__(self, *content, **kwargs):
#         super(Row, self).__init__(content, kwargs)
#         return
#
#     def generate(self, template, content, classes, style, kwargs):
#         assert isinstance(content, tuple)
#         classes = self.add_classes(classes, 'row')
#         out = ''
#         for c in content:
#             out += template.format(content=c, classes=classes, style=style)
#         return out
# R = functools.partial(Row)
#
#
# class RowColumn(DWidget):
#     """ Equivalent to Row(Column(...))
#
#     .. sourcecode:: python
#
#         RC(MD("##Bootstrap 3 row', '##Bootstrap 3 column', 'Other text in row/column'))
#
#     | Synonym: RC(...), useful abbreviation
#
#     :param content: content
#     :type content: basestring or tuple or DWidget
#     :param kwargs: standard kwargs
#     :type kwargs: dict
#
#     additional kwargs
#
#     :param width: column width, default 12
#     :type width: int
#
#     | Additional synonyms:
#     | RC(...), default width 12
#     | RC1(...), default width 1
#     | RC2(...), default width 2
#     | RC3(...), default width 3
#     | RC4(...), default width 4
#     | RC5(...), default width 5
#     | RC6(...), default width 6
#     | RC7(...), default width 7
#     | RC8(...), default width 8
#     | RC9(...), default width 9
#     | RC10(...), default width 10
#     | RC11(...), default width 12
#     | RC12(...), default width 11
#     """
#     template = Column.template
#     row_template = Row.template
#
#     def __init__(self, *content, **kwargs):
#         super(RowColumn, self).__init__(content, kwargs)
#         return
#
#     def generate(self, template, content, classes, style, kwargs):
#         assert isinstance(content, tuple)
#         width = kwargs.get('width', 12)
#         col_classes = self.add_classes(classes, 'col-md-{}'.format(width))
#         out = ''
#         for c in content:
#             out += template.format(content=c, classes=col_classes, style=style)
#         out = self.row_template.format(classes='class="row"', style='', content=out)
#         return out
# RC = functools.partial(RowColumn, width=12)
# RC1 = functools.partial(RowColumn, width=1)
# RC2 = functools.partial(RowColumn, width=2)
# RC3 = functools.partial(RowColumn, width=3)
# RC4 = functools.partial(RowColumn, width=4)
# RC5 = functools.partial(RowColumn, width=5)
# RC6 = functools.partial(RowColumn, width=6)
# RC7 = functools.partial(RowColumn, width=7)
# RC8 = functools.partial(RowColumn, width=8)
# RC9 = functools.partial(RowColumn, width=9)
# RC10 = functools.partial(RowColumn, width=10)
# RC11 = functools.partial(RowColumn, width=11)
# RC12 = functools.partial(RowColumn, width=12)
#
#
# class RowColumnMap(DWidget):
#     """ Equivalent to map(Row(Column(...)), ... )
#
#     .. sourcecode:: python
#
#         content = RC6M((t, t),
#                        (t, t), style='border:1px solid;')
#
#     Generates two rows with C6 content.
#
#
#     :param content: content
#     :type content: basestring or tuple or DWidget
#     :param kwargs: standard kwargs
#     :type kwargs: dict
#
#     additional kwargs
#
#     :param width: column width, default 12
#     :type width: int
#
#     | Synonyms:
#     | RCM(...), default width 12
#     | RC1M(...), default width 1
#     | RC2M(...), default width 2
#     | RC3M(...), default width 3
#     | RC4M(...), default width 4
#     | RC5M(...), default width 5
#     | RC6M(...), default width 6
#     | RC7M(...), default width 7
#     | RC8M(...), default width 8
#     | RC9M(...), default width 9
#     | RC10M(...), default width 10
#     | RC11M(...), default width 12
#     | RC12M(...), default width 11
#     """
#     template = Column.template
#     row_template = Row.template
#
#     def __init__(self, *content, **kwargs):
#         super(RowColumnMap, self).__init__(content, kwargs)
#         return
#
#     def generate(self, template, content, classes, style, kwargs):
#         assert isinstance(content, tuple)
#         width = kwargs.get('width', 12)
#         col_classes = self.add_classes(classes, 'col-md-{}'.format(width))
#         rows = tuple()
#         for r in content:
#             assert isinstance(r, tuple)
#             rout = ''
#             for c in r:
#                 rout += template.format(content=c, classes=col_classes, style=style)
#             rout = self.row_template.format(classes='class="row"', style='', content=rout)
#             rows += (rout,)
#         out = ''.join(rows)
#         return out
# RCM = functools.partial(RowColumnMap, width=12)
# RC1M = functools.partial(RowColumnMap, width=1)
# RC2M = functools.partial(RowColumnMap, width=2)
# RC3M = functools.partial(RowColumnMap, width=3)
# RC4M = functools.partial(RowColumnMap, width=4)
# RC5M = functools.partial(RowColumnMap, width=5)
# RC6M = functools.partial(RowColumnMap, width=6)
# RC7M = functools.partial(RowColumnMap, width=7)
# RC8M = functools.partial(RowColumnMap, width=8)
# RC9M = functools.partial(RowColumnMap, width=9)
# RC10M = functools.partial(RowColumnMap, width=10)
# RC11M = functools.partial(RowColumnMap, width=11)
# RC12M = functools.partial(RowColumnMap, width=12)
