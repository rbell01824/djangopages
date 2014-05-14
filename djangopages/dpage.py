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
from django.template import add_to_builtins
from django.utils.encoding import force_unicode
from django.template import Template, Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

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

    def __init__(self, template=None, objs=None, form=None, width=12):
        """
        Initialize the DPage.

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
        self.template = template if template else settings.DPAGE_DEFAULT_TEMPLATE
        self.objs = []
        self.content = ''
        self.form = form
        if objs:
            self.objs = objs  # graph objects in this cell
        self.width = width  # width of this column
        pass

    def layout(self, *content):
        """
        Save page content from a layout.

        :param content:
        :type: tuple
        A layout establishes the row column structure using the helper r... and c... methods.  Example:

        self.layout(rc12(x1),
                    rc6(x21, x22),
                    rc(x3),
                    r(c3(x41), c9(r(x42))),
                    r(c3(x51), c9(r(x521),
                                  r(x522),
                                  rc4(x5231, x5232, x5233)
                                  )
                      )
                    )
        """
        def _layout(some_content):
            out = ''
            for con in some_content:
                if isinstance(con, tuple) or isinstance(con, list):
                    out += _layout(con)
                else:
                    out += con
            return out

        self.content = _layout(content)
        return self.content

    def page(self):
        """
        Define the page.  The subclass must define this method.

        The page method defines the page.  Example:

                def page(self):
                    xr1 = Text('This text comes from dpage.Text')
                    xr2 = Markdown('**Bold Markdown Text**')
                    xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                    self.layout(rc12(xr1, xr2, xr3))
                    return self
        """
        raise NotImplementedError("Subclasses should implement this!")

    def render(self):
        """
        Render this DPage.
        :return: response object
        :rtype: HttpResponse
        """
        # if there is a layout, use it to render
        if len(self.content) > 0:
            content = self.content
        else:
            content = self.render_objs()

        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT

        return render_to_response(self.template,
                                  {'content': content})

    def render_objs(self):
        """
        Render using the object list
        """
        # if whatever is in objs is iterable, iterate over the objects and render each according to whatever it is
        # otherwise, just render whatever it is
        content = ''
        if isinstance(self.objs, collections.Iterable):
            # noinspection PyTypeChecker
            for obj in self.objs:
                content += obj.render()
        elif self.objs:
            # noinspection PyUnresolvedReferences
            content += self.objs.render()
        return content


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
#         # page.layout(r(c3(x41), c9(x42)))
#         self.layout(rc12(x1),
#                     rc6(x21, x22),
#                     rc(x3),
#                     r(c3(x41), c9(r(x42))),
#                     r(c3(x51), c9(r(x521),
#                                   r(x522),
#                                   rc4(x5231, x5232, x5233)
#                                   )
#                       )
#                     )
#
########################################################################################################################


def c(*content, **kwargs):
    """
    :param content: Content to wrap in a column of width width
    :type content: object or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
    """
    width = kwargs.pop('width', 12)

    out = ''
    for con in content:
        if hasattr(con, 'render'):
            out += con.render()
        else:
            out += con
    out = dpage_col_before.format(width) + out + dpage_col_after
    return out

c1 = functools.partial(c, width=1)
c2 = functools.partial(c, width=2)
c3 = functools.partial(c, width=3)
c4 = functools.partial(c, width=4)
c5 = functools.partial(c, width=5)
c6 = functools.partial(c, width=6)
c7 = functools.partial(c, width=7)
c8 = functools.partial(c, width=8)
c9 = functools.partial(c, width=9)
c10 = functools.partial(c, width=10)
c11 = functools.partial(c, width=11)
c12 = functools.partial(c, width=12)


def r(*content):
    """
    Wrap content in a bootstrap 3 row
    :param content: The html content to wrap
    :type content: unicode
    """
    out = ''
    for con in content:
        if hasattr(con, 'render'):
            con_out = con.render()
        else:
            con_out = con
        out += con_out
    out = dpage_row_before + out + dpage_row_after
    return out


def rc(*content, **kwargs):
    """
    Wrap content in a row and column of width width.
    :param content: content
    :type content: unicode or collections.iterable
    :param kwargs: keyword args (width: bootstrap width int or unicode, ...)
    :type kwargs: dict
    """
    width = kwargs.pop('width', 12)
    out = ''
    for con in content:
        out += c(con, width=width)
    out = r(out)
    return out

rc1 = functools.partial(rc, width=1)
rc2 = functools.partial(rc, width=2)
rc3 = functools.partial(rc, width=3)
rc4 = functools.partial(rc, width=4)
rc5 = functools.partial(rc, width=5)
rc6 = functools.partial(rc, width=6)
rc7 = functools.partial(rc, width=7)
rc8 = functools.partial(rc, width=8)
rc9 = functools.partial(rc, width=9)
rc10 = functools.partial(rc, width=10)
rc11 = functools.partial(rc, width=11)
rc12 = functools.partial(rc, width=12)


########################################################################################################################
#
# Classes to add content to DPage. Classes that add content to a DPage should derive from CellBase and
# MUST provide a render method.
#
########################################################################################################################


class CellBase(object):
    """
    Base class for all cell objects
    """

    def __init__(self, **kwargs):
        """
        """
        return

    def render(self):
        """
        This method should return the HTML to render the object.
        """
        raise NotImplementedError("Subclasses should implement this!")


class Text(CellBase):
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

    def render(self):
        """
        Render the Text object
        """
        return self.text


class Markdown(CellBase):
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

    def render(self):
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


class HTML(CellBase):
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

    def render(self):
        """
        Render markdown text.

        :return: html version of markdown text
        :rtype: unicode
        """
        return self.htmltext


class Graph(CellBase):
    """
    DPage graph object class that uses Chartkick.
    """
    # noinspection PyShadowingBuiltins
    def __init__(self, graph_type, data,
                 options=None,
                 **kwargs):
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

    def render(self):
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


########################################################################################################################
#
# DjangoPage Content classes.
#
# These classes have a render method that returns HTML text appropriate to their type/content.
#
########################################################################################################################


########################################################################################################################

# This text is used as a wrapper for all DjangoPage graphs
GRAPH_BEFORE_HTML = """
<!-- Start of graph -->
<div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

GRAPH_AFTER_HTML = """
</div>
<!-- End of graph -->
"""

# This text is used as a wrapper for chartkick template tags
CHARTKICK_BEFORE_HTML = """
<!-- Start of chartkick graph -->
<div class="col-xs-12 col-sm-12 col-md-12 col-lg-12">
"""

CHARTKICK_AFTER_HTML = """
</div>
<!-- End of chartkick graph -->
"""

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']


def static_name_generator(base_name='x'):
    """
    Returns a unique name of the form base_name_counter
    :param base_name:
    """
    if not hasattr(static_name_generator, "counter"):
        static_name_generator.counter = 0  # it doesn't exist yet, so initialize it
    static_name_generator.counter += 1
    return '{}_{}'.format(base_name, static_name_generator.counter)


class XGraphCK(object):
    """
    Graph object class for Chartkick.  Class that actually holds the graph object definition.
    """
    # noinspection PyShadowingBuiltins
    def __init__(self, graph_type, data, options=None,
                 width=12,
                 min=None, max=None, height=None, library=None,
                 text_before=None, text_after=None):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode or list[dict] or dict
        :param options: 'with' options for the chartkick graph.
        :type options: unicode
        :param width: Bootstrap3 grid width for graph
        :type width: int
        :param min: Min data value
        :type min: int or float
        :param max: Max data value
        :type max: int or float
        :param height: string version of height, ex '500px'
        :type height: unicode
        :param library: highcharts library values, ex. [('title.text', 'graph title'),...]
        :type library: list[tuple] or tuple
        :param text_before: Markdown text to display before the graph.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graph.
        :type text_after: unicode
        """

        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))

        # todo 2: when this is working, remove the unneeded class attributes
        # todo 2: since all that's really needed is self.output
        self.graph_type = graph_type  # save type of graph
        self.data = data  # the data to display
        self.options = options  # chartkick with options
        self.width = width
        self.min = min
        self.max = max
        self.height = height
        self.library = library
        self.text_before = text_before  # markdown text to display before the graph
        self.text_after = text_after  # markdown text to display after the graph

        #
        #  Generate the html to render this graph with this data
        #

        # Generate the row for the graph within it's containing col
        output = GRAPH_BEFORE_HTML.replace('WIDTH', str(width))

        # Output text_before if there is any
        if text_before:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': xgraph_markdown(text_before)}))
            pass

        # create a context variable to hold the data if necessary
        # Note: because the expr is evaluated and then the value immediately used when the template is rendered
        # we do NOT need unique variables.
        if not isinstance(data, basestring):
            name = static_name_generator()
            output += '{{% expr {} as {} %}}'.format(data.__repr__(), name)
            data = name

        # Output the chartkick graph
        if options:
            chart = '{}_chart {} with {}'.format(graph_type, data, options)
            pass
        else:
            chart = '{}_chart {}'.format(graph_type, data)
            pass
        chart = '{% ' + chart + ' %}'
        chart = CHARTKICK_BEFORE_HTML + chart + CHARTKICK_AFTER_HTML
        # print '===', chart

        output += chart

        # Output text_after if there is any
        if text_after:
            output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': xgraph_markdown(text_after)}))

        output += GRAPH_AFTER_HTML
        self.output = output
        pass

    def render(self):
        """
        Render the graph
        """
        return self.output

    # noinspection PyShadowingBuiltins
    def options(self, min=None, max=None, height=None, library=None):
        """
        Set chartkick & highchart options
        :param min:
        :param max:
        :param height:
        :param library:
        """
        # fixme: finish options method for XGraphCK
        pass


########################################################################################################################


class XGraphHC(object):
    """
    Graph object class for Hichcharts.  Class that actually holds the graph object definition.
    """

    def __init__(self, graph_type, data, options=None,
                 width=12, text_before=None, text_after=None):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode
        :param options: 'with' options for the chartkick graph.
        :type options: unicode
        :param width: Bootstrap3 grid width for graph
        :type width: int
        :param text_before: Markdown text to display before the graph.
        :type text_before: unicode
        :param text_after: Markdown text to display after the graph.
        :type text_after: unicode
        """

        # if not graph_type in LEGAL_GRAPH_TYPES:
        #     raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        #
        # # todo 2: when this is working, remove the unneeded class attributes
        # # todo 2: since all that's really needed is self.output
        # self.graph_type = graph_type                    # save type of graph
        # self.data = data                                # the data to display
        # self.options = options                          # chartkick with options
        # self.width = width
        # self.text_before = text_before                  # markdown text to display before the graph
        # self.text_after = text_after                    # markdown text to display after the graph
        #
        # #
        # #  Generate the html to render this graph with this data
        # #
        #
        # # Generate the row for the graph within it's containing col
        # output = GRAPH_BEFORE_HTML.replace('WIDTH', str(width))
        #
        # # Output text_before if there is any
        # if text_before:
        #     output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': xgraph_markdown(text_before)}))
        #     pass
        #
        # # Output the chartkick graph
        # if options:
        #     chart = '{}_chart {} with {}'.format(graph_type, data, options)
        #     pass
        # else:
        #     chart = '{}_chart {}'.format(graph_type, data)
        #     pass
        # chart = '{% ' + chart + ' %}'
        # chart = CHARTKICK_BEFORE_HTML + chart + CHARTKICK_AFTER_HTML
        #
        # output += chart
        #
        # # Output text_after if there is any
        # if text_after:
        #     output += MARKDOWN_TEXT_TEMPLATE.render(Context({'markdown_text': xgraph_markdown(text_after)}))
        #
        # output += GRAPH_AFTER_HTML
        # self.output = output
        pass

    def render(self):
        """
        Render the graph
        """
        # return self.output
        pass


#############
#############
#############
#############
#############
#############
#############
