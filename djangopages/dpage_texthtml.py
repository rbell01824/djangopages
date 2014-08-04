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
from loremipsum import get_paragraph

from djangopages.dpage import Content, render_objects
from django.utils.encoding import force_unicode

########################################################################################################################
#
# Basic Text, Markdown, and HTML classes.
#
########################################################################################################################


class Text(Content):
    """
    Renders content to the page.  Text can also be included by passing a str in the
    content.
    """

    def __init__(self, *content, **kwargs):
        """
            Create text object and initialize it.
            :param content: The text.
            :type content: unicode
            :param kwargs: RFU
            :type kwargs: dict
        """
        super(Text, self).__init__()
        self.content = content
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render the Text object
        :param kwargs:
        """
        out = ''
        for obj in self.content:
            if isinstance(obj, basestring):
                out += obj
            else:
                out += render_objects(obj, **kwargs)
        return out


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


class HTML(object):
    """
    Holds HTML text for inclusion in a DPage.  This is a convenience method since DPageMarkdown can be
    used interchangeably.
    """

    def __init__(self, *content, **kwargs):
        """
        Create a DPageHTML object and initialize it.

        :param content: Text to process as html.
        :type content: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.content = content
        self.kwargs = kwargs
        pass

    # noinspection PyUnusedLocal
    def render(self, **kwargs):
        """
        Render HTML text.
        :param kwargs:
        """
        out = ''
        for obj in self.content:
            if isinstance(obj, basestring):
                out += obj
            else:
                out += render_objects(obj)
        return out

########################################################################################################################
#
# Convenience method for loremipsum text generation.
#
########################################################################################################################


# noinspection PyPep8Naming
def GP():
    """
    Provide a bit of syntactic sugar for the more verbose get_paragraph in loremipsum.
    :return:
    """
    return get_paragraph()