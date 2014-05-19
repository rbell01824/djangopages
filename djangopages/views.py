#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/7/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/7/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

from loremipsum import get_paragraph
import datetime
import qsstats

from django.views.generic import View
from django.db.models import Count
from django import forms

from djangopages.dpage import *

import django_tables2 as tables

from test_data.models import syslog_query, VNode, VCompany


########################################################################################################################
#
# Development test class based view
#
########################################################################################################################

class Test1(DPage):
    """
    Class based dpage with render method overridden.  Objs style interface.
    """

    def page(self, *args, **kwargs):
        """
        Actually create the page
        :param args:
        :param kwargs:
        """
        self.form = None
        self.content.append(Text('This text comes from dpage.Text'))
        self.content.append(Markdown('**Bold Markdown Text**'))
        self.content.append(HTML('<h3>H3 text from DPageHTML</h3>'))
        return self


class Test2(DPage):
    """
    Basic test of layout facility.
    """

    def page(self, *args, **kwargs):
        """
        Override
        :param args:
        :param kwargs:
        """
        xr1 = Text('This text comes from dpage.Text')
        # self.content = RC12(xr1)
        xr2 = Markdown('**Bold Markdown Text**')
        xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
        self.content = RC12(xr1, xr2, xr3)
        return self


class Test3(DPage):
    """
    Complex render test
    """
    def page(self, *args, **kwargs):
        """
        Override
        :param args:
        :param kwargs:
        """
        x1 = Text('Row 1: This text comes from dpage.Text')
        x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
        x22 = HTML('<p>Row 2 col 2: </p><h3>H3 text from DPageHTML</h3>')
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(get_paragraph()))
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(get_paragraph()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(get_paragraph()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(get_paragraph()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(get_paragraph()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(get_paragraph()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(get_paragraph()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(get_paragraph()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(get_paragraph()))
        # page.layout(R(C3(x41), C9(x42)))
        self.content = (R1C12(x1),
                        R1C6(x21, x22),
                        R1C(x3),
                        R(C3(x41), C9(R(x42))),
                        R(C3(x51), C9(R(x521),
                                      R(x522),
                                      R1C4(x5231, x5232, x5233)
                                      )
                          )
                        )
        return self


class Test4(DPage):
    """
    Basic test of Graph facility with two graphs in a row.
    """
    def page(self, *args, **kwargs):
        """
        Override
        :param args:
        :param kwargs:
        """
        # set the company and node since no form yet
        company = 'BMC_1'
        node = 'A0040CnBPGC1'

        # get the syslog data for this company/node
        qs = syslog_query(company, node)

        # Count all the syslog records
        all_count_host = qs.count()

        # Get count by type data
        xqs = qs.values('message_type').annotate(num_results=Count('id'))
        # Format for bar chart
        count_by_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        # Sort data for pie chart
        count_by_type_sorted_by_count = sorted(count_by_type, lambda x, y: cmp(x[1], y[1]), None, True)

        # create the column chart and set it's title
        col_graph = Graph('column', count_by_type)
        col_graph.options = {'height': '400px',
                             'title.text': 'Syslog records by type',
                             'subtitle.text': '{} node {}'.format(company, node)}

        # create the pie chart and set it's title
        pie_graph = Graph('pie', count_by_type_sorted_by_count)
        pie_graph.options = {'height': '400px',
                             'title.text': 'Syslog records by type',
                             'subtitle.text': '{} node {}'.format(company, node)}

        # put some explanation text above and below the charts
        text_top = Markdown('### Error count by type for {} Node {} '.format(company, node) +
                            'Total errors {}'.format(all_count_host))
        text_bottom = Markdown('### Analysis\n'
                               'Here is where the analysis can go.\n\n' +
                               '{}\n\n'.format(get_paragraph()) +
                               '{}\n\n'.format(get_paragraph()) +
                               '{}\n\n'.format(get_paragraph()))

        self.content = (R1C(text_top),
                        R1C6(col_graph, pie_graph),
                        R1C(text_bottom))
        return self


class Test5(DPage):
    """
    Multiple graphs on page with multiple kinds of graphs
    """
    def page(self, *args, **kwargs):
        """
        For specified company, display a summary report and details by node.
        :param args:
        :param kwargs:
        """
        self.company_summary('BMC_1')
        return self

    def company_summary(self, company):
        """
        For specified company, display a summary report and details by node.
        :param company: Company
        :return: DPage OBJECT!
        """
        # noinspection PyListCreation
        content = []
        content.append(self.all_hosts_summary(company))
        panels = []
        for host in self.get_hosts(company):
            panels.append(self.host_summary(company, host))
        content.append(Accordion(panels))
        self.content = content
        return self

    def all_hosts_summary(self, company):
        """
        Display bar chart of errors by type for all nodes and a line chart with 4 lines of
        errors by type vs time.
        :param company: Company
        :return: HTML
        """
        qs = syslog_query(company)
        errbt = self.time_chart(qs, company, 'All Nodes')
        cbt = self.message_type_graph(qs, company, 'All Nodes')
        cecbn = self.critical_event_graph(qs, company)
        eecbn = self.error_event_graph(qs, company)
        # noinspection PyRedundantParentheses
        return (R1C4(cbt, cecbn, eecbn), RC(errbt))

    def host_summary(self, company, node):
        """
        Create summary output for company
        :param company: Company
        :param node: node
        :return: HTML
        """
        qs = syslog_query(company, node)
        errbt = self.time_chart(qs, company, node)
        cbt = self.message_type_graph(qs, company, node)
        cbt.options['height'] = '400px'
        xxx = R(C4(cbt), C8(errbt))
        return AccordionMultiPanel(xxx, title='{}:{} Details'.format(company, node))

    # noinspection PyMethodMayBeStatic
    def message_type_graph(self, qs, company, node):
        """

        :param qs:
        :param company:
        :param node:
        :return: :rtype:
        """
        xqs = qs.values('message_type').annotate(num_results=Count('id'))
        count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        cbt = Graph('column', count_by_type_type)
        cbt.options = {'title.text': 'Syslog Messages by Type',
                       'subtitle.text': '{}:{}'.format(company, node)}
        return cbt

    # noinspection PyMethodMayBeStatic
    def critical_event_graph(self, qs, company):
        """
        Critical event by node, all nodes
        :param qs:
        :param company:
        """
        # critical event by node
        critical_event_count_by_node = map(list, qs.filter(message_type='critical').
                                           order_by('node__host_name').
                                           values('node__host_name').
                                           annotate(count=Count('node__host_name')).
                                           values_list('node__host_name', 'count'))
        cecbn = Graph('column', critical_event_count_by_node)
        cecbn.options = {'title.text': 'Critical Events by Host',
                         'subtitle.text': '{}:All Nodes'.format(company)}
        return cecbn

    # noinspection PyMethodMayBeStatic
    def error_event_graph(self, qs, company):
        """
        Error event by node all nodes
        :param qs:
        :param company:
        """
        # error event by node
        error_event_count_by_node = map(list, qs.filter(message_type='error').
                                        order_by('node__host_name').
                                        values('node__host_name').
                                        annotate(count=Count('node__host_name')).
                                        values_list('node__host_name', 'count'))
        eecbn = Graph('column', error_event_count_by_node)
        eecbn.options = {'title.text': 'Error Events by Host',
                         'subtitle.text': '{}:All Nodes'.format(company)}
        return eecbn

    @staticmethod
    def time_chart(qs, company, host):
        """
        Create basic time chart summary
        :param qs: Query set for company & host
        :param company: Company
        :param host: Host
        :return: graph OBJECT!
        """
        # total, critical, error events by time
        date_start = datetime.date(2012, 12, 1)
        date_end = datetime.date(2013, 2, 9)

        # setup the qss object & build time series
        qss = qsstats.QuerySetStats(qs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')

        # format for chartkick
        data_total = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        # get critical
        xqs = qs.filter(message_type='critical')
        qss = qsstats.QuerySetStats(xqs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')
        data_critical = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        # get error
        xqs = qs.filter(message_type='error')
        qss = qsstats.QuerySetStats(xqs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')
        data_error = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        # make the graph
        data = [{'name': 'All', 'data': data_total},
                {'name': 'Critical', 'data': data_critical},
                {'name': 'Error', 'data': data_error}]
        errbt = Graph('area', data)
        errbt.options = {'height': '440px',
                         'title.text': '{} Syslog Events By Hour'.format(company),
                         'subtitle.text': '{}:{}'.format(company, host)
                                          + ' - {} to {}'.format(date_start, date_end),
                         'plotOptions.area.stacking': 'normal'
                         }
        return errbt

    @staticmethod
    def get_hosts(company):
        """
        Get list of this companies hosts.
        :param company:
        """
        hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
        return hosts


class Test6(DPage):
    """
    Test accordion
    """
    def page(self, *args, **kwargs):
        """
        Create simple accordion page
        :param args:
        :param kwargs:
        """

        x1 = AccordionPanel(Text('This text comes from dpage.Text'), title='Row 1')
        # self.content = Accordion(x1)
        x2 = AccordionPanel(Markdown('**Bold Markdown Text**'), title='Row 2')
        x3 = AccordionPanel(HTML('<h3>H3 text from DPageHTML</h3>'), title='Row 3')
        self.content = Accordion(x1, x2, x3)
        return self


class Test7(DPage):
    """
    Test form support
    """
    def page(self, initial=None, *args, **kwargs):
        """
        Override
        :param initial:
        :param args:
        :param kwargs:
        """
        # noinspection PyDocstring
        class TestForm(forms.Form):
            message = forms.CharField()

        xrform = Form(self, TestForm, 'Update the display', initial=initial, action_url='/dpages/test7')
        xr1 = Markdown('# Test of form support\n\n'
                       'Here is the form')
        xr2 = Markdown('\n\nThe form message is **{}**\n\n'.format(initial['message']))
        xr3 = Markdown('\n\n**After the form**\n\n'
                       'Graphs, tables, and other stuff go here')
        xr4 = HTML('<a class="btn btn-success form-control" href="/">Done playing.</a>')
        self.content = (R1C12(xr1), R1C4(xrform), RC12(xr2, xr3), R1C3(xr4))
        return self


class Test8(DPage):
    """
    Test form support
    """
    def page(self, initial=None, *args, **kwargs):
        """
        Override
        :param initial:
        :param args:
        :param kwargs:
        """

        # Title for the page
        xr1 = Markdown('# Test of table support\n\n')

        # Node: create title, get queryset, create the table
        node_tit = Markdown('## Node table')
        node_qs = VNode.objects.all()
        node_tbl = Table(self, node_qs)

        # Company: create title, get queryset, create the table
        company_tit = Markdown('## Company table')
        company_qs = VCompany.objects.all()
        company_tbl = Table(self, company_qs)

        # Some stuff after the page
        xr3 = Markdown('\n\n**After the table**\n\n')

        # Define the content layout
        self.content = (RC(xr1),
                        R(C2(node_tit, company_tbl),
                          C6(node_tit, node_tbl)),
                        RC(xr3))
        # self.content = t_node
        return self


class DevTestView(View):
    """
    View class for dev testing.
    """
    test = 'test1'
    testmap = {'test1': Test1,
               'test2': Test2,
               'test3': Test3,
               'test4': Test4,
               'test5': Test5,
               'test6': Test6,
               'test7': Test7,
               'test8': Test8,
               }

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
        Execute the graph method and display the results.
        :param request:
        """
        dt = self.testmap[self.test]
        dpage = dt(request).page({'message': 'Enter your message here.'})
        return dpage.render()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, *args, **kwargs):
        """
        Send the post data to the page and rerender.
        :param request:
        :param args:
        :param kwargs:
        """
        dt = self.testmap[self.test]
        dpage = dt(request).page(request.POST)
        return dpage.render()

