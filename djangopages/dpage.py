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
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from djangopages.libs import dict_nested_set

# HTML to create a bootstrap3 row
dpage_row_before = '<!-- Start of dpage row -->' \
                   '<div class="row">'
dpage_row_after = '</div>' \
                  '<!-- End of dpage row -->'
dpage_col_before = '<!-- Start of dpage col -->' \
                   '<div class="col-md-{}">'
dpage_col_after = '</div>' \
                  '<!-- End of dpage col -->'

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

    def __init__(self, request=None, context=None, template=None, objs=None, form=None, width=12):
        """
        Initialize the DPage.

        :param request: The request object
        :param context: Context values for the page
        :type context: dict
        :param template: template name to use for this DPage object.  If None, DPageDefaultTemplate specified in
                         settings is used.
        :type template: unicode
        :param objs: The DPage... like object(s) for this DPage.
        :type objs: list or DjangoPageGrid or DjangoPagePage or DjangoPageRow or DjangoPageColumn or object or ...
        :param form: DPageForm object holding the form for this DPage
        :type form: DPageForm
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        """
        # fixme: add title, slug, description, created, madified, tags, and ev (eval result) to the class
        self.request = request
        self.context = context
        self.template = template if template else settings.DPAGE_DEFAULT_TEMPLATE
        self.objects = objs if objs else []
        self.form = form                                    # todo: don't think I need this, leave for a bit
        self.width = width  # width of page                 # todo: don't think I need this, leave for a bit
        self.content = []
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
        # if there is a layout, use it to render
        content = render_objects(self.content, request=self.request, **kwargs)

        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT

        return render_to_response(self.template,
                                  {'content': content})

    # class _Text(object):
    #     def __init__(self, text):
    #         self.text = text
    #         pass
    #     def render(self):
    #         return self.text
    #
    # def Text(self, text):
    #     """
    #     Create a text object on the page
    #     """
    #     obj = self._Text(text)
    #     self.objects.append(obj)
    #     return obj

########################################################################################################################
#
# Layout support methods.  Really just syntactic sugar to make layout easier.
#
# A DPage contains a list of rows.  Each row may have multiple columns.  Columns have a default or
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
        self.objs = content
        self.width = kwargs.pop('width', 12)
        return

    def render(self, **kwargs):
        """
        Render objects in column

        :return: HTML
        :rtype: unicode
        """
        out = ''
        for obj in self.objs:
            out += obj.render()
        out = dpage_col_before.format(self.width) + out + dpage_col_after
        return out


def column(*content, **kwargs):
    """
    :param content: Content to wrap in a column of width width
    :type content: object or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
    """
    return Column(*content, **kwargs)
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
    def __init__(self, *content):
        """
        Wrap *content objects in row.

        :param content: Content to wrap in a row
        :type content: object or collections.iterable
        :return: Row object
        :rtype: Row object
        """
        self.content = content
        return

    def render(self, **kwargs):
        """
        Render objects in row

        :return: HTML
        :rtype: unicode
        """
        out = ''
        for con in self.content:
            out += con.render()
        out = dpage_row_before + out + dpage_row_after
        return out


def row(*content, **kwargs):
    """
    Wrap content in a bootstrap 3 row
    :param content: The html content to wrap
    :type content: unicode
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
        :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
        :type kwargs: dict
        :return: RowColumn object
        :rtype: RowColumn object
        """
        self.content = content
        self.width = kwargs.pop('width', 12)
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
        out = dpage_row_before + out + dpage_row_after
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


########################################################################################################################
#
# Collapsed panel
#
########################################################################################################################


class Panel(object):
    """
    Collapsible panel
    """
    def __init__(self, *content, **kwargs):
        """
        Create a collapsible panel on a button.

        :param content: Content
        :type content: list
        :param kwargs: Keyword arguments. title=None, btn_type='btn-primary'
        :type kwargs: dict
        :return: HTML for panel
        :rtype: unicode
        """
        self.content = content
        self.title = kwargs.pop('title', '')
        self.btn_type = kwargs.pop('button', 'btn-primary')
        pass

    def render(self, **kwargs):
        """
        Render collapsible panel.
        """
        name = static_name_generator('btn_collapse')
        template = '<!-- Start of collapsible panel -->\n' \
                   '    <button type="button" class="btn {btn_type}" data-toggle="collapse" data-target="#{name}">\n' \
                   '        {title}\n ' \
                   '    </button>\n ' \
                   '    <div id="{name}" class="collapse">\n' \
                   '        {content}\n' \
                   '    </div>\n' \
                   '<!-- End of collapsable panel -->\n'
        content = render_objects(self.content, **kwargs)
        out = template.format(btn_tpe=self.btn_type, name=name, title=self.title, content=content)
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
    def __init__(self, *content):
        """
        Create accordion object.

        :param content: Accordion content.  Must AccordionPanel or list of AccordionRow.
        :type content: list or AccordionPanel
        """
        # todo: check that content is AccordionPanel or list of AccordionPanel
        self.content = content
        return

    def render(self, **kwargs):
        """
        Render accordion.
        """
        accordion_id = static_name_generator('accordion_id')
        template = '<!-- Start of accordion -->\n' \
                   '<div class="panel-group" id="{accordion_id}">\n' \
                   '    {content}\n' \
                   '</div>\n' \
                   '<!-- End of accordion -->\n'
        content = render_objects(self.content, accordion_id=accordion_id, **kwargs)
        return template.format(accordion_id=accordion_id, content=content)


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
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        accordion_id = kwargs['accordion_id']

        panel_id = static_name_generator('panel_id')
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
        out = template.format(accordion_id=accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=panel_id,
                              panel_title=self.title,
                              panel_content=content)
        return out


