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
# Register classes
#
########################################################################################################################
########################################################################################################################
#
# DPage class
#
########################################################################################################################


class DPage(object):
    """
    DPage, aka Django Page class.

    A DPage objects holds a Django Page.  It consists of an optional form and 0 or more DPage clild objects.

    Conceptually, a DPage displays a filter form that a user can use to customize the output of the DPage's
    objects.
    """

    def __init__(self, request=None, context=None, template=None, objs=None, **kwargs):
        """
        Initialize the DPage.

        :param request: The request object
        :type request: WSGIRequest
        :param context: Context values for the page
        :type context: dict
        :param template: template name to use for this DPage object.  If None, DPageDefaultTemplate specified in
                         settings is used.
        :type template: unicode
        :param objs: The DPage... like object(s) for this DPage.
        :type objs: list or DjangoPageGrid or DjangoPagePage or DjangoPageRow or DjangoPageColumn or object or ...
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.request = request
        self.context = context
        self.template = template if template else settings.DPAGE_DEFAULT_TEMPLATE
        self.objects = objs if objs else []
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
                    self.layout(RC12(xr1, xr2, xr3))
                    return self
        """
        raise NotImplementedError("Subclasses should implement this!")

    def render(self, **kwargs):
        """
        Render this DPage.

        :return: response object
        :rtype: HttpResponse
        """
        # init context if nothing in it
        if not self.context:
            self.context = {}

        # render all our objects
        content = render_objects(self.content, request=self.request, **kwargs)

        # if there was nothing, use the default content
        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT

        self.context['content'] = content

        return render(self.request, self.template, self.context)

        # todo: consider coding the template here and simplifing the base, alternately read from file
        # # build out template & pour in the content
        # template = '{% extends "base.html" %}\n' \
        #            '{% load django_tables2 %}\n' \
        #            '{% block content %}\n' \
        #            '<!-- Start of dpage page -->\n' \
        #            '    <div class="container-fluid">\n' \
        #            '        insert_the_content_here\n' \
        #            '    </div>\n' \
        #            '<!-- End of dpage page -->\n' \
        #            '{% endblock content %}\n'
        # output = template.replace('insert_the_content_here', content)
        #
        # # create template and context objects
        # t = Template(output)
        # c = Context(self.context)
        #
        # return HttpResponse(t.render(c))


########################################################################################################################
#
# Layout support classes and methods.  Really just syntactic sugar to make layout easier.
#
########################################################################################################################
#
#  A DPage contains a list of rows.  Each row may have multiple columns.  Columns have a default or
# specified width.  Columns can contain anything that has a render method.  Rows may be nested in columns may be
# nested in rows ... to whatever deapth amuses.  Past 2 or 3 it's probably not a good idea.
#
#     row_________________________________________________________________________________________________
#     col________________________ col__________________________ col_______________________________________
#     form_______________________ graph________________________ table_____________________________________
#     text_______________________ markdown_____________________ html______________________________________
#
# Example:
#         x1 = Text('Row 1: This text comes from dpage.Text')
#         x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
#         x22 = HTML('<p>Row 2 col 2: </p><h3>H3 text from DPageHTML</h3>')
#         x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(get_paragraph()))
#         x41 = HTML('<p>Row 4 col 1:{}</p>'.format(get_paragraph()))
#         x42 = HTML('<p>Row 4 col 2:{}</p>'.format(get_paragraph()))
#         x51 = HTML('<p>Row 5 col 1:{}</p>'.format(get_paragraph()))
#         x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(get_paragraph()))
#         x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(get_paragraph()))
#         x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(get_paragraph()))
#         x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(get_paragraph()))
#         x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(get_paragraph()))
#         # page.layout(R(C3(x41), C9(x42)))
#         self.layout(RC12(x1),
#                     RC6(x21, x22),
#                     RC(x3),
#                     R(C3(x41), C9(R(x42))),
#                     R(C3(x51), C9(R(x521),
#                                   R(x522),
#                                   RC4(x5231, x5232, x5233)
#                                   )
#                       )
#                     )
#
########################################################################################################################


class Column(object):
    """
    Wrap content in a column.
    """
    def __init__(self, *content, **kwargs):
        """
        Wrap *content objects in column of width width=nn.

        :param content: Content to wrap in a column of width width
        :type content: object or collections.iterable
        :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
        :type kwargs: dict
        :return: Column object
        :rtype: Column object
        """
        self.content = content
        self.width = kwargs.pop('width', 12)
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render objects in column

        :param kwargs: RFU
        :type kwargs: dict
        """
        dpage_col_before = '<!-- Start of dpage col -->\n' \
                           '<div class="col-md-{width}">\n'
        dpage_col_after = '</div>\n' \
                          '<!-- End of dpage col -->\n'

        out = render_objects(self.content)
        out = dpage_col_before.format(width=self.width) + out + dpage_col_after
        return out


def column(*content, **kwargs):
    """
    :param content: Content to wrap in a column of width width
    :type content: object or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
    """
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


class Row(object):
    """
    Wrap content in a row.
    """
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
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render objects in row

        :param kwargs: RFU
        :type kwargs: dict
        """
        # HTML to create a bootstrap3 row
        dpage_row_before = '<!-- Start of dpage row -->\n' \
                           '<div class="row">\n'
        dpage_row_after = '</div>\n' \
                          '<!-- End of dpage row -->\n'

        out = ''
        for con in self.content:
            if hasattr(con, 'render'):
                out += con.render()
            else:
                out += con
        out = dpage_row_before + out + dpage_row_after
        return out


def row(*content, **kwargs):
    """
    Wrap content in a bootstrap 3 row
    :param content: The html content to wrap
    :type content: unicode
    :param kwargs: RFU
    :type kwargs: dict
    """
    return Row(*content, **kwargs)
R = functools.partial(row)


class RowColumn(object):
    """
    Wrap content in a row with columns of width width.
    """
    def __init__(self, *content, **kwargs):
        """
        Wrap *content objects in column of width width=nn.

        :param content: Content to wrap in a row with multiple columns of width width
        :type content: object or collections.iterable
        :param kwargs: Optional arguments, bootstrap 'width' RFU
        :type kwargs: dict
        :return: RowColumn object
        :rtype: RowColumn object
        """
        self.content = content
        self.width = kwargs.pop('width', 12)
        self.kwargs = kwargs
        pass

    def render(self, **kwargs):
        """
        Render objects in row/column

        :param kwargs: RFU
        :type kwargs: dict
        """
        # out = render_objects(self.content)
        out = ''
        for con in self.content:
            outcol = Column(con, width=self.width).render()
            outrow = Row(outcol).render()
            out += outrow
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


class Row1Column(object):
    """
    Wrap content in a row with columns of width width.
    """
    def __init__(self, *content, **kwargs):
        """
        Wrap *content objects in column of width width=nn.

        :param content: Content to wrap in a row with multiple columns of width width
        :type content: object or collections.iterable
        :param kwargs: Bootstrap 3 width, rest RFU
        :type kwargs: dict
        :return: RowColumn object
        :rtype: RowColumn object
        """
        self.content = content
        self.width = kwargs.pop('width', 12)
        self.kwargs = kwargs
        pass

    def render(self, **kwargs):
        """
        Render objects in row/column

        :return: HTML
        :rtype: unicode
        """
        out = ''
        for con in self.content:
            out += Column(con, width=self.width).render()
        out = Row(out).render()
        return out


def row1column(*content, **kwargs):
    """
    Wrap content in a row and column of width width.

    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
    """
    return Row1Column(*content, **kwargs)
R1C = functools.partial(row1column, width=12)
R1C1 = functools.partial(row1column, width=1)
R1C2 = functools.partial(row1column, width=2)
R1C3 = functools.partial(row1column, width=3)
R1C4 = functools.partial(row1column, width=4)
R1C5 = functools.partial(row1column, width=5)
R1C6 = functools.partial(row1column, width=6)
R1C7 = functools.partial(row1column, width=7)
R1C8 = functools.partial(row1column, width=8)
R1C9 = functools.partial(row1column, width=9)
R1C10 = functools.partial(row1column, width=10)
R1C11 = functools.partial(row1column, width=11)
R1C12 = functools.partial(row1column, width=12)


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


LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']


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
        out = ''
        out += super(ButtonModal, self).render()
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
        self.id = kwargs.pop('id', static_name_generator('modal'))
        self.modal_label = kwargs.pop('modal_label', static_name_generator('modal_label'))
        self.kwargs = kwargs
        return

    def render(self):
        out = ''
        t_btn = '<button class="btn btn-primary" data-toggle="modal" data-target="#{id}">' \
                '    {btn_text}' \
                '</button>'
        t_top = '<!-- modal start -->\n' \
                '<div class="modal fade" id="{id}" tabindex="-1" role="dialog" \n' \
                '     aria-labelledby="{modal_label}" aria-hidden="true">\n' \
                '    <div class="modal-dialog">\n' \
                '        <div class="modal-content">\n'
        t_hdr = '            <div class="modal-header">\n' \
                '                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">' \
                '                    &times;' \
                '                </button>\n' \
                '                <h4 class="modal-title" id="{modal_label}">{modal_header}</h4>\n' \
                '            </div>\n'
        t_bdy = '            <div class="modal-body">\n' \
                '                {body}\n' \
                '            </div>\n'
        t_ftr = '            <div class="modal-footer">\n' \
                '                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\n' \
                '                <button type="button" class="btn btn-primary">Save changes</button>\n' \
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
            out += t_hdr.format(modal_label=self.modal_label, modal_header=self.header)
        out += t_bdy.format(body=body)
        if self.footer:
            out += t_ftr
        out += t_btm
        return out


# class ButtonModal(object):
#     """
#     Modal object with a button to activate
#     """
#     def __init__(self, button, *content, **kwargs):
#         self.button = button
#         self.modal = Modal(*content, **kwargs)
#         return
#
#     def render(self):
#         out = ''
#         return

########################################################################################################################
#
# Model
#
########################################################################################################################
# todo 1: add model support http://getbootstrap.com/javascript/#modals
# fixme: create pure modal and panel, pure link and button, content objects to connect the two via the id



########################################################################################################################
#
# Carousel
#
########################################################################################################################
# todo 1: add carousel support http://getbootstrap.com/javascript/#carousel

########################################################################################################################
#
# Panel
#
########################################################################################################################


# todo 1: add panel object with support for header, footer, and panel class
class Panel(object):
    def __init__(self):
        pass
    def render(self):
        pass

########################################################################################################################
#
# Collapsed button panel
#
########################################################################################################################
# todo 1: modify Button Panel so that panel and button are separated

class ButtonPanel(object):
    """
    Collapsible button panel
    """
    # todo 2: add panel heading and footer to buttonpanel
    def __init__(self, *content, **kwargs):
        """
        Create a collapsible panel on a button.

        :param content: Content
        :type content: list
        :param kwargs: Keyword arguments. title=None, btn_type='btn-primary'
        :type kwargs: dict
        :return: HTML for button panel
        :rtype: unicode
        """
        self.content = content
        self.title = kwargs.pop('title', '')
        self.btn_type = kwargs.pop('button', 'btn-primary')
        self.id = kwargs.pop('id', static_name_generator('btn_collapse'))
        self.kwargs = kwargs
        # todo 2: add header, footer, and panel class attributes here
        pass

    def render(self, **kwargs):
        """
        Render button collapsible panel.
        """
        template = '<!-- Start of button collapsible panel -->\n' \
                   '    <button type="button" class="btn {btn_type}" data-toggle="collapse" data-target="#{bp_id}">\n' \
                   '        {title}\n ' \
                   '    </button>\n ' \
                   '    <div id="{bp_id}" class="collapse">\n' \
                   '        {content}\n' \
                   '    </div>\n' \
                   '<!-- End of button collapsible panel -->\n'
        content = render_objects(self.content, **kwargs)
        out = template.format(btn_type=self.btn_type, bp_id=self.id, title=self.title, content=content)
        return out

########################################################################################################################
#
# Panel and Accordion support
#
########################################################################################################################


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
        self.id = kwargs.pop('id', static_name_generator('accordion_id'))
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
        self.id = kwargs.pop('id', static_name_generator('panel_id'))
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
        self.id = kwargs.pop('id', static_name_generator('panel_id'))
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

########################################################################################################################

########################################################################################################################


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
# todo 1: add support for table sorter: http://mottie.github.io/tablesorter/docs/index.html
# http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# looks good: http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# https://github.com/Mottie/tablesorter/wiki


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
        # name = static_name_generator('table')
        # self.dpage.context[name] = self.qs
        # template = '<!-- start of table -->\n' \
        #            '    {% render_table x_the_table_object %}\n' \
        #            '<!-- end of table -->\n'
        # output = template.replace('x_the_table_object', name)
        # return output

########################################################################################################################
#
# Support Routines
#
########################################################################################################################


def static_name_generator(base_name='x'):
    """
    Returns a unique name of the form base_name_counter
    :param base_name:
    """
    if not hasattr(static_name_generator, "counter"):
        static_name_generator.counter = 0  # it doesn't exist yet, so initialize it
    static_name_generator.counter += 1
    return '{}_{}'.format(base_name, static_name_generator.counter)


def render_objects(objects, **kwargs):
    """
    Render the object list.

    Note: kwargs should/must contain the request object!!!

    :param objects: list of objects or object to render
    :type: list or object
    :param kwargs: extra arguments for render
    :type kwargs: dict
    :return: Rendered output of objects
    :rtype: unicode
    """
    # if whatever is in objs is iterable, iterate over the objects and render each according to whatever it is
    # otherwise, just render whatever it is
    out = ''
    if isinstance(objects, collections.Iterable):
        for obj in objects:
            if hasattr(obj, 'render'):
                out += obj.render(**kwargs)
            elif isinstance(obj, basestring):
                out += obj
            elif isinstance(obj, collections.Iterable):
                out += render_objects(obj, **kwargs)
            else:
                out += obj
        return out
    elif hasattr(objects, 'render'):
        return objects.render(**kwargs)
    else:
        return objects
