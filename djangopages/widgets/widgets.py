#!/usr/bin/env python
# coding=utf-8

"""
Widgets
=======

.. module:: widgets
   :synopsis: Provides DjangoPage widgets to create text

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create text on pages.

8/4/14 - Initial creation

Widgets
*******

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

Widgets
=======
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

    .. Note:: If you need to force rendering of the widget you can code **widget(...).generate()** or use
        the convenience method **X(widget(...))**.

    DWidget implements

    * __add__
    * __radd__
    * __mul__
    * __str__
    * __repr__

    as a convenience.

    .. note:: add (+) and mul (*) force immediate rendering of the widget.
    """
    template = ''

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
        out = self.generate(*args)
        # log.debug('##### done dwidget render')
        # if isinstance(out, DWidget):
        #     out = out.render()
        return out

    def generate(self, template, content, classes, style, kwargs):
        """ Generate the widget's content.

        .. note:: **Widgets MUST override this method.**

        :param template: The widget's template with all objects rendered.
        :type template: varies, typically str or tuple
        :param content: The widget's content with all objects rendered.
        :type content: varies, typically str or tuple
        :param classes: The widget's classes with all objects rendered.
        :type classes: varies, typically str
        :param style: The widget's styles with all objects rendered.
        :type style: varies, typically str
        :param kwargs: The widget's kwargs.  Note, objects are **not rendered**.
        :type kwargs: dict
        :return: The widget's HTML
        :rtype: str
        """
        log.debug('!!!!! in DWidget generate')
        try:
            c = ' '.join(content)
            return template.format(content=c, classes=classes, style=style)
        except TypeError:
            raise TypeError('Non string content for default DWidget generate')

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

    # @staticmethod
    # def add_classes(existing, new):
    #     """ Add classes to existing classes for the widget.  Typically used by the widget's generate method
    #     to add classes that the widget needs to those created by the widget definition.
    #
    #     .. sourcecode:: python
    #
    #         add( existing_classes, 'classes_to_add')
    #
    #     :param existing: Existing class string, ex. class="someclass another_class"
    #     :type existing: str or unicode
    #     :param new: Classes to add, ex. "a_class_to_add"
    #     :type new: str or unicode
    #     :return: new class string, ex. class="someclass another_class a_class_to_add"
    #     :rtype: str
    #     """
    #     if existing == '':
    #         return 'class="{}"'.format(new)
    #     return existing[:-1] + ' ' + new + '"'
    #
    # @staticmethod
    # def add_style(existing, new):
    #     """Add style(s) to existing style(s) for the widget.  Typically used by the widget's generate method
    #     to add styles that the widget needs to those created by the widget definition.
    #
    #     .. sourcecode:: python
    #
    #         add_style( existing_styles, 'styles_to_add')
    #
    #     :param existing: Existing style string, ex. style="style1;style2;"
    #     :type existing: str or unicode
    #     :param new: Styles to add, ex. "style3;style4;"
    #     :type new: str or unicode
    #     :return: new style string, ex. style="style1;style2;style3;style4;"
    #     :rtype: str
    #     """
    #     if existing == '':
    #         return 'style="{}"'.format(new)
    #     return existing[:-1] + ' ' + new + '"'


# class DWidgetSimple(DWidget):
#     """ Base class for simple widgets """
#     def __init__(self, template, tformat, content, classes, style):
#         super(DWidgetSimple, self).__init__(template, tformat, content, classes, style)
#         return
#
#     # noinspection PyMethodOverriding
#     def generate(self, template, tformat, content, classes, style):
#         """ HTML heading
#
#         :param tremplate: widget template
#         :type tremplate: str or unicode
#         :param content: content text
#         :type content: str or unicode
#         :param classes: classes to add to output
#         :type classes: str or unicode
#         :param style: styles to add to output
#         :type style: str or unicode
#         :return: HTML H html
#         :rtype: unicode
#         """
#         if isinstance(content, (list, tuple)):
#             rtn = ''
#             for c in content:
#                 rtn += self.__class__(c, classes, style).render()
#             return rtn
#         if classes:
#             classes = 'class="{}" '.format(classes)
#         if style:
#             style = 'style="{}" '.format(style)
#         rtn = template.format(**tformat)
#         return rtn

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
