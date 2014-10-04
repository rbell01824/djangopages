#!/usr/bin/env python
# coding=utf-8

"""
Text Widgets Overview
*********************

.. module:: widgets.texthtml
   :synopsis: Widgets to create HTML text

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

widgets.texthtml provides a number of widgets to create HTML text on pages.

10/2/14 - Initial creation

Widgets
=======
"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '10/2/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'


import markdown as md
import loremipsum as li
import functools
from collections import Iterable

from django.utils.encoding import force_unicode

########################################################################################################################
#
# Basic Text/HTML, and Markdown
#
########################################################################################################################


def text(content, para=False, classes='', style=''):
    """ Returns text content optionally with classes and style and wrapped in paragraph.  If
    content is iterable, wraps each element and returns concatenated results. Optionally set
    classes and style.

    .. sourcecode:: python

        text('This is some text content.  More text content. <b>Can contain html</b>')
        text(['Text 1', 'Text 2'], para=True)

    | Shortcuts:
    | T(...), useful abbreviation
    | HTML(...), useful to indicate intent

    :param content: Text to output
    :type content: str or unicode or iterable
    :param para: If True wrap output in a paragraph
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for content
    :rtype: unicode
    """
    if not isinstance(content, basestring) and isinstance(content, Iterable):
        rtn = ''
        for c in content:
            rtn += text(c, para, classes, style)
        return rtn
    if para:
        template = '<p class="{classes}" style="{style}">{content}</p>'
    elif classes or style:
        template = '<span class="{classes}" style="{style}">{content}</span>'
    else:
        template = '{content}'
    return template.format(content=content, classes=classes, style=style)
T = functools.partial(text)
HTML = functools.partial(text)


def markdown(markdown_text, markdown_extensions=list()):
    """ Returns HTML equivalent of markdown_text. If markdown_text is iterable applies to each
    element and returns concatenated result.

    .. sourcecode:: python

        markdown('Some *markdown text.')
        markdown(['#Heading', 'Paragraph 1', 'Paragraph 2'])

    Shortcut: MD(...)

    :param markdown_text: Markdown text to translate to HTML
    :type markdown_text: str or unicode or iterable
    :param markdown_extensions: defaults to []; see Markdown extensions in python documentation
    :type markdown_extensions: list
    :return: HTML for markdown_text.
    :rtype: unicode
    """
    if not isinstance(markdown_text, basestring) and isinstance(markdown_text, Iterable):
        rtn = ''
        for mt in markdown_text:
            rtn += markdown(mt, markdown_extensions)
        return rtn
    rtn = md.markdown(force_unicode(markdown_text),
                      markdown_extensions,
                      output_format='html5',
                      safe_mode=False,
                      enable_attributes=False)
    return rtn
MD = functools.partial(markdown)


def loremipsum(line_count, para=True, classes='', style=''):
    """ Return loremipsum paragraphs with line_count sentences.  If line_count is iterable returns multiple
    concatenated paragraphs. Optionally will set classes and style.

    .. sourcecode:: python

        LI(3)           # Creates paragraph with 3 sentences.
        LI((3, 5))      # Creates paragraph with 3 sentences and paragraph with 5 sentences

    :param line_count: number of sentences in paragraph
    :type line_count: int or long or iterable
    :param para: if True wrap output in a paragraph, default True
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode or DWidget
    :param style: styles to add to output
    :type style: str or unicode or DWidget
    :return: HTML for loremipsum
    :rtype: unicode
    """
    if isinstance(line_count, Iterable):
        rtn = ''
        for lc in line_count:
            rtn += loremipsum(lc, para, classes, style)
        return rtn
    content = ' '.join(li.get_sentences(line_count))
    if para:
        template = '<p class="{classes}" style="{style}">{content}</p>'
    elif classes or style:
        template = '<span class="{classes}" style="{style}">{content}</span>'
    else:
        template = '{content}'
    return template.format(content=content, classes=classes, style=style)
LI = functools.partial(loremipsum)


def dup(string, count=1, classes='', style=''):
    """ Generate count duplicates of a string.  If string is iterable return duplicate each string
    and return concatenated result.


    .. sourcecode:: python

        dup('xxx ', 2)    # generates 'xxx xxx '
        BR(2)             # generates '<br/><br/>'
        SP(2)             # generates '&nbsp;&nbsp;'

    | Shortcuts:
    | SD = functools.partial(dup)
    | BR = functools.partial(dup, '<br/>')
    | SP = functools.partial(dup, '&nbsp;')
    | Search = functools.partial(dup, '', classes='glyphicon glyphicon-search')

    :param string: the string to use.  If iterable returns concatenated result
    :type string: str or unicode or tuple
    :param count: the number of times to repeat the string
    :type count: int or long
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for duplicated string
    :rtype: unicode
    """
    if not isinstance(string, basestring) and isinstance(string, Iterable):
        rtn = ''
        for s in string:
            rtn += dup(s, count, classes, style)
        return rtn
    content = string * count
    if classes or style:
        template = '<span class="{classes}" style="{style}">{content}</span>'
        return template.format(content=content, classes=classes, style=style)
    return content
SD = functools.partial(dup)
BR = functools.partial(dup, '<br/>')
SP = functools.partial(dup, '&nbsp;')
Search = functools.partial(dup, '', classes='glyphicon glyphicon-search')

# todo: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages
