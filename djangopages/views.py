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

from test_data.models import syslog_query, syslog_companies, syslog_hosts,\
    syslog_event_graph, \
    VNode, VCompany


########################################################################################################################
#
# Development test class based view
#
########################################################################################################################

class Test1(DPage):
    """
    Class based dpage with render method overridden.  Objs style interface.
    """
    title = 'DjangoPages_Test1'
    description = 'Demonstrate basic text widgets'
    tags = []

    def page(self):
        """
        Actually create the page
        """
        ###################
        # Put some content on the page
        ###################
        self.content.append(Text('This text comes from dpage.Text.', ' So does this'))
        self.content.append(Markdown('#Header markdown text', '**Bold Markdown Text**'))
        self.content.append(HTML('<h3>H3 text from DPageHTML</h3>',
                                 '<strong>Strong text from HTML content</strong>'))
        return self


class Test2(DPage):
    """
    Basic test of layout facility.
    """
    title = 'DjangoPages_Test2'
    description = 'Demonstrate row/column layout of text objects'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Create some page content
        ###################
        xr1 = HTML('<h3>Text on row 1</h3>')
        xr2 = Markdown('**Text on row 2**')
        xr3 = Text('Text on row 3', Button('a button'), 'Some more text in row 3')
        ###################
        # Layout the content on the page
        ###################
        self.content = (RC12(xr1, xr2), RC(xr3),)
        return self


class Test3(DPage):
    """
    Complex render test
    """
    title = 'DjangoPages_Test3'
    description = 'Demonstrate complex row/column layout'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Create some page content
        ###################
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
        ###################
        # Layout the content on the page
        #
        # This layout generates roughly 200 lines of Bootstrap 3 html!
        ###################
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
    title = 'DjangoPages_Test4'
    description = 'Demonstrate DB driven graphs with highcharts customization'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Get the DB data we need
        ###################

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

        ###################
        # Create the charts
        ###################
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
        ###################
        # Create title and other page content
        ###################
        # put some explanation text above and below the charts
        text_top = Markdown('### Error count by type for {} Node {} '.format(company, node) +
                            'Total errors {}'.format(all_count_host))
        text_bottom = Markdown('### Analysis\n'
                               'Here is where the analysis can go.\n\n' +
                               '{}\n\n'.format(get_paragraph()) +
                               '{}\n\n'.format(get_paragraph()) +
                               '{}\n\n'.format(get_paragraph()))
        ###################
        # Layout the content on the page
        ###################
        self.content = (R1C(text_top),
                        R1C6(col_graph, pie_graph),
                        R1C(text_bottom))
        return self


