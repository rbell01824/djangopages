#!/usr/bin/env python
# coding=utf-8

"""
Text Widgets Overview
*********************

.. module:: texthtml
   :synopsis: Provides DjangoPage widgets to create text

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create text on pages.

8/4/14 - Initial creation

Widgets
=======
"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
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

import markdown
import loremipsum
import functools

from django.utils.encoding import force_unicode
from djangopages.widgets.widgets import DWidget

########################################################################################################################
#
# Basic Text/HTML, and Markdown
#
########################################################################################################################


class Text(DWidget):
    """ Renders text content to the page.

    .. sourcecode:: python

            Text('this is some text content.  More text content. <b>Can contain html</b>')

    | Shortcuts:
    | T(...), useful abbreviation
    | HTML(...), useful to indicate intent


    :param content: content to output
    :type content: str or unicode or tuple or DWidget
    :param para: if True wrap output in a paragraph
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for content
    :rtype: unicode
    """
    def __init__(self, content, para=False, classes='', style=''):
        if para:
            template = '<p class="{classes}" style="{style}">{content}</p>'
        elif classes or style:
            template = '<span class="{classes}" style="{style}">{content}</span>'
        else:
            template = '{content}'
        super(Text, self).__init__('content', template,
                                   {'content': content, 'para': para, 'classes': classes, 'style': style})
        return
T = functools.partial(Text)
HTML = functools.partial(Text)


class Markdown(DWidget):
    """ Renders markdown content to the page.

    .. sourcecode:: python

        Markdown('Some *markdown text.')
        Markdown(('##Title', 'Other **markdown** text', '<b>Can contain html</b>')

    Shortcut: MD()

    :param source: source
    :type source: str or unicode or tuple or DWidget
    :param extensions: defaults to []; see Markdown extensions in python documentation
    :type extensions: list
    :return: HTML for source
    :rtype: unicode
    """
    def __init__(self, source, extensions=list()):
        super(Markdown, self).__init__(source, extensions)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Renders markdown content to the page. """
        source, extensions = self.args
        if isinstance(source, tuple):
            rtn = ''
            for s in source:
                rtn += Markdown(s, extensions).generate()
            return rtn
        rtn = markdown.markdown(force_unicode(source),
                                extensions,
                                output_format='html5',
                                safe_mode=False,
                                enable_attributes=False)
        return rtn
MD = functools.partial(Markdown)


class LI(DWidget):
    """ Generate loremipsum paragraphs with line_count sentences.

    .. sourcecode:: python

        LI(3)           # Creates paragraph with 3 sentences.
        LI((3, 5))      # Creates paragraph with 3 sentences and paragraph with 5 sentences

    :param line_count: number of sentences in paragraph
    :type line_count: int or tuple or list
    :param para: if True wrap output in a paragraph
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for loremipsum
    :rtype: unicode
    """
    def __init__(self, line_count, para=True, classes='', style=''):
        super(LI, self).__init__(line_count, para, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Generate loremipsum paragraphs with line_count sentences. """
        line_count, para, classes, style = self.args
        if isinstance(line_count, (tuple, list)):
            rtn = ''
            for lc in line_count:
                rtn += LI(lc, para, classes, style)
            return rtn
        content = ' '.join(loremipsum.get_sentences(line_count))
        if classes:
            classes = 'class="{}" '.format(classes)
        if style:
            style = 'style="{}" '.format(style)
        template = '<p {classes} {style}>' \
                   '{content}' \
                   '</p>'
        if para:
            return template.format(content=content, classes=classes, style=style)
        return content


class StringDup(DWidget):
    """ Generate amount duplicates of a string.

    .. sourcecode:: python

        StringDup('xxx ', 2)    # generates 'xxx xxx '
        BR(2)                   # generates '<br/><br/>'
        SP(2)                   # generates '&nbsp;&nbsp;'

    | Shortcuts:
    | BR, generates one or more HTML line breaks
    | SP, generates one or more non-breaking HTML spaces

    :param string: the string to use
    :type string: str or unicode or tuple or DWidget
    :param count: the number of times to repeat the string
    :type count: int
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for string
    :rtype: unicode
    """
    def __init__(self, string, count=1, classes='', style=''):
        super(StringDup, self).__init__(string, count, classes, style)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Generate amount duplicates of a string. """
        string, count, classes, style = self.args
        if isinstance(string, tuple):
            rtn = ''
            for lc in string:
                rtn += StringDup(lc, count, classes, style)
            return rtn

        assert isinstance(string, (str, unicode))
        assert len(string) > 0
        assert isinstance(count, int)
        assert count > 0
        content = string * count
        if classes:
            classes = 'class="{}" '.format(classes)
        if style:
            style = 'style="{}" '.format(style)
        if classes or style:
            template = '<span {classes} {style}>{content}</span>'
            return template.format(content=content, classes=classes, style=style)
        return content
SD = functools.partial(StringDup)
BR = functools.partial(StringDup, '<br/>')
SP = functools.partial(StringDup, '&nbsp;')

# todo: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages
