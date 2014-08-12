#!/usr/bin/env python
# coding=utf-8

""" Text widgets

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

from djangopages.dpage import DWidget, render_objects
from django.utils.encoding import force_unicode

########################################################################################################################
#
# Basic Text, Markdown, and HTML classes.
#
########################################################################################################################


class Text(DWidget):
    """ Renders content to the page.

    | Text(\*content, \*\*kwargs)
    | T(...)
    | HTML(...)

        :param content: content
        :type content: basestring or tuple or DWidget
        :param kwargs: standard kwargs plus
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

    def render(self):
        """
        Render the Text object
        """
        content, classes, style, template = self.render_setup()
        if self.kwargs.pop('para', None):
            return Text.template_para.format(content=content, classes=classes, style=style)
        return template.format(content=content, classes=classes, style=style)
T = functools.partial(Text)
HTML = functools.partial(Text)


class Markdown(DWidget):
    """ Renders markdown to the page.

    | Markdown(\*content, \*\*kwargs)
    | MD()

        :param content: content
        :type content: basestring or tuple or DWidget
        :param kwargs: standard kwargs plus
        :type kwargs: dict

    additional kwargs

        :param extensions: see Markdown extensions in python documentation
        :type extensions: varies
    """
    def __init__(self, *content, **kwargs):
        super(Markdown, self).__init__(content, kwargs=kwargs)
        pass

    def render(self):
        extensions = self.kwargs.pop('extensions', [])
        content, classes, style, template = self.render_setup()
        out = ''
        for obj in self.content:
            out += markdown.markdown(force_unicode(obj),
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

# fixme: resume work here


class LI(DWidget):
    """ Generate loremipsum paragraphs of sentence length amount.

    LI(amount=1, para=True)

    * amount: If amount is list, generated multiple paragraphs of lengths defined by
      list. Otherwise, invoke LIParagraph(amount, para).render() to output amount paragraphs.
    * para: if True wrap the paragraphs in <p>...</p>

    ex.
        LI([3,5]) creates two paragraphs.  The first has 3 sentences.  The second 5
        sentences.
    """
    def __init__(self, amount=1, para=True):
        super(LI, self).__init__()
        self.amount = amount
        self.para = para
        pass

    def render(self):
        amount = self.amount
        para = self.para
        if isinstance(amount, list):
            out = ''
            for pl in amount:
                out += LISentence(pl, para).render()
            return out
        return LIParagraph(amount, para).render()


class LIParagraph(DWidget):
    """Generate amount loremipsum paragraphs

    LIParagraph(amount=1, para=True)
        | amount: number of paragraphs to return
        | para: if true, wrap each returned paragraph in <p>...</p>
    """
    def __init__(self, amount=1, para=True):
        super(LIParagraph, self).__init__()
        self.amount = amount
        self.para = para
        pass

    def render(self):
        amount = self.amount
        para = self.para
        li = loremipsum.get_paragraphs(amount)
        if not para:
            return li
        out = ''
        for p in li:
            out += '<p>{}</p>'.format(p)
        return out


class LISentence(DWidget):
    """
    Generate a loremipsum sentences
    """
    def __init__(self, amount=1, para=True):
        super(LISentence, self).__init__()
        self.amount = amount
        self.para = para
        pass

    def render(self):
        amount = self.amount
        para = self.para
        li = loremipsum.get_sentences(amount)
        out = ''
        for p in li:
            out += ' ' + p
        if para:
            out = '<p>{}</p>'.format(out)
        return out


# todo 1: turn SP & BR & NBSP methods into classes


class AmountStr(DWidget):
    """
    amount occurences of a string
    """
    def __init__(self, content, amount=1):
        super(AmountStr, self).__init__(content)
        self.amount = amount
        pass

    def render(self):
        return self.content*self.amount
AS = functools.partial(AmountStr)
BR = functools.partial(AmountStr, '<br/>')
SP = functools.partial(AmountStr, '&nbsp;')

# todo 2: add html sysbols see http://www.w3schools.com/html/html_entities.asp and subsequent pages