class Test5(DPage):
    """
    Multiple graphs on page with multiple kinds of graphs
    """
    title = 'DjangoPages_Test5'
    description = 'Demonstrate syslog graphs and multi-panels'
    tags = []

    def page(self):
        """
        For specified company, display a summary report and details by node.
        """
        ###################
        # Create summary for company
        ###################
        self.company_summary('BMC_1')
        return self

    def company_summary(self, company):
        """
        For specified company, display a summary report and details by node.
        :param company: Company
        :return: DPage OBJECT!
        """
        ###################
        # Use methods to build content
        ###################
        # noinspection PyListCreation
        content = []
        content.append(self.all_hosts_summary(company))
        panels = []
        ###################
        # Iterate over hosts and build content for each one
        ###################
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
        ###################
        # Get data from DB
        ###################
        qs = syslog_query(company)
        ###################
        # Build the graphs we want on the page
        ###################
        errbt = self.time_chart(qs, company, 'All Nodes')
        cbt = self.message_type_graph(qs, company, 'All Nodes')
        cecbn = self.critical_event_graph(qs, company)
        eecbn = self.error_event_graph(qs, company)
        ###################
        # Layout the content on the page
        ###################
        return (R1C4(cbt, cecbn, eecbn), RC(errbt),)

    def host_summary(self, company, node):
        """
        Create summary output for company
        :param company: Company
        :param node: node
        :return: HTML
        """
        ###################
        # Get the DB data
        ###################
        qs = syslog_query(company, node)
        ###################
        # Make the charts we want
        ###################
        errbt = self.time_chart(qs, company, node)
        cbt = self.message_type_graph(qs, company, node)
        cbt.options['height'] = '400px'
        ###################
        # Layout the content on the page
        ###################
        xxx = R(C4(cbt), C8(errbt))
        ###################
        # Put the layout in an accordion multi panel
        ###################
        return AccordionMultiPanel(xxx, title='{}:{} Details'.format(company, node))

    # noinspection PyMethodMayBeStatic
    def message_type_graph(self, qs, company, node):
        """

        :param qs:
        :param company:
        :param node:
        :return: :rtype:
        """
        ###################
        # Get DB data we want on graph
        ###################
        xqs = qs.values('message_type').annotate(num_results=Count('id'))
        count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
        ###################
        # Create the graph
        ###################
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
        ###################
        # Get DB data we want on graph
        ###################
        # critical event by node
        critical_event_count_by_node = map(list, qs.filter(message_type='critical').
                                           order_by('node__host_name').
                                           values('node__host_name').
                                           annotate(count=Count('node__host_name')).
                                           values_list('node__host_name', 'count'))
        ###################
        # Create the graph
        ###################
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
        ###################
        # Get DB data we want on graph
        ###################
        # error event by node
        error_event_count_by_node = map(list, qs.filter(message_type='error').
                                        order_by('node__host_name').
                                        values('node__host_name').
                                        annotate(count=Count('node__host_name')).
                                        values_list('node__host_name', 'count'))
        ###################
        # Create the graph
        ###################
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
        ###################
        # Get the graph data together
        ###################
        # total, critical, error events by time
        date_start = datetime.date(2012, 12, 1)
        date_end = datetime.date(2013, 2, 9)

        # setup the qss object & build time series
        qss = qsstats.QuerySetStats(qs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')

        # format for chartkick
        data_total = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        ###################
        # Get data from DB
        ###################
        # get critical
        xqs = qs.filter(message_type='critical')
        qss = qsstats.QuerySetStats(xqs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')
        data_critical = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        ###################
        # Get data from DB
        ###################
        # get error
        xqs = qs.filter(message_type='error')
        qss = qsstats.QuerySetStats(xqs, 'time')
        time_series = qss.time_series(date_start, date_end, 'hours')
        data_error = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]

        ###################
        # Format for graph
        ###################
        # make the graph
        data = [{'name': 'All', 'data': data_total},
                {'name': 'Critical', 'data': data_critical},
                {'name': 'Error', 'data': data_error}]
        ###################
        # Create the graph
        ###################
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
        ###################
        # Get hosts for this company
        ###################
        hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
        return hosts


class Test6(DPage):
    """
    Test accordion
    """
    title = 'DjangoPages_Test6'
    description = 'Demonstrate accordion with text widgets'
    tags = []

    def page(self):
        """
        Create simple accordion page
        """
        ###################
        # Put some data in accordion panels
        ###################
        xcritical = AccordionPanel(syslog_event_graph(), title='Critical events: all companies/nodes')
        xerror = AccordionPanel(syslog_event_graph(message_type='error'),
                                title='Error events: all companies/nodes')
        xco = []
        for co in ['BMC_1', 'Smart_1']:
            xco.append(AccordionPanel(syslog_event_graph(company=co),
                                      title='Critical events: {} all nodes'.format(co)))
            xco.append(AccordionPanel(syslog_event_graph(company=co, message_type='error'),
                                      title='Error events: {} all nodes'.format(co)))
        ###################
        # Put into a layout
        ###################
        self.content = Accordion(xcritical, xerror, xco)
        return self


class Test7(DPage):
    """
    Test form support
    """
    title = 'DjangoPages_Test7'
    description = 'Demonstrate basic form widgets with off page link'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Create a form
        ###################
        # noinspection PyDocstring
        class TestFormButton(forms.Form):
            message = forms.CharField(initial='Enter your message here.', required=False,
                                      # widget=forms.TextInput(attrs={'onChange': 'this.form.submit()'})
                                      )

        xrform = Form(self, TestFormButton, 'Update the display',
                      action_url='/dpages/test7')
        ###################
        # Create some other content that uses form data
        ###################
        xr1 = Markdown('# Test of form support\n\n')

        message = self.request.POST.get('message', 'No message yet')

        xr2 = Markdown('**The form button message is: << {} >>**\n\n'.format(message))
        xr4 = HTML('<a class="btn btn-success form-control" href="/">Done playing.</a>')
        ###################
        # Put into a layout
        ###################
        self.content = (R1C12(xr1),
                        R(C4(xrform), C6(xr2)),
                        R1C3(xr4))
        return self


class Test8(DPage):
    """
    Test table2 support
    """
    title = 'DjangoPages_Test8'
    description = 'Demonstrate DB driven table2 widget'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Create some page content
        ###################
        # Title for the page
        xr1 = Markdown('# Test of table support\n\n')

        ###################
        # Get DB data and put in Table
        ###################
        # Node: create title, get queryset, create the table
        node_tit = Markdown('### Node table')
        node_qs = VNode.objects.all()
        node_tbl = Table2(self, node_qs)

        ###################
        # Get DB data and put in Table
        ###################
        # Company: create title, get queryset, create the table
        company_tit = Markdown('### Company table')
        company_qs = VCompany.objects.all()
        company_tbl = Table2(self, company_qs)

        ###################
        # Create some page content
        ###################
        # Some stuff after the page
        xr3 = Markdown('\n\n**After the table**\n\n')

        ###################
        # Put content on page
        ###################
        # Define the content layout
        self.content = (RC(xr1),
                        R(C3(company_tit, company_tbl),
                          C6(node_tit, node_tbl)),
                        RC(xr3))
        # self.content = t_node
        return self


class Test9(DPage):
    """
    Test button pannels
    """
    title = 'DjangoPages_Test9'
    description = 'Demonstrate button panel'
    tags = []

    def page(self):
        """
        Override
        """
        ###################
        # Get node DB data and put in Table
        ###################
        # Node: create title, get queryset, create the table
        node_tit = Markdown('### Node table')
        node_qs = VNode.objects.all()
        node_tbl = Table2(self, node_qs)

        ###################
        # Get company DB data and put in Table
        ###################
        # Company: create title, get queryset, create the table
        company_tit = Markdown('### Company table')
        company_qs = VCompany.objects.all()
        company_tbl = Table2(self, company_qs)

        ###################
        # Create a button panel
        ###################
        pn = Panel(node_tit, node_tbl)
        bpn = ButtonPanel('Open the node panel', pn)
        pc = Panel(company_tit, company_tbl)
        bpc = ButtonPanel('Open the company panel', pc)

        ###################
        # Put content on page
        ###################
        # Define the content layout
        self.content = (
            RC(get_paragraph()),
            Panel(R(C3(company_tit, company_tbl)), button='Show Companies'),
            Panel(R(C6(node_tit, node_tbl)), button='Show Nodes'),
            RC(get_paragraph()),
            RC(Markdown('#Button Panel')),
            R1C6(('The button is in the left column.', bpn, bpc, 'The panel is in the right column', get_paragraph()),
                 (get_paragraph(), Markdown('#### Node panel will appear here'), pn,
                  get_paragraph(), Markdown('#### Company panel will appear here'), pc))
            )
        # self.content = t_node
        return self


class Test10(DPage):
    """
    Test buttons
    """
    title = 'DjangoPages_Test10'
    description = 'Demonstrate basic buttons'
    tags = []

    def page(self):
        """
        Build button test page
        """
        b1 = Button('Default')
        b2 = Button('Primary', 'btn-primary')
        b3 = Button('Success', 'btn-success')
        b4 = Button('Info', 'btn-info')
        b5 = Button('Warning', 'btn-warning')
        b6 = Button('Danger', 'btn-danger')
        b7 = Button('Link', 'btn-link')
        b8 = Button('Link', 'btn-primary', 'btn-lg')
        b9 = Button('Link', 'btn-primary', '')
        b10 = Button('Link', 'btn-primary', 'btn-sm')
        b11 = Button('Link', 'btn-primary', 'btn-xs')
        self.content = (RC12(Markdown('Buttons come in different colors/styles')),
                        R(C12(b1, b2, b3, b4, b5, b6, b7)),
                        RC12(Markdown('Buttons come in sizes')),
                        R(C12(b8, b9, b10, b11)),)
        return self


class Test11(DPage):
    """
    Test modal
    """
    title = 'DjangoPages_Test11'
    description = 'Demonstrate modal linked to button'
    tags = []

    def page(self):
        """
        Build modal test page
        """
        mdl1 = Modal(RC(Markdown('#This is modal 1'),get_paragraph(), get_paragraph()))
        b1 = ButtonModal('Click to display modal 1', mdl1)
        mdl2 = Modal(RC(Markdown('#This is modal 2'),get_paragraph(), get_paragraph()))
        b2 = ButtonModal('Click to display modal 2', mdl2)
        mdl3 = Modal(get_paragraph(), get_paragraph(),
                     button='Modal 3 button',
                     header=Markdown('####Markdown header for modal 3'),
                     footer=(Button('A button'), 'This is the footer for modal 3',))
        self.content = (RC(get_paragraph()),
                        R(C(b1, b2)),
                        RC(get_paragraph()),
                        RC(mdl3),
                        RC(get_paragraph()))
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
               'test9': Test9,
               'test10': Test10,
               'test11': Test11,
               }

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        """
        Execute the graph method and display the results.
        :param request:
        """
        dt = self.testmap[self.test]
        dpage = dt(request).page()
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
        dpage = dt(request).page()
        return dpage.render()
