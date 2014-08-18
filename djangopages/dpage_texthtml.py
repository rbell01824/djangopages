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

from djangopages.dpage import DWidget
from django.utils.encoding import force_unicode

########################################################################################################################
#
# Basic Text/HTML, and Markdown
#
########################################################################################################################


class Text(DWidget):
    """ Renders text content to the page.

    .. sourcecode:: python

        Text('this is some text content', 'more text content', '<b>Can contain html</b>')

    | Synonym: T(...), useful abbreviation
    | Synonym: HTML(...), useful to indicate intent

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict

    additional kwargs

    :param para: if True wrap output in a paragraph
    :type para: bool
    """
    template = '{content}'
    template_para = '<p {classes} {style}>{content}</p>'

    def __init__(self, *content, **kwargs):
        super(Text, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        c = ' '.join(content)
        if kwargs.get('para', None):
            return Text.template_para.format(content=c, classes=classes, style=style)
        return template.format(content=c, classes=classes, style=style)
T = functools.partial(Text)
HTML = functools.partial(Text)


class Markdown(DWidget):
    """ Renders markdown content to the page.

    .. sourcecode:: python

        Markdown('##Title', 'Other **markdown** text', '<b>Can contain html</b>')

    Synonyms: MD()

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs plus
    :type kwargs: dict

    additional kwargs

    :param extensions: see Markdown extensions in python documentation
    """
    def __init__(self, *content, **kwargs):
        super(Markdown, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        extensions = kwargs.get('extensions', [])
        c = ' '.join(content)
        out = markdown.markdown(force_unicode(c),
                                extensions,
                                output_format='html5',
                                safe_mode=False,
                                enable_attributes=False)
        return out
MD = functools.partial(Markdown)

########################################################################################################################
#
# loremipsum text generation.
#
########################################################################################################################


class LI(DWidget):
    """ Generate loremipsum paragraphs of sentence specified lengths.

    .. sourcecode:: python

        LI(3, 5)        # Creates two paragraphs. The first has 3 sentences.  The second 5 sentences.
    """
    template = '<p {classes} {style}>' \
               '{content}' \
               '</p>'

    def __init__(self, *content, **kwargs):
        super(LI, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        para = kwargs.get('para', True)
        out = tuple()
        for pl in content:
            if pl > 0:
                content = ' '.join(loremipsum.get_sentences(pl))
            else:
                content = loremipsum.get_paragraph()
            if para:
                out += (template.format(content=content, classes=classes, style=style),)
            else:
                out += (content, )
        if para:
            out = ''.join(out)
        return out

########################################################################################################################
#
# Miscelaneous
#
########################################################################################################################


class AmountStr(DWidget):
    """ Generate amount occuranced of a string.

    .. sourcecode:: python

        AmountStr('xxx ', 2)    # generates 'xxx xxx '
        BR(2)                   # generates '<br/><br/>'
        SP(2)                   # generates '&nbsp;&nbsp;'


    :param content[0]: the string to use
    :type content[0]:
    :param content[1]: the number of times to repeat the string
    :type content[2]: int

    | Variations:
    | BR, generates one or more HTML line breaks
    | SP, generates one or more non-breaking HTML spaces
    """
    template = '<span {classes} {style}>{content}</span>'

    def __init__(self, *content, **kwargs):
        super(AmountStr, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        assert len(content) > 0
        amt = 1
        if len(content) > 1:
            amt = content[1]
        return template.format(content=content[0], classes=classes, style=style) * amt
AS = functools.partial(AmountStr)
BR = functools.partial(AmountStr, '<br/>')
SP = functools.partial(AmountStr, '&nbsp;')

# todo: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages
