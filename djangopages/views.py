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


def devtest():
    """
    Example of programmatic dpage.
    """
    # test layout facility
    page = DPage()
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
    # page.layout(r(c3(x41), c9(x42)))
    page.layout(rc12(x1),
                rc6(x21, x22),
                rc(x3),
                r(c3(x41), c9(r(x42))),
                r(c3(x51), c9(r(x521),
                              r(x522),
                              rc4(x5231, x5232, x5233))))
    return page.render()


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
        self.objs.append(Text('This text comes from dpage.Text'))
        self.objs.append(Markdown('**Bold Markdown Text**'))
        self.objs.append(HTML('<h3>H3 text from DPageHTML</h3>'))
        self.content = self.render_objs()
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
        self.layout(rc12(xr1, xr2, xr3))
        return self


class DevTest3(DPage):
    """
    Complex render test
    """
    # fixme: use render to actually render and add base method for building page
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
        # page.layout(r(c3(x41), c9(x42)))
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

        self.layout(rc(text_top),
                    rc6(col_graph, pie_graph),
                    rc(text_bottom))
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
        """
        content = []
        content.append(self.all_hosts_summary())
        for host in DevTest5.get_hosts(company):
            content.append(self.host_summary(host))
        self.layout(content)
        return self

    def all_hosts_summary(self):
        """
        """
        return rc(Text('Row 1'))

    def host_summary(self, host):
        """
        """
        return rc(Text('Company {}'.format(host)))

    @staticmethod
    def get_hosts(company):
        """
        Get list of this companies hosts.
        """
        hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
        return hosts

        # qs = syslog_query(company)
        # all_count = qs.count()
        #
        # # Count critical events
        # critical_event_count = map(list, qs.filter(message_type='critical').
        #                            order_by('node__host_name').
        #                            values('node__host_name').
        #                            annotate(count=Count('node__host_name')).
        #                            values_list('node__host_name', 'count'))
        # critical_event_count_title = '<h3>Critical Event Count by Host</h3>'
        # graph31 = XGraphCK('column', 'critical_event_count',
        #                    width=3,
        #                    text_before=critical_event_count_title)
        # graph32 = XGraphCK('pie', 'critical_event_count',
        #                    width=3,
        #                    text_before=critical_event_count_title)
        # error_event_count = map(list, qs.filter(message_type='error').
        #                         order_by('node__host_name').
        #                         values('node__host_name').
        #                         annotate(count=Count('node__host_name')).
        #                         values_list('node__host_name', 'count'))
        # error_event_count_title = '<h3>Error Event Count by Host</h3>'
        # graph33 = XGraphCK('column', 'error_event_count',
        #                    width=3,
        #                    text_before=error_event_count_title)
        # graph34 = XGraphCK('pie', 'error_event_count',
        #                    width=3,
        #                    text_before=error_event_count_title)
        # text_before = '<h3>{{company}} All Hosts, Total Syslog Records: {{all_count}}</h3>'
        # graphpage.objs.append(XGraphRow([graph31, graph32, graph33, graph34], text_before=text_before))


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

