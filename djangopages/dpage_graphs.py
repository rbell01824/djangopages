#!/usr/bin/env python
# coding=utf-8

"""
Graph Widgets
=============

.. module:: dpage_graphs
   :synopsis: Provides DjangoPage widgets to create chartkick graphs

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create various chartkick graphs.

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


from django.template import Context, Template

from djangopages.libs import dict_nested_set
from djangopages.dpage import DWidget, unique_name

########################################################################################################################
#
# Graph routines
#
########################################################################################################################

LEGAL_GRAPH_TYPES = ['line', 'pie', 'column', 'bar', 'area']

# todo 1: add data links, see http://stackoverflow.com/questions/19399346/need-to-link-url-in-highchart
# todo 1: http://birdchan.com/home/2012/09/07/highcharts-pie-charts-can-have-url-links/comment-page-1/


class GraphCK(DWidget):
    """ Chartkick widget

    .. sourcecode:: python

        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        line_graph = GraphCK('line', exchange, options={'height': '400px',
                                                        'title.text': 'Exchange Rates Chart',
                                                        'subtitle.text': 'Graphs may have subtitles'})
        multi_line_graph = GraphCK('line', temperature, options={'height': '400px',
                                                                 'title.text': 'Temperature Chart',
                                                                 'subtitle.text': 'Tokyo/London/NY/Berlin'})
        area_graph = GraphCK('area', areas, options={'height': '400px',
                                                     'title.text': 'Areas Chart',
                                                     'subtitle.text': 'Graphs may have subtitles'})

    .. note:: see the example page for details on how to setup data
    """
    template = '{{% {chart} %}}'

    # noinspection PyShadowingBuiltins
    def __init__(self, graph_type, data, options='', **kwargs):
        """ Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode or list[dict] or list[list] or dict
        :param options: 'with' options for the chartkick graph.
        :type options: dict
        :param kwargs: RFU
        :type kwargs: dict
        """
        if not graph_type in LEGAL_GRAPH_TYPES:
            raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        super(GraphCK, self).__init__((graph_type, data, options,), kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        # log.debug('+++++ in Graph generate')
        # log.debug('      template <<{}>>'.format(template))
        # log.debug('      content <<{}>>'.format(content))
        # log.debug('      classes <<{}>>'.format(classes))
        # log.debug('      style <<{}>>'.format(style))
        # log.debug('      kwargs <<{}>>'.format(kwargs))
        gtype, data, options = content[0:3]
        # log.debug('      gtype <<{}>>'.format(gtype))
        # log.debug('      data <<{}>>'.format(data))
        # log.debug('      options <<{}>>'.format(options))
        if options:
            options = self.set_options(options)
            chart = '{gtype}_chart data with {options}'.format(gtype=gtype, options=options)
            pass
        else:
            chart = '{gtype}_chart data'.format(gtype=gtype)
            pass
        out_chart = template.format(chart=chart)
        t = Template('{% load chartkick %}' + out_chart)
        c = Context({'data': data})
        out = t.render(c)
        # log.debug('+++++ out <<{}>>'.format(out))
        return out

    def set_options(self, options):
        """
        Set chartkick & highchart options
            options = "height='500px' library=" + str(library)

        """
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
