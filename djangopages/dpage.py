#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/9/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/9/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

import markdown
import collections
import functools
from copy import copy

from django.conf import settings
from django.utils.encoding import force_unicode
from django.template import Template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf

from djangopages.libs import dict_nested_set

########################################################################################################################
#
# Support Routines
#
########################################################################################################################


def unique_name(base_name='x'):
    """
    Returns a unique name of the form 'base_name'_counter.  Used internally to create id and other names.

    ex. unique_name('xxx')

    :param base_name:
    :return: Unique name
    :rtype: unicode
    """
    if not hasattr(unique_name, "counter"):
        unique_name.counter = 0  # it doesn't exist yet, so initialize it
    unique_name.counter += 1
    return '{}_{}'.format(base_name, unique_name.counter)


def render_objects(*content, **kwargs):
    """
    Render the content.

    ex. render_objects('something', 'another thing', ('a list thing', 'second'))

    render_objects is also available as X(...) as a convenience method.

    :param content: content to render
    :type: list or object
    :param kwargs: RFU
    :type kwargs: dict
    :return: Rendered output of objects
    :rtype: unicode
    """
    out = ''
    for con in content:
        if isinstance(con, basestring):                     # strings are just themselves
            out += con
        elif hasattr(con, 'render'):                        # objects with render methods know how to render themselves
            out += con.render(**kwargs)
        elif isinstance(con, collections.Iterable):         # collections are walked
            for con1 in con:
                out += render_objects(con1, **kwargs)       # recurse to render this collection item
        else:                                               # this should never happen
            raise ValueError('Unknown content type in render_objects {}'.format(con))
    return out
X = functools.partial(render_objects)                       # convenience method for render objects

########################################################################################################################
#
# Register classes
#
########################################################################################################################


class _DPageRegister(type):
    """
    Internal metaclass to register DPage child objects.  Do not mess with this!
    """
    def __init__(cls, name, base, attrs):
        if not hasattr(cls, 'pages_list'):
            # Executed when processing DPageRegister class itself.
            # Use class variables so there is only one copy
            cls.pages_list = []          # List of subclasses to allow listing
            cls.pages_dict = {}          # Dictionary of subclasses to allow quick name lookup
        else:
            cls.pages_list.append({'cls': cls, 'name': name})       # Put in list
            cls.pages_dict[name] = cls                              # Put in dict

########################################################################################################################
#
# DPage class
#
########################################################################################################################


class DPage(object):
    """
    DPage, aka Django Page class.  DPage child classes derive from DPage.

    Basic example:

        class Example(DPage):
            title = 'DjangoPages_Example'               # You must define a class title.  It must be unique.
            description = 'Demonstrate links'           # You should provide a class description.  It may be any
                                                        # length.
            tags = []                                   # RFU

            def page(self):                             # You must override the page class.
                self.content = ...                      # page must define the content
                return self                             # You must return self

    See the source for additional child class examples.

    """
    __metaclass__ = _DPageRegister              # use DPageRegister to register child classes

    def __init__(self, request=None, context=None, template=None, **kwargs):
        """
        Initialize the DPage.  As a general rule, you need not perform initialization in the DPage child class.
        However, if you do it is possible to provide additional context content and customize the template.

        :param request: The request object
        :type request: WSGIRequest
        :param context: Additional context values for the page
        :type context: dict
        :param template: template name to use for this DPage object.  If None, DPageDefaultTemplate specified in
                         settings is used.
        :type template: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.request = request
        self.context = context
        self.template = template if template else settings.DPAGE_DEFAULT_TEMPLATE
        self.content = []
        self.kwargs = kwargs
        pass

    def page(self):
        """
        Define the page.  The subclass must define this method.

        The page method defines the page.  Example:

                def page(self):
                    xr1 = Text('This text comes from dpage.Text')
                    xr2 = Markdown('**Bold Markdown Text**')
                    xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                    self.content(RC12(xr1, xr2, xr3))
                    return self
        """
        raise NotImplementedError("Subclasses should implement DPage.page!")

    def render(self, **kwargs):
        """
        Render this DPage and return a Django response object.

        :return: response object
        :rtype: HttpResponse
        """
        # init context if nothing in it
        if not self.context:
            self.context = {}

        # render all our objects
        content = render_objects(self.content, **kwargs)

        # if there was nothing, use the default content
        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT

        self.context['content'] = content

        return render(self.request, self.template, self.context)

########################################################################################################################
#
# Content classes and methods
#
########################################################################################################################


class Content(object):
    """
    Base class for content classes.

    Content classes provide content for DPage.  See the examples in the code.
    """
    def __init__(self):
        pass

    def render(self):
        """
        Render this content object.
        """
        raise NotImplementedError("Subclasses should implement Content.render!")

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
        self.content = content
        self.width = kwargs.pop('width', Column.width)
        self.template = kwargs.pop('template', Column.template)
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render objects in column of width width
        """
        out = ''
        for con in self.content:
            out += self.template.format(width=self.width, content=render_objects(con))
        return out


