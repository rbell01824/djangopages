#!/usr/bin/env python
# coding=utf-8

"""
Text Widgets
============

.. module:: dpage_texthtml
   :synopsis: Provides DjangoPage widgets to create text

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create text on pages.

8/4/14 - Initial creation


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

########################################################################################################################
#
# Basic Text/HTML, and Markdown
#
########################################################################################################################


# noinspection PyPep8Naming
def Text(content, para=False, classes='', style='', template=None):
    """ Renders text content to the page.

    .. sourcecode:: python

        Text('this is some text content.  More text content. <b>Can contain html</b>')

    | Synonym: T(...), useful abbreviation
    | Synonym: HTML(...), useful to indicate intent

    :param content: content
    :type content: str or unicode
    :param para: if True wrap output in a paragraph
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :param template: override template
    :type template: str or unicode
    """
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    if template:
        return template.format(content=content)
    if para:
        return '<p {classes} {style}>{content}</p>'.format(classes=classes, style=style, content=content)
    if classes or style:
        return '<span {classes} {style}>{content}</span>'.format(classes=classes, style=style, content=content)
    return content
T = functools.partial(Text)
HTML = functools.partial(Text)


# noinspection PyPep8Naming
def Markdown(source, extensions=list()):
    """ Renders markdown content to the page.

    .. sourcecode:: python

        Markdwon('Some *markdown text.')
        Markdown(('##Title', 'Other **markdown** text', '<b>Can contain html</b>')

    Synonyms: MD()

    :param source: source
    :type source: str or unicode or tuple
    :param extensions: defaults to []; see Markdown extensions in python documentation
    :type extensions: list
    """
    if isinstance(source, tuple):
        rtn = ''
        for s in source:
            rtn += Markdown(s, extensions)
        return rtn
    rtn = markdown.markdown(force_unicode(source),
                            extensions,
                            output_format='html5',
                            safe_mode=False,
                            enable_attributes=False)
    return rtn
MD = functools.partial(Markdown)

########################################################################################################################
#
# loremipsum text generation.
#
########################################################################################################################


# noinspection PyPep8Naming
def LI(line_count, para=True, classes='', style='', template=None):
    """ Generate loremipsum paragraphs with line_count sentences.

    .. sourcecode:: python

        LI(3)           # Creates paragraph with 3 sentences.
        LI((3, 5))      # Creates paragraph with 3 sentences and paragraph with 5 sentences

    :param line_count: number of sentences in paragraph
    :type line_count: int or tuple
    :param para: if True wrap output in a paragraph
    :type para: bool
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :param template: override template
    :type template: str or unicode
    """
    if isinstance(line_count, tuple):
        rtn = ''
        for lc in line_count:
            rtn += LI(lc, para, classes, style, template)
        return rtn
    content = ' '.join(loremipsum.get_sentences(line_count))
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    if template:
        return template.format(content=content)
    template = '<p {classes} {style}>' \
               '{content}' \
               '</p>'
    if para:
        return template.format(content=content, classes=classes, style=style)
    return content

########################################################################################################################
#
# Miscelaneous
#
########################################################################################################################


# noinspection PyPep8Naming
def StringDup(string, count=1, classes='', style='', template=None):
    """ Generate amount duplicates of a string.

    .. sourcecode:: python

        StringDup('xxx ', 2)    # generates 'xxx xxx '
        BR(2)                   # generates '<br/><br/>'
        SP(2)                   # generates '&nbsp;&nbsp;'


    :param string: the string to use
    :type string:
    :param count: the number of times to repeat the string
    :type count: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :param template: override template
    :type template: str or unicode

    | Variations:
    | BR, generates one or more HTML line breaks
    | SP, generates one or more non-breaking HTML spaces
    """
    assert isinstance(string, (str, unicode))
    assert len(string) > 0
    assert isinstance(count, int)
    assert count > 0
    content = string * count
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    if template:
        return template.format(content=content)
    if classes or style:
        template = '<span {classes} {style}>{content}</span>'
        return template.format(content=content, classes=classes, style=style)
    return content
SD = functools.partial(StringDup)
BR = functools.partial(StringDup, '<br/>')
SP = functools.partial(StringDup, '&nbsp;')

# todo: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages
