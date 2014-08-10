#!/usr/bin/env python
# coding=utf-8

""" Some description here

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

from djangopages.dpage import Content, render_objects
from django.utils.encoding import force_unicode

########################################################################################################################
#
# Basic Text, Markdown, and HTML classes.
#
########################################################################################################################


class Text(object):
    """
    Renders content to the page.

    If <content> is a basestring, outputs <content>.  Otherwise outputs <content>.render().
    Accepts (<content>, <content>, ... ).
    """

    def __init__(self, *content):
        """
        Create text object and initialize it.
        :param content: The content text or object list.
        """
        super(Text, self).__init__()
        self.content = content
        return

    def render(self):
        """
        Render the Text object
        """
        out = ''
        for obj in self.content:
            if isinstance(obj, basestring):
                out += obj
            else:
                out += render_objects(obj)
        return out
T = functools.partial(Text)
HTML = functools.partial(Text)


class Markdown(object):
    """
    Holds markdown text for inclusion in a DPage.  Markdown can also hold Text and HTML.
    """

    def __init__(self, *content, **kwargs):
        """
        Create a markdown object and initialize it.

        :param content: Text to process as markdown.
        :type content: unicode
        :param kwargs:
            extensions          Markdown extensions
            RFU
        :type kwargs: dict
        """
        self.content = content
        self.extensions = kwargs.pop('extensions', None)
        self.kwargs = kwargs
        pass

    def render(self, **kwargs):
        """
        Render markdown text.
        :param kwargs:
        """
        out = ''
        for obj in self.content:
            if isinstance(obj, basestring):
                out += markdown.markdown(force_unicode(obj),
                                         self.extensions if self.extensions else '',
                                         output_format='html5',
                                         safe_mode=False,
                                         enable_attributes=False)
            else:
                out += render_objects(obj, **kwargs)
        return out
MD = functools.partial(Markdown)


########################################################################################################################
#
# Convenience methods for loremipsum text generation.
#
########################################################################################################################
# todo 1: turn LI methods into classes


# noinspection PyPep8Naming
def LI(amount=1, para=True):
    """
    Generate loremipsum paragraphs of sentence length sentences.
    :param amount: Number of paragraphs to generate, or a list of sentence lengths for each paragraph.
    :type amount: int or list
    :param para: If true wrap each paragraph in html p tags
    :type para: bool
    """
    if isinstance(amount, (int, long, float)):
        return LI_Paragraph(amount, para)
    out = ''
    for pl in amount:
        out += LI_Sentence(pl, para)
    return out


# noinspection PyPep8Naming
def LI_Paragraph(amount=1, para=True):
    """
    Provide a bit of syntactic sugar for the more verbose get_paragraphs in loremipsum.
    :param amount: Number of paragraphs to generate
    :type amount: int
    :param para: If true wrap each paragraph in html p tags
    :type para: bool
    """
    li = loremipsum.get_paragraphs(amount)
    if not para:
        return li
    out = []
    for p in li:
        out.append('<p>{}</p>'.format(p))
    return out


# noinspection PyPep8Naming
def LI_Sentence(amount=1, para=True):
    """
    Provide a bit of syntactic sugar for the more verbose get_sentences in loremipsum.
    :param amount: Number of sentences to generate
    :type amount: int
    """
    li = loremipsum.get_sentences(amount)
    out = ''
    for p in li:
        out += ' ' + p
    if not para:
        return out
    out = '<p>{}</p>'.format(out)
    return out

# todo 1: turn SP & BR & NBSP methods into classes


# noinspection PyPep8Naming
def BR(amount=1):
    """
    amount <br />
    :param amount:
    :return:
    """
    return '<br />'*amount


# noinspection PyPep8Naming
def SP(amount=1):
    """
    Amount spaces.
    :param amount:
    :return:
    """
    return '&nbsp;'*amount


# todo 2: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages

