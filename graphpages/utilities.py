#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/31/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/31/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

import markdown
import collections

from django.conf import settings
from django.template import add_to_builtins
from django.template.loader import render_to_string
from django.template import Context, Template
from django.utils.encoding import force_unicode

# fixme: finish syslog cruft.  add iterator on nodes.  add the last 2 things JZ did, build as a method
# todo 1: add title and stacked to xgraph it will need to be type sensitive
# todo 1: add collapse bootstrap to elements as an option see http://getbootstrap.com/javascript/#collapse
# todo 1: add button group with links to elements as an option
# todo 1: add smart table in xgraph stack as xtable see
# todo 1: Internal APIs — django-tables2 0.16.0.dev documentation:
# todo 1: export using jquery http://jsfiddle.net/terryyounghk/KPEGU/
# todo 1: http://www.kunalbabre.com/projects/table2CSV.php  use this one
# todo 1: http://stackoverflow.com/questions/4639372/export-to-csv-in-jquery/7588465#7588465
# todo 1: django-tables2 - An app for creating HTML tables — django-tables2 0.16.0.dev documentation:
# todo 1: http://elsdoerfer.name/docs/django-tables/
# todo 1: add syslog example with form for selecting node and dt range


########################################################################################################################
#
# The following classes define the XGraph... methods used to support graphpages
#
########################################################################################################################

########################################################################################################################

# This text is used as a wrapper for a graphpage graph
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

########################################################################################################################
#
# Utility support functions
#
########################################################################################################################


def xgraph_nested_set(dic, key, value):
    """
    Set value in nested dictionary.

    :param dic: dictionary where value needs to be set
    :type dic: dict
    :param key: a.b.c key into dic
    :type key: unicode
    :param value:
    :type value: varies
    :return: dictionary with value set for specified key
    :rtype: dict
    """
    keys = key.split('.')
    xdic = dic
    for k in keys[:-1]:
        xdic = xdic.setdefault(k, {})
    xdic[keys[-1]] = value
    return dic


def xgraphck_multiple_series(list_of_dicts, name, data_label, data_value):
    """
    Turn a list of dictionaries into a 'multiple series list suitable for chartkick.

        Turn this:

            [{'num_results': 26, 'node__host_name': u'A0040CnBEPC1', 'message_type': u'critical'},
             {'num_results': 69, 'node__host_name': u'A0040CnBEPC2', 'message_type': u'critical'},
            ...
             {'num_results': 8, 'node__host_name': u'A0040CnBEPC2', 'message_type': u'warning'},
             {'num_results': 3170, 'node__host_name': u'A0040CnBPGC1', 'message_type': u'warning'}]

        into this:

            [{'data': [['A0040CnBEPC1', 26], ['A0040CnBEPC2', 69]], 'name': 'critical'},
            ...
             {'data': [['A0040CnBEPC2', 8], ['A0040CnBPGC1', 3170]], 'name': 'warning'}]

    :param list_of_dicts: List of dictionary entries to process
    :type list_of_dicts: list of dict
    :param name: dictionary name for the name field
    :type name: unicode
    :param data_label: dictionary name for the data label field
    :type data_label: unicode
    :param data_value: dictionary name for the data value field
    :type data_value: unicode
    :return: List of dictionary entries suitable for chartkick multiple series
    :rtype: list of dict
    """
    names = list(set([x[name] for x in list_of_dicts]))
    data = []
    for a_name in names:
        z = {'name': a_name, 'data': [[x[data_label], x[data_value]] for x in list_of_dicts if x[name] == a_name]}
        data.append(z)
    return data