class ColumnX(Column):
    def render(self, **kwargs):
        """
        Render objects in a single column of width width
        """
        out = self.template.format(width=self.width, content=render_objects(self.content))
        return out


def column(*content, **kwargs):
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


def columnX(*content, **kwargs):
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
    Wrap each content in a row.
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
    Wrap all content in a row.
    """
    def render(self, **kwargs):
        """
        Render all objects in a row
        """
        out = self.template.format(content=render_objects(self.content))
        return out


def row(*content, **kwargs):
    return Row(*content, **kwargs)
R = functools.partial(row)


def rowX(*content, **kwargs):
    return RowX(*content, **kwargs)
RX = functools.partial(rowX)


class RowColumn(Row, Column):
    """
    Create a rowcolumn class.  Wrap content in a row wrapping a column.  Equivalent to
    Row(Column(content).render()).render()
    """
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumn object.
        """
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content
        pass

    def render(self, **kwargs):
        """
        Render RowColumn
        :param kwargs:
        """
        out = ''
        out = Column(*self.content, template=self.col_template, **self.kwargs).render()
        out = Row(out, template=self.row_template, **self.kwargs).render()
        return out


class RowColumnX(Row, ColumnX):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.
        """
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content
        pass

    def render(self, **kwargs):
        """
        Render RowColumnX
        """
        out = ''
        out = ColumnX(*self.content, template=self.col_template, **self.kwargs).render()
        out = Row(out, template=self.row_template, **self.kwargs).render()
        return out


class RowXColumn(RowX, Column):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.
        """
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content
        pass

    def render(self, **kwargs):
        """
        Render RowColumnX
        """
        out = ''
        out = Column(*self.content, template=self.col_template, **self.kwargs).render()
        out = RowX(out, template=self.row_template, **self.kwargs).render()
        return out


class RowXColumnX(RowX, ColumnX):
    def __init__(self, *content, **kwargs):
        """
        Initialize RowColumnX object.
        """
        self.row_template = kwargs.pop('row_template', Row.template)
        self.col_template = kwargs.pop('col_template', Column.template)
        self.kwargs = kwargs
        self.content = content
        pass

    def render(self, **kwargs):
        """
        Render RowColumnX
        """
        out = ''
        out = ColumnX(*self.content, template=self.col_template, **self.kwargs).render()
        out = RowX(out, template=self.row_template, **self.kwargs).render()
        return out


def rowcolumn(*content, **kwargs):
    """
    Wrap content in a row and column of width width.

    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
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


def rowXcolumn(*content, **kwargs):
    """
    Wrap content in a row and column of width width.

    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
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


def rowcolumnX(*content, **kwargs):
    """
    Wrap content in a row and column of width width.

    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
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


def rowXcolumnX(*content, **kwargs):
    """
    Wrap content in a row and column of width width.

    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
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

########################################################################################################################
#
# Content classes and methods
#
# Classes to add content to DPage. Classes that add content to a DPage MUST provide a render method.
#
########################################################################################################################
# todo 3: add class to deal with file like objects and queryset objects
# todo 3: add support for select2 https://github.com/applegrew/django-select2
# todo 3: https://github.com/digi604/django-smart-selects provides chained selects for django models

# todo 3: allow form to specify custom template
# todo 2: support rest of bootstrap 3 form attributes
# todo 2: syntactic suggar for Form


