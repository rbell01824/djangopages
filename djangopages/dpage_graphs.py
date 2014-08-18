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


from copy import copy

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


class Graph(DWidget):
    """
    DPage graph object class that uses Chartkick.
    """
    template = ''

    # noinspection PyShadowingBuiltins
    def __init__(self, graph_type, data, options=None, **kwargs):
        """
        Create a graph object

        :param graph_type: The type of this graph.  Must be line, pie, column, bar, or area.
        :type graph_type: unicode
        :param data: The name of the context variable holding the graph's data
        :type data: unicode or list[dict] or list[list] or dict
        :param options: 'with' options for the chartkick graph.
        :type options: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        # if not graph_type in LEGAL_GRAPH_TYPES:
        #     raise ValueError('In Graph illegal graph type {}'.format(graph_type))
        log.debug('.....graph def begin')
        super(Graph, self).__init__((graph_type, data, options,), kwargs)
        log.debug('.....graph def end')
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        log.debug('+++++ in Graph generate')
        log.debug('+++++ template <<{}>>'.format(template))
        log.debug( '+++++ content <<{}>>'.format(content))
        log.debug( '+++++ classes <<{}>>'.format(classes))
        log.debug( '+++++ style <<{}>>'.format(style))
        log.debug( '+++++ kwargs <<{}>>'.format(kwargs))
        return 'hi dude'


    # # noinspection PyUnusedLocal
    # def render(self, **kwargs):
    #     """
    #     Render the graph
    #     """
    #     # Generate the chartkick graph template text
    #     data = self.data
    #     if self.options:
    #         options = self.set_options()
    #         chart = '{}_chart data with {}'.format(self.graph_type, options)
    #         pass
    #     else:
    #         chart = '{}_chart data'.format(self.graph_type)
    #         pass
    #     t = Template('{% load chartkick %} {% ' + chart + ' %}')
    #
    #     # render
    #     output = t.render(Context({'data': data}))
    #
    #     return output

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