class AccordionPanelN(object):
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
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        accordion_id = kwargs['accordion_id']

        panel_id = static_name_generator('panel_id')
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
        out = template.format(accordion_id=accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=panel_id,
                              panel_title=self.title,
                              panel_content=content)
        return out

########################################################################################################################
#
# Classes to add content to DPage. Classes that add content to a DPage should derive from ContentBase and
# MUST provide a render method.
#
########################################################################################################################


class ContentBase(object):
    """
    Base class for all objects that render actual content as opposed to formating (aka row/column/etc).
    """

    def __init__(self, **kwargs):
        self.request = kwargs.pop('request', None)
        return

    def render(self, **kwargs):
        """
        This method should return the HTML to render the object.
        """
        raise NotImplementedError("Subclasses should implement render method!")


class Text(ContentBase):
    """
    Holds text for inclusion in the page
    """

    def __init__(self, text, **kwargs):
        """
        Create text object and initialize it.
        :param text: The text.
        :type text: unicode
        :param kwargs: additional arguments for base class
        :type kwargs:

        """
        super(Text, self).__init__(**kwargs)
        self.text = text
        return

    def render(self, **kwargs):
        """
        Render the Text object
        """
        return self.text


class Markdown(ContentBase):
    """
    Holds markdown text for inclusion in a DPage.
    """

    def __init__(self, markdown_text, extensions=None, **kwargs):
        """
        Create a markdown object and initialize it.

        :param markdowntext: Text to process as markdown.
        :type markdowntext: unicode
        :param extensions: Optional markdown options string.  See python markdown documentation.
        :type extensions: unicode or None
        :param kwargs: additional arguments for base class
        :type kwargs:
        """
        super(Markdown, self).__init__(**kwargs)
        self.extensions = extensions
        self.markdown_text = markdown_text
        # todo: here check text type and deal with file like objects and queryset objects
        # for now just deal with actual text
        pass

    def render(self, **kwargs):
        """
        Render markdown text.

        :return: html version of markdown text
        :rtype: unicode
        """
        return markdown.markdown(force_unicode(self.markdown_text),
                                 self.extensions if self.extensions else '',
                                 output_format='html5',
                                 safe_mode=False,
                                 enable_attributes=False)


class HTML(ContentBase):
    """
    Holds HTML text for inclusion in a DPage.  This is a convenience method since DPageMarkdown can be
    used interchangeably.
    """

    def __init__(self, htmltext, **kwargs):
        """
        Create a DPageHTML object and initialize it.

        :param htmltext: Text to process as markdown.
        :type htmltext: unicode
        """
        super(HTML, self).__init__(**kwargs)
        self.htmltext = htmltext
        # todo: here check text type and deal with file like objects and queryset objects
        # for now just deal with actual text
        pass

    def render(self, **kwargs):
        """
        Render HTML text.

        :return: html version of markdown text
        :rtype: unicode
        """
        return self.htmltext


class Graph(ContentBase):
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
        """
        super(Graph, self).__init__(**kwargs)
        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))

        # todo 2: when this is working, remove the unneeded class attributes
        # todo 2: since all that's really needed is self.output
        self.graph_type = graph_type  # save type of graph
        self.data = data  # the data to display
        self.options = options  # chartkick with options
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
LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']


class Form(ContentBase):
    """
    Provide form support
    """
    def __init__(self, dpage, form, submit='Submit', initial=None, action_url=None, **kwargs):
        super(Form, self).__init__(**kwargs)
        self.dpage = dpage
        self.form = form
        self.submit = submit
        self.initial = initial
        self.action_url = action_url
        pass

    def render(self, **kwargs):
        """
        Create and render the form
        """
        if self.initial:
            the_form = self.form(self.initial)
        else:
            the_form = self.form()
        request = self.dpage.request
        template = '{% load bootstrap3 %}\n' \
                   '<!-- start of django bootstrap3 form -->\n' \
                   '    <form action="{action_url}" method="post" class="form">\n' \
                   '        <!-- csrf should be here -->{% csrf_token %}<!-- -->\n' \
                   '        {% bootstrap_form the_form %}\n' \
                   '        {% buttons %}\n' \
                   '            <button type="submit" class="btn btn-primary">\n' \
                   '                {% bootstrap_icon "star" %} Submit\n' \
                   '            </button>\n' \
                   '        {% endbuttons %}\n' \
                   '    </form>\n' \
                   '<!-- end of django bootstrap3 form -->\n'
        # Do NOT use format here since the template contains {% ... %}
        template = template.replace('{action_url}', self.action_url if self.action_url else '/dpages/')
        t = Template(template)
        c = {'the_form': the_form}
        c.update(csrf(request))
        output = t.render(Context(c))
        return output
        # return template

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
    content = ''
    if isinstance(objects, collections.Iterable):
        for obj in objects:
            if isinstance(obj, collections.Iterable):
                content += render_objects(obj, **kwargs)
            else:
                content += obj.render(**kwargs)
        return content
    else:
        return objects.render(**kwargs)