class Text(object):
    """
    Holds text for inclusion in the page
    """

    def __init__(self, *content, **kwargs):
        """
        Create text object and initialize it.
        :param content: The text.
        :type content: unicode
        :param kwargs: RFU
        :type kwargs: dict

        """
        self.content = content
        self.kwargs = kwargs
        # todo 2: add text options here and render text in a span
        return

    def render(self, **kwargs):
        """
        Render the Text object

        :param kwargs: RFU
        :type kwargs: dict
        """
        out = ''
        for obj in self.content:
            if hasattr(obj, 'render'):
                out += render_objects(obj, **kwargs)
            else:
                out += obj
        return out


class Markdown(object):
    """
    Holds markdown text for inclusion in a DPage.
    """

    def __init__(self, *content, **kwargs):
        """
        Create a markdown object and initialize it.

        :param content: Text to process as markdown.
        :type content: unicode
        :param kwargs: extensions, RFU
        :type kwargs: dict
        """
        self.content = content
        self.extensions = kwargs.pop('extensions', None)
        self.kwargs = kwargs
        # todo 3: here check text type and deal with file like objects and queryset objects
        # for now just deal with actual text
        # todo 2: add markdown kwargs options here
        pass

    def render(self, **kwargs):
        """
        Render markdown text.
        """
        out = ''
        for obj in self.content:
            if hasattr(obj, 'render'):
                out += render_objects(obj, **kwargs)
            else:
                out += markdown.markdown(force_unicode(obj),
                                         self.extensions if self.extensions else '',
                                         output_format='html5',
                                         safe_mode=False,
                                         enable_attributes=False)
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

    def render(self, **kwargs):
        """
        Render HTML text.
        """
        out = ''
        for obj in self.content:
            if hasattr(obj, 'render'):
                out += render_objects(obj)
            else:
                out += obj
        return out


