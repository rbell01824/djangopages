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

from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template import add_to_builtins
from django.utils.encoding import force_unicode
from django.template import Template, Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

from taggit.models import TaggedItem

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
        self.form = form
        if objs:
            self.objs = objs                    # graph objects in this cell
        self.width = width                      # width of this column
        pass

    def render(self):
        """
        Render this DPage.
        :return: response object
        :rtype: HttpResponse
        """
        content = ''

        # if whatever is in objs is iterable, iterate over the objects and render each according to whatever it is
        # otherwise, just render whatever it is
        if isinstance(self.objs, collections.Iterable):
            # noinspection PyTypeChecker
            for obj in self.objs:
                content += obj.render()
        elif self.objs:
            # noinspection PyUnresolvedReferences
            content += self.objs.render()

        t = loader.get_template(self.template)
        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT
        c = Context({'content': content})

        return render_to_response(self.template,
                                  {'content': content})

########################################################################################################################
#
# DPageText, ... classes to add content to DPage
#
########################################################################################################################


class DPageText(object):
    """
    Holds text for inclusion in a DPage.
    """
    def __init__(self, text):
        self.text = text
        return

    def render(self):
        """
        Return render text for the DPageText object.
        """
        return self.text


class DPageMarkdown(object):
    """
    Holds markdown text for inclusion in a DPage.
    """
    def __init__(self, markdowntext, extensions=None):
        """
        Create a DPageMarkdown object and initialize it.

        :param markdowntext: Text to process as markdown.
        :type markdowntext: unicode
        :param extensions: Optional markdown options string.  See python markdown documentation.
        :type extensions: unicode or None
        """
        self.extensions = extensions
        self.markdowntext = markdowntext
        # todo: here check text type and deal with file like objects and queryset objects
        # for now just deal with actual text
        pass

    def render(self):
        """
        Render markdown text.

        :return: html version of markdown text
        :rtype: unicode
        """
        return markdown.markdown(force_unicode(self.markdowntext),
                                 self.extensions if self.extensions else '',
                                 output_format='html5',
                                 safe_mode=False,
                                 enable_attributes=False)


class DPageHTML(object):
    """
    Holds HTML text for inclusion in a DPage.  This is a convenience method since DPageMarkdown can be
    used interchangeably.
    """
    def __init__(self, htmltext):
        """
        Create a DPageHTML object and initialize it.

        :param htmltext: Text to process as markdown.
        :type htmltext: unicode
        """
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

########################################################################################################################
#
# DjangoPage Grid classes
#
########################################################################################################################


class DjangoPageGrid(object):
    """
    Base class for the DjangoPage... classes.  The DjangoPage... classes really only provide some
    syntactic sugar for users. This class actually does the heavy lifting.  It contains a list of other
    DjangoPage... objects (Markdown/Graph/Table/..., Row/Column, ...).  Any DjangoPage
    child class that has a render method can be in this list and will be rendered as part of the
    DjangoPage.
    """

    def __init__(self, before_html, after_html, objs=None, width=12):
        """
        Initialize the DjangoPageGrid.

        :param before_html: HTML to output before this cell
        :type before_html: unicode
        :param after_html: HTML to output after this cell
        :type after_html: unicode
        :param objs: The object(s) in this graph.
        :type objs: list or DjangoPageGrid or DjangoPagePage or DjangoPageRow or DjangoPageColumn or object or ...
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        """
        self.before_html = before_html
        self.after_html = after_html
        self.objs = []
        if objs:
            self.objs = objs                    # graph objects in this cell
        self.width = width                      # width of this column
        pass

    def render(self):
        """
        Generate the html for this DjangoPage Object.  Subclass may override this method.
        """
        output = self.before_html

        # if whatever is in objs is iterable, iterate over the objects and render each according to whatever it is
        # otherwise, just render whatever it is
        if isinstance(self.objs, collections.Iterable):
            # noinspection PyTypeChecker
            for obj in self.objs:
                output += obj.render()
        else:
            # noinspection PyUnresolvedReferences
            output += self.objs.render()

        output += self.after_html
        return output

########################################################################################################################

# This text is used as a wrapper for a graphpage
DJANGOPAGE_BEFORE_HTML = """
<!-- Start of graphpage -->
<div class="container-fluid">
    <div class="row">
        <div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

DJANGOPAGE_AFTER_HTML = """
        </div>
    </div>
</div>
<!-- End of graphpage -->
"""


class DjangoPagePage(DjangoPageGrid):
    """
    DjangoPagePage class that supports a grid like collection of DjangoPage objects.  Semantically,
    this represents a collection of rows of columns of graphs on a page.

    row_________________________________________________________________________________________________
    col________________________ col__________________________ col_______________________________________
    graph______________________ graph________________________ graph_____________________________________
    graph______________________ graph________________________ graph_____________________________________
    graph______________________                               graph_____________________________________
    graph______________________                               graph_____________________________________
    graph______________________
    graph______________________
    row_____________________________________________________________________
    col__________________________ col_______________________________________
    graph________________________ graph_____________________________________

    Columns need not hold the same number of DjangoPage objects!
    """

    def __init__(self, objs=None, width=12):
        """
        Initialize DjangoPagePage.

        :param objs: The object(s) in this graph.
        :type objs: list, XGraphRow, XGraphColumn, XGraph
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        """
        super(DjangoPagePage, self).__init__(DJANGOPAGE_BEFORE_HTML.replace('WIDTH', str(width)),
                                             DJANGOPAGE_AFTER_HTML,
                                             objs, width)
        pass

########################################################################################################################

# This text is used as a wrapper for a graphpage row
DJANGOPAGE_ROW_BEFORE_HTML = """
<!-- Start of graphpage row -->
<div class="container-fluid">
    <div class="row">
        <div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

DJANGOPAGE_ROW_AFTER_HTML = """
        </div>
    </div>
</div>
<!-- End of graphpage row -->
"""


class DjangoPageRow(DjangoPageGrid):
    """
    DjangoPage row class.  Semantically this holds a list of columns of objects in a row..
    """

    def __init__(self, objs=None, width=12):
        """
        Initialize DjangoPageRow.

        :param objs: The object(s) in this graph.
        :type objs: list, DjangoPageRow, DjangoPageColumn, DjangoPageGraph
        :param width: width of cell (Bootstrap3 width, 1 - 12)
        :type width: int
        """
        super(DjangoPageRow, self).__init__(DJANGOPAGE_ROW_BEFORE_HTML.replace('WIDTH', str(width)),
                                            DJANGOPAGE_ROW_AFTER_HTML,
                                            objs, width)
        pass


########################################################################################################################

# This text is used as a wrapper for a graphpage column
DJANGOPAGE_COLUMN_BEFORE_HTML = """
<!-- Start of graphpage column -->
<div class="col-xs-WIDTH col-sm-WIDTH col-md-WIDTH col-lg-WIDTH">
"""

DJANGOPAGE_COLUMN_AFTER_HTML = """
</div>
<!-- End of graphpage column -->
"""


class DjangoPageColumn(DjangoPageGrid):
    """
    Graph column class.  Semantically this holds a list of graphs in a column in a row.
    """
    def __init__(self, objs=None, width=12):
        """
        Create graph column object to hold objects in this column

        :param objs: List of Graph objects in this column.
        :type objs: list, XGraph
        :param width: width of column
        :type width: int
        """
        super(DjangoPageColumn, self).__init__(DJANGOPAGE_COLUMN_BEFORE_HTML.replace('WIDTH', str(width)),
                                               DJANGOPAGE_COLUMN_AFTER_HTML,
                                               objs, width)
        pass


########################################################################################################################
#
# DjangoPage Content classes.
#
# These classes have a render method that returns HTML text appropriate to their type/content.
#
########################################################################################################################


class DjangoPageMarkdown(object):
    """
    Class to hold and render markdown text.
    """
    def __init__(self, text, extensions=None):
        """
        Create a DjangoPageMarkdown object and initialize it.

        :param text: Text to process as markdown.
        :type text: unicode
        :param extensions: Optional markdown options string.  See python markdown documentation.
        :type extensions: unicode or None
        """
        self.extensions = extensions
        self.text = text
        # todo: here check text type and deal with file like objects and queryset objects
        # for now just deal with actual text
        pass

    def render(self):
        """
        Render markdown text.

        :return: html version of markdown text
        :rtype: unicode
        """
        return markdown.markdown(force_unicode(self.text),
                                 self.extensions if self.extensions else '',
                                 output_format='html5',
                                 safe_mode=False,
                                 enable_attributes=False)


class DjangoPageText(DjangoPageMarkdown):
    """
    Ma
    """
    # fixme: finish this
    def __init__(self, text):
        super(DjangoPageText, self).__init__(text)


class DjangoPageHTML(DjangoPageMarkdown):
    """
    Ma
    """
    # fixme: finish this
    def __init__(self, text):
        super(DjangoPageHTML, self).__init__(text)

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
        self.graph_type = graph_type                    # save type of graph
        self.data = data                                # the data to display
        self.options = options                          # chartkick with options
        self.width = width
        self.min = min
        self.max = max
        self.height = height
        self.library = library
        self.text_before = text_before                  # markdown text to display before the graph
        self.text_after = text_after                    # markdown text to display after the graph

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


########################################################################################################################
#
# Force load of template tags that are generally needed by graphpages
#
# This is important: If the function is called early, and some of the custom
# template tags use superclasses of django template tags, or otherwise cause
# the following situation to happen, it is possible that circular imports
# cause problems:
#
# If any of those superclasses import django.template.loader (for example,
# django.template.loader_tags does this), it will immediately try to register
# some builtins, possibly including some of the superclasses the custom template
# uses. This will then fail because the importing of the modules that contain
# those classes is already in progress (but not yet complete), which means that
# usually the module's register object does not yet exist.
#
# In other words:
#       {custom-templatetag-module} ->
#       {django-templatetag-module} ->
#       django.template.loader ->
#           add_to_builtins(django-templatetag-module)
#           <-- django-templatetag-module.register does not yet exist
#
# It is therefor imperative that django.template.loader gets imported *before*
# any of the templatetags it registers.
#
########################################################################################################################


def load_templatetags():
    """
    Load custom template tags so they are always available.  See https://djangosnippets.org/snippets/342/.

    In your settings file:

    TEMPLATE_TAGS = ( "djutils.templatetags.sqldebug", )

    Make sure load_templatetags() gets called somewhere, for example in your apps init.py
    """

    #
    # Note: For reasons I don't understand this code gets ececuted twice when
    # Django starts.  Nothing bad seems to happen so I'll use the technique.
    # print '=== in utilities init ==='

    #
    # Register the template tag as <application>.templatetags.<template tag lib>
    #
    try:
        for lib in settings.TEMPLATE_TAGS:
            add_to_builtins(lib)
    except AttributeError:
        pass

########################################################################################################################
#
# Taggit List filter for admin
#
########################################################################################################################


class TaggitListFilter(SimpleListFilter):
    """
    A custom filter class that can be used to filter by taggit tags in the admin.

    code from https://djangosnippets.org/snippets/2807/
    """

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('tags')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        :param model_admin:
        :param request:
        """
        list = []
        tags = TaggedItem.tags_for(model_admin.model)
        for tag in tags:
            list.append((tag.name, _(tag.name)), )
        return list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query
        string and retrievable via `self.value()`.
        :param queryset:
        :param request:
        """
        if self.value():
            return queryset.filter(tags__name__in=[self.value()])
