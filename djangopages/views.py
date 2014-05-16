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
import datetime, qsstats

from django.views.generic import View
from django.views.generic import ListView
from django.db.models import Count

from djangopages.dpage import *

from test_data.models import syslog_query, VNode


########################################################################################################################
#
# Development test class based view
#
########################################################################################################################


class DevTest0(DPage):
    """
    Example of class based dpage
    """
    pass


class DevTest1(DPage):
    """
    Class based dpage with render method overridden.  Objs style interface.
    """

    def page(self):
        """
        Actually create the page
        """
        self.form = None
        self.content.append(Text('This text comes from dpage.Text'))
        self.content.append(Markdown('**Bold Markdown Text**'))
        self.content.append(HTML('<h3>H3 text from DPageHTML</h3>'))
        return self


class DevTest2(DPage):
    """
    Basic test of layout facility.
    """

    def page(self):
        """
        Override
        """
        xr1 = Text('This text comes from dpage.Text')
        xr2 = Markdown('**Bold Markdown Text**')
        xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
        self.content = RC12(xr1, xr2, xr3)
        return self


class DevTest3(DPage):
    """
    Complex render test
    """
    def page(self):
        """
        Override
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
        self.content = (RC12(x1),
                        RC6(x21, x22),
                        RC(x3),
                        R(C3(x41), C9(R(x42))),
                        R(C3(x51), C9(R(x521),
                                      R(x522),
                                      RC4(x5231, x5232, x5233)
                                      )
                          )
                        )
        return self


class DevTest4(DPage):
    """
    Basic test of Graph facility with two graphs in a row.
    """
    def page(self):
        """
        Override
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

        self.content = (RC(text_top),
                        RC6(col_graph, pie_graph),
                        RC(text_bottom))
        return self


class DevTest5(DPage):
    """
    Multiple graphs on page with multiple kinds of graphs
    """
    def page(self):
        """
        For specified company, display a summary report and details by node.
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
        for host in DevTest5.get_hosts(company):
            content.append(self.host_summary(company, host))
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
        return self.do_summary(qs, company, 'All Hosts')

    def host_summary(self, company, host):
        """
        Create summary output for company
        :param company: Company
        :param host: Host
        :return: HTML
        """
        qs = syslog_query(company, host)
        return self.do_summary(qs, company, host)

    def do_summary(self, qs, company, host):
        """
        Do summary for a single host for the company
        :param qs: Queryset for this company & host
        :param company: Company
        :param host: Host
        :return: HTML
        """
        xqs = qs.values('message_type').annotate(num_results=Count('id'))
        count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        cbt = Graph('column', count_by_type_type)
        cbt.options = {'title.text': 'Syslog Messages by Type',
                       'subtitle.text': '{}:{}'.format(company, host)}

        # make the time chart
        errbt = self.time_chart(qs, company, host)

        # check just a node
        if host != 'All Hosts':
            cbt.options['height'] = '400px'
            xxx = R(C4(cbt), C8(errbt))
            return Panel(xxx, title='{}:{}'.format(company, host))

        # all nodes so make critical and error events by node
        # critical event by node
        critical_event_count_by_node = map(list, qs.filter(message_type='critical').
                                       order_by('node__host_name').
                                       values('node__host_name').
                                       annotate(count=Count('node__host_name')).
                                       values_list('node__host_name', 'count'))
        cecbn = Graph('column', critical_event_count_by_node)
        cecbn.options = {'title.text': 'Critical Events by Host',
                         'subtitle.text': '{}:{}'.format(company, host)}

        # error event by node
        error_event_count_by_node = map(list, qs.filter(message_type='error').
                                    order_by('node__host_name').
                                    values('node__host_name').
                                    annotate(count=Count('node__host_name')).
                                    values_list('node__host_name', 'count'))
        eecbn = Graph('column', error_event_count_by_node)
        eecbn.options = {'title.text': 'Error Events by Host',
                         'subtitle.text': '{}:{}'.format(company, host)}

        return (RC4(cbt, cecbn, eecbn), RC(errbt))

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


class DevTestView(View):
    """
    View class for dev testing.
    """
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
        Execute the graph method and display the results.
        :param request:
        """
        return DevTest5().page().render()