class Link(object):
    def __init__(self, href, *content, **kwargs):
        """
        Create a DPage Link object and initialize it.

        :param href: Link href
        :type href: unicode
        :param content: Content the link wraps
        :type content:
        :param kwargs:
        """
        self.href = href
        self.content = content
        self.target = kwargs.pop('target', None)
        self.link_class = kwargs.pop('link_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        out = ''
        body = render_objects(self.content)
        target = ''
        if self.target:
            target = 'target="{target}" '.format(self.target)
        link_class = ''
        if self.link_class:
            link_class = 'class="{link_class}" '.format(link_class=self.link_class)
        template = '<a href="{href}" {target} {link_class}>{body}</a>'
        out = template.format(href=self.href, target=target, link_class=link_class, body=body)
        return out


class LinkButton(Link):
    def __init__(self, href, *content, **kwargs):
        link_class = kwargs.pop('link_class', 'btn btn-primary btn-sm')
        super(LinkButton, self).__init__(href, *content, link_class=link_class, **kwargs)
        return

    def render(self):
        out = super(LinkButton, self).render()
        return out


class Button(object):
    """
    DPage button class
    """
    def __init__(self, btn_text, btn_type='btn-default', btn_size=None, btn_extra=None, **kwargs):
        """
        Create a button object.

        :param btn_text: The text to display in the button.
        :type btn_text: unicode
        :param btn_type: The type of button to display per Bootstrap 3
        :type btn_type: unicode
        :param btn_size: The size of the button to display per Bootstrap 3
        :type btn_size: unicode
        :param btn_extra: Extra text for <button ...>.  Used to create buttons for Modal and Panel
        :type btn_extra: unicode
        """
        self.btn_text = btn_text
        self.btn_type = btn_type
        self.btn_size = btn_size if btn_size else ''
        self.btn_extra = btn_extra if btn_extra else ''
        self.kwargs = kwargs
        return

    def render(self):
        template = '<!-- start of button -->\n' \
                   '    <button type="button" class="btn {btn_type} {btn_size}" {btn_extra}>\n' \
                   '        {btn_text}\n' \
                   '    </button>\n' \
                   '<!-- end of button -->\n'
        out = template.format(btn_text=self.btn_text,
                              btn_type=self.btn_type,
                              btn_size=self.btn_size,
                              btn_extra=self.btn_extra)
        return out


class ButtonModal(Button):
    """
    Button to control modal object
    """
    def __init__(self, btn_text, modal, btn_type='btn-default', btn_size=None, **kwargs):
        self.modal = modal
        btn_extra = 'data-toggle="modal" data-target="#{modal_id}" '.format(modal_id=modal.id)
        super(ButtonModal, self).__init__(btn_text, btn_type, btn_size, btn_extra=btn_extra, **kwargs)
        return

    def render(self):
        out = super(ButtonModal, self).render()
        out += self.modal.render()
        return out


class Modal(object):
    """
    Modal object
    """
    def __init__(self, *content, **kwargs):
        self.content = content
        self.button = kwargs.pop('button', None)
        self.header = kwargs.pop('header', None)
        self.footer = kwargs.pop('footer', None)
        self.id = kwargs.pop('id', unique_name('modal'))
        self.modal_label = kwargs.pop('modal_label', unique_name('modal_label'))
        self.kwargs = kwargs
        return

    def render(self):
        out = ''
        t_btn = '<!-- modal button start -->\n' \
                '<button class="btn btn-primary" data-toggle="modal" data-target="#{id}">\n' \
                '    {btn_text}\n' \
                '</button>\n' \
                '<!-- modal button end -->'
        t_top = '<!-- modal start -->\n' \
                '<div class="modal fade" id="{id}" tabindex="-1" role="dialog" \n' \
                '     aria-labelledby="{modal_label}" aria-hidden="true">\n' \
                '    <div class="modal-dialog">\n' \
                '        <div class="modal-content">\n'
        t_hdr = '            <div class="modal-header">\n' \
                '                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">' \
                '                    &times;' \
                '                </button>\n' \
                '                {modal_header}\n' \
                '            </div>\n'
        t_bdy = '            <div class="modal-body">\n' \
                '                {body}\n' \
                '            </div>\n'
        t_ftr = '            <div class="modal-footer">\n' \
                '                {modal_footer}\n' \
                '           </div>\n'
        t_btm = '        </div>\n' \
                '    </div>\n' \
                '</div>\n' \
                '<!-- modal end -->\n'
        out = ''
        body = render_objects(self.content)
        if self.button:
            out += t_btn.format(id=self.id, btn_text=self.button)
        out += t_top.format(id=self.id, modal_label=self.modal_label)
        if self.header:
            hdr = render_objects(self.header)
            out += t_hdr.format(modal_label=self.modal_label, modal_header=hdr)
        out += t_bdy.format(body=body)
        if self.footer:
            ftr = render_objects(self.footer)
            out += t_ftr.format(modal_footer=ftr)
        out += t_btm
        return out


class ButtonPanel(Button):
    """
    Button to control panel object
    """
    def __init__(self, btn_text, panel, btn_type='btn-default', btn_size=None, **kwargs):
        """
        Create a button panel.

        :param btn_text: Text of the button
        :param panel: Panel to attach.  Must be declared before button.
        :param btn_type: Button type per Button.
        :param btn_size: Button size per Button
        :param kwargs: RFU
        """
        self.panel = panel
        btn_extra = 'data-toggle="collapse" data-target="#{panel_id}" '.format(panel_id=panel.id)
        super(ButtonPanel, self).__init__(btn_text, btn_type, btn_size, btn_extra=btn_extra, **kwargs)
        return

    def render(self):
        out = ''
        out += super(ButtonPanel, self).render()
        return out


class Panel(object):
    """
    Collapsible button panel
    """
    # todo 2: add panel heading and footer to buttonpanel
    def __init__(self, *content, **kwargs):
        """
        Create a collapsible panel.

        :param content: Content
        :type content: list
        :param kwargs: Keyword arguments. button=None
        :type kwargs: dict
        """
        self.content = content
        self.button = kwargs.pop('button', None)
        self.id = kwargs.pop('id', unique_name('panel'))
        self.kwargs = kwargs
        # todo 2: add header, footer, and panel class attributes here
        pass

    def render(self, **kwargs):
        """
        Render button collapsible panel.
        """
        t_btn = '<!-- panel button start -->\n' \
                '<button class="btn btn-primary" data-toggle="collapse" data-target="#{id}">\n' \
                '    {btn_text}\n' \
                '</button>\n' \
                '<!-- panel button end -->'
        t_bdy = '<!-- panel start -->\n' \
                '    <div id="{id}" class="collapse">\n' \
                '        {content}\n' \
                '    </div>\n' \
                '<!-- panel end -->\n'

        out = ''
        content = render_objects(self.content, **kwargs)

        if self.button:
            out += t_btn.format(id=self.id, btn_text=self.button)
        out += t_bdy.format(id=self.id, content=content)
        return out


class Accordion(object):
    """
    Accordion support
    """
    def __init__(self, *content, **kwargs):
        """
        Create accordion object.

        :param content: Accordion content.  Must AccordionPanel or list of AccordionRow.
        :type content: list or AccordionPanel
        :param kwargs: RFU
        :type kwargs: dict
        """
        # todo 2: check that content is AccordionPanel or list of AccordionPanel
        # todo 2: add other accordion options in kwargs
        self.content = content
        self.id = kwargs.pop('id', unique_name('accordion_id'))
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render accordion.
        """
        template = '<!-- Start of accordion -->\n' \
                   '<div class="panel-group" id="{accordion_id}">\n' \
                   '    {content}\n' \
                   '</div>\n' \
                   '<!-- End of accordion -->\n'
        content = render_objects(self.content, accordion_id=self.id, **kwargs)
        return template.format(accordion_id=self.id, content=content)


class AccordionPanel(object):
    """
    Panel within an Accordion
    """
    def __init__(self, *content, **kwargs):
        """
        Define accordion panel.
        :param kwargs: title='', default=False
        :type kwargs: dict
        """
        self.content = content
        self.accordion_id = kwargs.pop('accordion_id', None)
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        self.id = kwargs.pop('id', unique_name('panel_id'))
        # todo 2: add other accordion panel options here
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        # Accordion panels can not get their accordion parent id until the parent
        # is created, possibly after the panel is created.  So we may need to fetch
        # the accordion_id here.
        if not self.accordion_id:
            kwargs.pop('accordion_id')

        template = '<!-- start of panel -->\n' \
                   '    <div class="panel panel-default">\n' \
                   '        <div class="panel-heading">\n' \
                   '            <h4 class="panel-title">\n' \
                   '                <a data-toggle="collapse" data-parent="#{accordion_id}" ' \
                   '                    href="#{panel_id}">\n' \
                   '                    {panel_title}\n' \
                   '                </a>\n' \
                   '            </h4>\n' \
                   '        </div>\n' \
                   '        <div id="{panel_id}" class="panel-collapse collapse {panel_collapsed}">\n' \
                   '            <div class="panel-body">\n' \
                   '                {panel_content}\n ' \
                   '            </div>\n' \
                   '        </div>\n' \
                   '    </div>\n' \
                   '<!-- end of panel -->\n'
        content = render_objects(self.content, **kwargs)
        out = template.format(accordion_id=self.accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=self.id,
                              panel_title=self.title,
                              panel_content=content)
        return out


class AccordionMultiPanel(object):
    """
    Panel within an Accordion
    """
    def __init__(self, *content, **kwargs):
        """
        Define accordion panel.
        :param kwargs: title='', default=False
        :type kwargs: dict
        """
        self.content = content
        self.accordion_id = kwargs.pop('accordion_id', None)
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        self.id = kwargs.pop('id', unique_name('panel_id'))
        # todo 2: add other options here
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        # Accordion panels can not get their accordion parent id until the parent
        # is created, possibly after the panel is created.  So we may need to fetch
        # the accordion_id here.
        if not self.accordion_id:
            kwargs.pop('accordion_id')

        template = '<!-- start of panel -->\n' \
                   '    <div class="panel panel-default">\n' \
                   '        <div class="panel-heading">\n' \
                   '            <h4 class="panel-title">\n' \
                   '                <a data-toggle="collapse" data-target="#{panel_id}" ' \
                   '                    href="#{panel_id}">\n' \
                   '                    {panel_title}\n' \
                   '                </a>\n' \
                   '            </h4>\n' \
                   '        </div>\n' \
                   '        <div id="{panel_id}" class="panel-collapse collapse {panel_collapsed}">\n' \
                   '            <div class="panel-body">\n' \
                   '                {panel_content}\n ' \
                   '            </div>\n' \
                   '        </div>\n' \
                   '    </div>\n' \
                   '<!-- end of panel -->\n'
        content = render_objects(self.content, **kwargs)
        out = template.format(accordion_id=self.accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=self.id,
                              panel_title=self.title,
                              panel_content=content)
        return out


# fixme: finish table  do this: http://www.pontikis.net/labs/bs_grid/demo/
class Table(object):
    """
    Table support

    table-responsive
    table-condensed
    table-hover
    table-bordered
    table-striped
    """
    def __init__(self, heading, *content, **kwargs):
        self.heading = heading
        self.content = content
        self.tresponsive = kwargs.pop('tbl_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        out = ''
        # Build table class
        cls = 'table'

        return out


class TableRow(object):
    """
    Table row support

      <tr>
         <td>January</td>
         <td>$100</td>
      </tr>
    """
    def __init__(self, *content, **kwargs):
        self.content = content
        self.tr_class = kwargs.pop('tr_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        out = ''
        for con in self.content:
            if isinstance(con, TableCell):
                out += render_objects(con)
            else:
                out += '<td>' + render_objects(con) + '</td>'
        tr_start = '<tr>'
        if self.tr_class:
            tr_start = '<tr class="{tr_class}" >'.format(self.tr_class)
        out = tr_start + out + '</tr>'
        return out


def TR(*content, **kwargs):
    tr = TableRow(content, kwargs)
    return tr


class TableCell(object):
    """
    Table cell support
    """
    def __init__(self, *content, **kwargs):
        """
        Initialize a td table element

        :param content: content
        :type content: object or list
        :param kwargs: RFU
        :type: dict
        """
        self.content = content
        self.td_class = kwargs.pop('td_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        td_start = '<td>'
        if self.td_class:
            td_start = '<td class="{td_class}" >'.format(td_class=td_class)
        out = ''
        for con in self.content:
            out += td_start + render_objects(con) + '</td>\n'
        return out


def TD(*content, **kwargs):
    td = TableCell(content, kwargs)
    return td


class TableHead(object):
    """
    Table head support

     <thead>
      <tr>
         <th>Month</th>
         <th>Savings</th>
      </tr>
     </thead>

    """
    def __init__(self, *content, **kwargs):
        """
        """
        pass

    def render(self):
        out = ''
        return out


class TableFoot(object):
    """
    Table foot support

     <tfoot>
      <tr>
         <td>Sum</td>
         <td>$180</td>
      </tr>
     </tfoot>

    """
    def __init__(self, *content, **kwargs):
        """
        """
        pass

    def render(self):
        out = ''
        return out


class Table2(object):
    """
    Provide django-tables2 support
    """
    def __init__(self, dpage, qs, **kwargs):
        """
        Initialize a Table object

        :param dpage: dpage object
        :type dpage: DPage
        :param qs: Queryset
        :type qs:
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.dpage = dpage
        self.qs = qs
        self.kwargs = kwargs
        # todo 2: add other kwargs options here
        pass

    def render(self, **kwargs):
        """
        Generate html for table
        """
        template = '<!-- start of table -->\n' \
                   '    {% load django_tables2 %}\n' \
                   '    {% render_table insert_the_table %}\n' \
                   '<!-- end of table -->\n'
        t = Template(template)
        c = {'insert_the_table': self.qs, 'request': self.dpage.request}
        output = t.render(Context(c))
        return output
        # output = ''
        # name = unique_name('table')
        # self.dpage.context[name] = self.qs
        # template = '<!-- start of table -->\n' \
        #            '    {% render_table x_the_table_object %}\n' \
        #            '<!-- end of table -->\n'
        # output = template.replace('x_the_table_object', name)
        # return output

# todo 1: add support for table sorter: http://mottie.github.io/tablesorter/docs/index.html
# http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# looks good: http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# https://github.com/Mottie/tablesorter/wiki

class Form(object):
    """
    Provide form support
    """
    def __init__(self, dpage, form, submit='Submit', initial=None, action_url=None, **kwargs):
        """
        Create a form object.

        :param dpage: dpage object
        :type dpage: DPage
        :param form: form object
        :type form: forms.Form
        :param submit: text for submit button.  If None, no submit button.
        :type submit: unicode
        :param initial: initial bound values
        :type initial: dict or None
        :param action_url: submit action url
        :type action_url: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.dpage = dpage
        self.form = form
        self.submit = submit
        self.initial = initial
        self.action_url = action_url
        self.kwargs = kwargs
        # todo 2: add other kwargs options here
        pass

    def render(self, **kwargs):
        """
        Create and render the form
        """
        #
        #  Alternate form template
        #
        # <form method="post" class="bootstrap3" action="/graphpages/graphpage/{{ graph_pk }}"> {% csrf_token %}
        #     {# Include the hidden fields #}
        #     {% for hidden in graphform.hidden_fields %}
        #         {{ hidden }}
        #     {% endfor %}
        #     {# Include the visible fields #}
        #     {% for field in graphform.visible_fields %}
        #         {% if field.errors %}
        #             <div class="row bg-danger">
        #                 <div class="col-md-3 text-right"></div>
        #                 <div class="col-md-7">{{ field.errors }}</div>
        #             </div>
        #         {% endif %}
        #         <div class="row">
        #             <div class="col-md-3 text-right">{{ field.label_tag }}</div>
        #             <div class="col-md-7">{{ field }}</div>
        #         </div>
        #     {% endfor %}
        #     <div class="row">
        #         <div class='col-md-3 text-right'>
        #             <input type="submit" value="Display graph" class="btn btn-primary"/>
        #         </div>
        #     </div>
        # </form>
        #
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),
        if self.initial:
            the_form = self.form(self.initial)
        elif len(self.dpage.request.POST) > 0:
            the_form = self.form(self.dpage.request.POST)
        else:
            the_form = self.form()
        request = self.dpage.request
        form_class_name = self.form.__name__
        template_top = '{% load bootstrap3 %}\n' \
                       '<!-- start of django bootstrap3 form -->\n' \
                       '    <form role="form" action="{action_url}" method="post" class="form">\n' \
                       '        <!-- csrf should be here -->{% csrf_token %}<!-- -->\n' \
                       '        <!-- our form class name -->' \
                       '            <input type="hidden" name="form_class_name" value="{form_class_name}" >\n' \
                       '        {% bootstrap_form the_form %}\n'
        template_button = '        {% buttons %}\n' \
                          '            <button type="submit" class="btn btn-primary">\n' \
                          '                {% bootstrap_icon "star" %} {submit_text}\n' \
                          '            </button>\n' \
                          '        {% endbuttons %}\n'
        template_bottom = '    </form>\n' \
                          '<!-- end of django bootstrap3 form -->\n'
        template = template_top
        if self.submit:
            template += template_button
        template += template_bottom

        # Do NOT use format here since the template contains {% ... %}
        template = template.replace('{action_url}', self.action_url if self.action_url else '/dpages/')
        template = template.replace('{form_class_name}', form_class_name)
        if self.submit:
            template = template.replace('{submit_text}', self.submit)
        t = Template(template)
        c = {'the_form': the_form}
        c.update(csrf(request))
        output = t.render(Context(c))
        return output
        # return template

# todo 1: add support for normal bootstrap 3 forms
# todo 1: add id to Form

########################################################################################################################
#
# Carousel
#
########################################################################################################################


class Carousel(object):
    """
    Carousel
    """
    def __init__(self, *content, **kwargs):
        self.content = content
        self.id = kwargs.pop('id', unique_name('carousel_id'))
        self.data_interval = kwargs.pop('data-interval', 'false')
        self.indicators = kwargs.pop('indicators', None)
        self.background_color = kwargs.pop('background-color', '#D8D8D8')
        return

    def render(self):
        t_ind = '<!-- Start Bottom Carousel Indicators -->\n' \
                '<ol class="carousel-indicators">\n' \
                '    <li data-target="#{carousel_id}" data-slide-to="0" class="active"></li>\n' \
                '    <li data-target="#{carousel_id}" data-slide-to="1"></li>\n' \
                '    <li data-target="#{carousel_id}" data-slide-to="2"></li>\n' \
                '</ol>\n<!-- End Bottom Carousel Indicators -->\n'
        out = """
                  <div class="carousel slide" data-ride="carousel" id="{carousel_id}" data-interval="{data_interval}">

                    <!-- Carousel Slides / Quotes -->
                    <div class="carousel-inner" style="background-color: {background_color};">

                      <!-- Quote 1 -->
                      <div class="item active">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <small>Someone famous</small>
                              <p>1 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>2 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>3 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>4 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>5 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>6 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                              <p>7 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit!</p>
                            </div>
                          </div>
                      </div>
                      <!-- Quote 2 -->
                      <div class="item">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam auctor nec lacus ut tempor. Mauris.</p>
                            </div>
                          </div>
                      </div>
                      <!-- Quote 3 -->
                      <div class="item">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut rutrum elit in arcu blandit, eget pretium nisl accumsan. Sed ultricies commodo tortor, eu pretium mauris.</p>
                            </div>
                          </div>
                      </div>
                    </div>

                    <!-- Carousel Buttons Next/Prev -->
                    <a data-slide="prev" href="#{carousel_id}" class="left carousel-control">
                        <i class="fa fa-chevron-left"></i>
                    </a>
                    <a data-slide="next" href="#{carousel_id}" class="right carousel-control">
                        <i class="fa fa-chevron-right"></i>
                    </a>


                  </div>
            """
        t_jsf = """
                    <!-- Controls buttons -->
                    <div style="text-align:center;">
                      <input type="button" class="btn start-slide" value="Start">
                      <input type="button" class="btn pause-slide" value="Pause">
                      <input type="button" class="btn prev-slide" value="Previous Slide">
                      <input type="button" class="btn next-slide" value="Next Slide">
                      <input type="button" class="btn slide-one" value="Slide 1">
                      <input type="button" class="btn slide-two" value="Slide 2">
                      <input type="button" class="btn slide-three" value="Slide 3">
                    </div>
                  <script>
                     $(function(){
                        // Initializes the carousel
                        $(".start-slide").click(function(){
                           $("#{carousel_id}").carousel('cycle');
                        });
                        // Stops the carousel
                        $(".pause-slide").click(function(){
                           $("#{carousel_id}").carousel('pause');
                        });
                        // Cycles to the previous item
                        $(".prev-slide").click(function(){
                           $("#{carousel_id}").carousel('prev');
                        });
                        // Cycles to the next item
                        $(".next-slide").click(function(){
                           $("#{carousel_id}").carousel('next');
                        });
                        // Cycles the carousel to a particular frame
                        $(".slide-one").click(function(){
                           $("#{carousel_id}").carousel(0);
                        });
                        $(".slide-two").click(function(){
                           $("#{carousel_id}").carousel(1);
                        });
                        $(".slide-three").click(function(){
                           $("#{carousel_id}").carousel(2);
                        });
                     });
                  </script>
                """
        out = out.format(carousel_id=self.id,
                         data_interval=self.data_interval,
                         background_color=self.background_color)
        # out += t_jsf.replace('{carousel_id}', self.id)
        return out


########################################################################################################################
#
# Graph routines
#
########################################################################################################################

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']

# todo 1: add data links, see http://stackoverflow.com/questions/19399346/need-to-link-url-in-highchart
# todo 1: http://birdchan.com/home/2012/09/07/highcharts-pie-charts-can-have-url-links/comment-page-1/
class Graph(object):
    """
    DPage graph object class that uses Chartkick.
    """
    # noinspection PyShadowingBuiltins
    def __init__(self, graph_type, data, options=None, **kwargs):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode or list[dict] or dict
        :param options: 'with' options for the chartkick graph.
        :type options: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))

        # todo 2: when this is working, remove the unneeded class attributes
        # todo 2: since all that's really needed is self.output
        self.graph_type = graph_type  # save type of graph
        self.data = data  # the data to display
        self.options = options  # chartkick with options
        self.kwargs = kwargs
        pass

    def render(self, **kwargs):
        """
        Render the graph
        """
        # Generate the chartkick graph template text
        data = self.data
        if self.options:
            options = self.set_options()
            chart = '{}_chart data with {}'.format(self.graph_type, options)
            pass
        else:
            chart = '{}_chart data'.format(self.graph_type)
            pass
        t = Template('{% load chartkick %} {% ' + chart + ' %}')

        # render
        output = t.render(Context({'data': data}))

        return output

    def set_options(self):
        """
        Set chartkick & highchart options
            options = "height='500px' library=" + str(library)

        """
        options = copy(self.options)
        out = ''

        # deal with height, max, and min
        height = options.pop('height', None)
        if height:
            out += " height='{}'".format(height)
        xmax = options.pop('max', None)
        if xmax:
            out += " max='{}'".format(xmax)
        xmin = options.pop('min', None)
        if xmin:
            out += " min='{}'".format(xmin)

        # Is there anythin left
        if len(options) < 1:
            return out

        # These are library options of the form title.text: ...
        library = {}
        for key, value in options.iteritems():
            dict_nested_set(library, key, value)
        out += " library={}".format(str(library))

        return out
