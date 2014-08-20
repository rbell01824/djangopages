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

from djangopages.dpage import *
from djangopages.dpage_layout import *
from djangopages.dpage_bootstrap3 import *
from djangopages.dpage_graphs import *
from djangopages.dpage_texthtml import *

from django.db.models import Count
from test_data.models import VSyslog

########################################################################################################################

from django.shortcuts import render


def index(request):
    context = {'foo': 'bar'}
    return render(request, 'index.html', context)


class DemoList(DPage):
    """ List the available DPage(s) """
    title = 'DjangoPages List 2'
    description = 'List the test/demo DPages'
    tags = []

    def get(self, *args, **kwargs):
        """ List available pages """
        t = '<a href="/dpages/{name}" ' \
            'class="btn btn-default btn-xs" ' \
            'role="button" ' \
            'style="width:400px;text-align:left;margin-bottom:2px;">' \
            '{text}' \
            '</a><br/>\n'
        # noinspection PyUnresolvedReferences
        pages = DPage.find('demo')
        out = ''
        for page in pages:
            # get the class definition for this page
            cls = page['cls']
            # make a link button object to execute an instance of the class
            # lnk = Link('/dpages/{name}'.format(name=cls.__name__), cls.title)
            # lnkbtn = Button(lnk, btn_size='btn-xs')
            # Output a line with the link button, test title, and test description
            line = t.format(name=cls.__name__, text=cls.description)
            out += line
        self.content = out
        return self


class TestBasicGraphs001(DPage):
    """ Basic test of Graph facility with two graphs in a row. """
    title = 'Graphs'
    description = 'Data base query with multiple graphs in a row'
    tags = ['demo', 'graphs']

    def get(self, *args, **kwargs):
        # set the company and node, and get the syslog data

        company = 'BMC_1'
        node = 'A0040CnBPGC1'
        qs = VSyslog.objects.filter(node__host_name=node,
                                    node__company__company_name=company)

        # Count all the syslog records
        all_count_host = qs.count()

        # Get count by type data
        xqs = qs.values('message_type').annotate(num_results=Count('id'))

        # Format for bar chart
        count_by_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))

        # Create the charts
        # create the column chart and set it's title
        col_graph = GraphCK('column', count_by_type,
                            options={'height': '400px',
                                     'title.text': 'Syslog records by type',
                                     'subtitle.text': '{} node {}'.format(company, node)})

        # Sort data for pie chart
        count_by_type_sorted_by_count = sorted(count_by_type, lambda x, y: cmp(x[1], y[1]), None, True)

        # create the pie chart and set it's title
        pie_graph = GraphCK('pie', count_by_type_sorted_by_count,
                            options={'height': '400px',
                                     'title.text': 'Syslog records by type',
                                     'subtitle.text': '{} node {}'.format(company, node)})

        # Create title and other page content
        text_top = Markdown('### Error count by type for {} Node {} '.format(company, node) +
                            'Total errors {}'.format(all_count_host))
        text_bottom = Markdown('### Analysis\n'
                               'Here is where the analysis can go.\n\n' +
                               LI(12, 12))
        # create back link
        lnk = Link('/demo', T(Glyphicon('arrow-left'), 'Back'),
                   classes='btn-primary', style='margin-bottom: 5px;')
        linecnt = T(SP(4), 'Improvement: 4:1, Source ~ 50 lines, Output > 200 lines.')

        # Layout the content on the page
        self.content = T(RC(lnk + linecnt),
                         Panel(None,
                               T(RC(text_top),
                                 RC6(col_graph, pie_graph),
                                 RC(text_bottom))))
        return self


class TestBasicGraphs002(DPage):
    """ Basic test of Graph facility with two graphs in a row. """
    title = 'Graphs'
    description = 'Data base query with multiple graphs in a row,version 2'
    tags = ['demo', 'graphs']

    def get(self, *args, **kwargs):
        # set the company and node, and get the syslog data

        company = 'BMC_1'
        node = 'A0040CnBPGC1'

        # get data from DB
        qs = VSyslog.objects.filter(node__host_name=node,
                                    node__company__company_name=company).values('message_type')
        all_count = qs.count()
        qs_by_type = qs.annotate(num_results=Count('id')).\
            order_by('message_type').\
            values_list('message_type', 'num_results')

        # turn into GraphCK compatible list
        count_by_type = map(list, qs_by_type)

        # make our graphs
        col_graph = GraphCK('column', count_by_type,
                            options={'height': '400px',
                                     'title.text': 'Syslog records by type',
                                     'subtitle.text': '{} node {}'.format(company, node)})
        pie_graph = GraphCK('pie', count_by_type,
                            options={'height': '400px',
                                     'title.text': 'Syslog records by type',
                                     'subtitle.text': '{} node {}'.format(company, node)})

        # Create title and other page content
        text_top = Markdown('### Error count by type for {} Node {} '.format(company, node) +
                            'Total errors {}'.format(all_count))
        text_bottom = Markdown('### Analysis\n'
                               'Here is where the analysis can go.\n\n' +
                               LI(12, 12))
        # create back link
        lnk = Link('/demo', T(Glyphicon('arrow-left'), 'Back'),
                   classes='btn-primary', style='margin-bottom: 5px;')
        linecnt = T(SP(4), 'Improvement: 4:1, Source ~ 50 lines, Output > 200 lines.')

        # Layout the content on the page
        self.content = T(RC(lnk + linecnt),
                         Panel(None,
                               T(RC(text_top),
                                 RC6(col_graph, pie_graph),
                                 RC(text_bottom))))
        return self


# class Test05(DPage):
#     """
#     Multiple graphs on page with multiple kinds of graphs
#     """
#     title = 'DjangoPages_Test05'
#     description = 'Demonstrate syslog graphs and multi-panels'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         For specified company, display a summary report and details by node.
#         """
#         ###################
#         # Create summary for company
#         ###################
#         self.company_summary('BMC_1')
#         return self
#
#     def company_summary(self, company):
#         """
#         For specified company, display a summary report and details by node.
#         :param company: Company
#         :return: DPage OBJECT!
#         """
#         ###################
#         # Use methods to build content
#         ###################
#         # noinspection PyListCreation
#         content = []
#         content.append(self.all_hosts_summary(company))
#         panels = []
#         ###################
#         # Iterate over hosts and build content for each one
#         ###################
#         for host in self.get_hosts(company):
#             panels.append(self.host_summary(company, host))
#         content.append(Accordion(panels))
#         self.content = content
#         return self
#
#     def all_hosts_summary(self, company):
#         """
#         Display bar chart of errors by type for all nodes and a line chart with 4 lines of
#         errors by type vs time.
#         :param company: Company
#         :return: HTML
#         """
#         ###################
#         # Get data from DB
#         ###################
#         qs = syslog_query(company)
#         ###################
#         # Build the graphs we want on the page
#         ###################
#         errbt = self.time_chart(qs, company, 'All Nodes')
#         cbt = self.message_type_graph(qs, company, 'All Nodes')
#         cecbn = self.critical_event_graph(qs, company)
#         eecbn = self.error_event_graph(qs, company)
#         ###################
#         # Layout the content on the page
#         ###################
#         # noinspection PyRedundantParentheses
#         return (RC4(cbt, cecbn, eecbn), RC(errbt),)
#
#     def host_summary(self, company, node):
#         """
#         Create summary output for company
#         :param company: Company
#         :param node: node
#         :return: HTML
#         """
#         ###################
#         # Get the DB data
#         ###################
#         qs = syslog_query(company, node)
#         ###################
#         # Make the charts we want
#         ###################
#         errbt = self.time_chart(qs, company, node)
#         cbt = self.message_type_graph(qs, company, node)
#         cbt.options['height'] = '400px'
#         ###################
#         # Layout the content on the page
#         ###################
#         xxx = R(C4(cbt), C8(errbt))
#         ###################
#         # Put the layout in an accordion multi panel
#         ###################
#         return AccordionMultiPanel(xxx, title='{}:{} Details'.format(company, node))
#
#     # noinspection PyMethodMayBeStatic
#     def message_type_graph(self, qs, company, node):
#         """
#
#         :param qs:
#         :param company:
#         :param node:
#         :return: :rtype:
#         """
#         ###################
#         # Get DB data we want on graph
#         ###################
#         xqs = qs.values('message_type').annotate(num_results=Count('id'))
#         count_by_type_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
#         ###################
#         # Create the graph
#         ###################
#         cbt = Graph('column', count_by_type_type)
#         cbt.options = {'title.text': 'Syslog Messages by Type',
#                        'subtitle.text': '{}:{}'.format(company, node)}
#         return cbt
#
#     # noinspection PyMethodMayBeStatic
#     def critical_event_graph(self, qs, company):
#         """
#         Critical event by node, all nodes
#         :param qs:
#         :param company:
#         """
#         ###################
#         # Get DB data we want on graph
#         ###################
#         # critical event by node
#         critical_event_count_by_node = map(list, qs.filter(message_type='critical').
#                                            order_by('node__host_name').
#                                            values('node__host_name').
#                                            annotate(count=Count('node__host_name')).
#                                            values_list('node__host_name', 'count'))
#         ###################
#         # Create the graph
#         ###################
#         cecbn = Graph('column', critical_event_count_by_node)
#         cecbn.options = {'title.text': 'Critical Events by Host',
#                          'subtitle.text': '{}:All Nodes'.format(company)}
#         return cecbn
#
#     # noinspection PyMethodMayBeStatic
#     def error_event_graph(self, qs, company):
#         """
#         Error event by node all nodes
#         :param qs:
#         :param company:
#         """
#         ###################
#         # Get DB data we want on graph
#         ###################
#         # error event by node
#         error_event_count_by_node = map(list, qs.filter(message_type='error').
#                                         order_by('node__host_name').
#                                         values('node__host_name').
#                                         annotate(count=Count('node__host_name')).
#                                         values_list('node__host_name', 'count'))
#         ###################
#         # Create the graph
#         ###################
#         eecbn = Graph('column', error_event_count_by_node)
#         eecbn.options = {'title.text': 'Error Events by Host',
#                          'subtitle.text': '{}:All Nodes'.format(company)}
#         return eecbn
#
#     @staticmethod
#     def time_chart(qs, company, host):
#         """
#         Create basic time chart summary
#
#         :param qs: Query set for company & host
#         :param company: Company
#         :param host: Host
#         :return: graph OBJECT!
#         """
#         ###################
#         # Get the graph data together
#         ###################
#         # total, critical, error events by time
#         date_start = datetime.date(2012, 12, 1)
#         date_end = datetime.date(2013, 2, 9)
#
#         # setup the qss object & build time series
#         qss = qsstats.QuerySetStats(qs, 'time')
#         time_series = qss.time_series(date_start, date_end, 'hours')
#
#         # format for chartkick
#         data_total = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]
#
#         ###################
#         # Get data from DB
#         ###################
#         # get critical
#         xqs = qs.filter(message_type='critical')
#         qss = qsstats.QuerySetStats(xqs, 'time')
#         time_series = qss.time_series(date_start, date_end, 'hours')
#         data_critical = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]
#
#         ###################
#         # Get data from DB
#         ###################
#         # get error
#         xqs = qs.filter(message_type='error')
#         qss = qsstats.QuerySetStats(xqs, 'time')
#         time_series = qss.time_series(date_start, date_end, 'hours')
#         data_error = [[t[0].strftime('%Y-%m-%d %H'), t[1]] for t in time_series]
#
#         ###################
#         # Format for graph
#         ###################
#         # make the graph
#         data = [{'name': 'All', 'data': data_total},
#                 {'name': 'Critical', 'data': data_critical},
#                 {'name': 'Error', 'data': data_error}]
#         ###################
#         # Create the graph
#         ###################
#         errbt = Graph('area', data)
#         errbt.options = {'height': '440px',
#                          'title.text': '{} Syslog Events By Hour'.format(company),
#                          'subtitle.text': '{}:{}'.format(company, host)
#                                           + ' - {} to {}'.format(date_start, date_end),
#                          'plotOptions.area.stacking': 'normal'
#                          }
#         return errbt
#
#     @staticmethod
#     def get_hosts(company):
#         """
#         Get list of this companies hosts.
#         :param company:
#         """
#         ###################
#         # Get hosts for this company
#         ###################
#         hosts = [n[0] for n in VNode.objects.filter(company__company_name=company).values_list('host_name')]
#         return hosts
#
#
# class Test06(DPage):
#     """
#     Test accordion
#     """
#     title = 'DjangoPages_Test06'
#     description = 'Demonstrate accordion with text widgets'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Create simple accordion page
#         """
#         ###################
#         # Put some data in accordion panels
#         ###################
#         xcritical = AccordionPanel(syslog_event_graph(), title='Critical events: all companies/nodes')
#         xerror = AccordionPanel(syslog_event_graph(message_type='error'),
#                                 title='Error events: all companies/nodes')
#         xco = []
#         for co in ['BMC_1', 'Smart_1']:
#             xco.append(AccordionPanel(syslog_event_graph(company=co),
#                                       title='Critical events: {} all nodes'.format(co)))
#             xco.append(AccordionPanel(syslog_event_graph(company=co, message_type='error'),
#                                       title='Error events: {} all nodes'.format(co)))
#         ###################
#         # Put into a layout
#         ###################
#         self.content = Accordion(xcritical, xerror, xco)
#         return self
#
#
# class Test07(DPage):
#     """
#     Test form support
#     """
#     title = 'DjangoPages_Test07'
#     description = 'Demonstrate basic form widgets with off page link'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Override
#         """
#         ###################
#         # Create a form
#         ###################
#         # noinspection PyDocstring
#         class TestFormButton(forms.Form):
#             message = forms.CharField(initial='Enter your message here.', required=False,
#                                       # widget=forms.TextInput(attrs={'onChange': 'this.form.submit()'})
#                                       )
#
#         xrform = Form(self, TestFormButton, 'Update the display',
#                       action_url='/dpages/Test07')
#         ###################
#         # Create some other content that uses form data
#         ###################
#         xr1 = Markdown('# Test of form support\n\n')
#
#         message = self.request.POST.get('message', 'No message yet')
#
#         xr2 = Markdown('**The form button message is: << {} >>**\n\n'.format(message))
#         xr4 = HTML('<a class="btn btn-success form-control" href="/">Done playing.</a>')
#         ###################
#         # Put into a layout
#         ###################
#         self.content = (RC12(xr1),
#                         R(C4(xrform), C6(xr2)),
#                         RC3(xr4))
#         return self
#
#
# class Test08(DPage):
#     """
#     Test table2 support
#     """
#     title = 'DjangoPages_Test08'
#     description = 'Demonstrate DB driven table2 widget'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Override
#         """
#         ###################
#         # Create some page content
#         ###################
#         # Title for the page
#         xr1 = Markdown('# Test of table support\n\n')
#
#         ###################
#         # Get DB data and put in Table
#         ###################
#         # Node: create title, get queryset, create the table
#         node_tit = Markdown('### Node table')
#         node_qs = VNode.objects.all()
#         node_tbl = Table2(self, node_qs)
#
#         ###################
#         # Get DB data and put in Table
#         ###################
#         # Company: create title, get queryset, create the table
#         company_tit = Markdown('### Company table')
#         company_qs = VCompany.objects.all()
#         company_tbl = Table2(self, company_qs)
#
#         ###################
#         # Create some page content
#         ###################
#         # Some stuff after the page
#         xr3 = Markdown('\n\n**After the table**\n\n')
#
#         ###################
#         # Put content on page
#         ###################
#         # Define the content layout
#         # self.content = (RC(xr1),
#         #                 R(C3(X(company_tit, company_tbl)),
#         #                   C6(X(node_tit, node_tbl))),
#         #                 RC(xr3))
#         self.content = (RC(xr1),
#                         R(C3X(company_tit, company_tbl),
#                            C6(X(node_tit, node_tbl))),
#                         RC(xr3))
#         # self.content = t_node
#         return self
#
# class Test09(DPage):
#     """
#     Test button pannels
#     """
#     title = 'DjangoPages_Test09'
#     description = 'Demonstrate button panel'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Override
#         """
#         ###################
#         # Get node DB data and put in Table
#         ###################
#         # Node: create title, get queryset, create the table
#         node_tit = Markdown('### Node table')
#         node_qs = VNode.objects.all()
#         node_tbl = Table2(self, node_qs)
#
#         ###################
#         # Get company DB data and put in Table
#         ###################
#         # Company: create title, get queryset, create the table
#         company_tit = Markdown('### Company table')
#         company_qs = VCompany.objects.all()
#         company_tbl = Table2(self, company_qs)
#
#         ###################
#         # Create a button panel
#         ###################
#         pn = Panel(X(node_tit, node_tbl))
#         bpn = ButtonPanel('Open the node panel', pn)
#         pc = Panel(X(company_tit, company_tbl))
#         bpc = ButtonPanel('Open the company panel', pc)
#
#         ###################
#         # Put content on page
#         ###################
#         # Define the content layout
#         self.content = (Markdown('**Side by side panels**'),
#                         R(C2(Panel(company_tit, company_tbl, button='Show Companies')),
#                            C6(Panel(node_tit, node_tbl, button='Show Nodes'))),
#                         RC(LI()),
#                         RC(Markdown('#Button Panel')),
#                         RC6(('The button is in the left column.', bpn, bpc,
#                               'The panel is in the right column', LI()),
#                              (LI(), Markdown('#### Node panel will appear here'), pn,
#                               LI(), Markdown('#### Company panel will appear here'), pc)
#                              ),
#                         )
#         # self.content = t_node
#         return self
#
#
# class Test10(DPage):
#     """
#     Test buttons
#     """
#     title = 'DjangoPages_Test10'
#     description = 'Demonstrate basic buttons'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Build button test page
#         """
#         b1 = Button('Default')
#         b2 = Button('Primary', btn_type='btn-primary')
#         b3 = Button('Success', btn_type='btn-success')
#         b4 = Button('Info', btn_type='btn-info')
#         b5 = Button('Warning', btn_type='btn-warning')
#         b6 = Button('Danger', btn_type='btn-danger')
#         b7 = Button('Link', btn_type='btn-link')
#         b8 = Button('Link', btn_type='btn-primary', btn_size='btn-lg')
#         b9 = Button('Link', btn_type='btn-primary', btn_size='')
#         b10 = Button('Link', btn_type='btn-primary', btn_size='btn-sm')
#         b11 = Button('Link', btn_type='btn-primary', btn_size='btn-xs')
#         b12 = Button(X(Markdown('### Markdown title\nSome additional text')))
#         b13 = Button('btn-block button', btn_extra='btn-block')
#         self.content = (RC12(Markdown('Buttons come in different colors/styles')),
#                         R(C12X(b1, b2, b3, b4, b5, b6, b7)),
#                         RC12(Markdown('Buttons come in sizes')),
#                         R(C12X(b8, b9, b10, b11)),
#                         R(C12X('<br/>', b12)),
#                         RC4(b13))
#         return self
#
#
# class Test11(DPage):
#     """
#     Test modal
#     """
#     title = 'DjangoPages_Test11'
#     description = 'Demonstrate modal linked to button'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Build modal test page
#         """
#         mdl1 = Modal(RC(Markdown('#This is modal 1'), LI(), LI()))
#         b1 = ButtonModal('Click to display modal 1', mdl1)
#         mdl2 = Modal(RC(Markdown('#This is modal 2'), LI(), LI()))
#         b2 = ButtonModal('Click to display modal 2', mdl2)
#         mdl3 = Modal(LI(), LI(),
#                      button='Modal 3 button',
#                      header=Markdown('####Markdown header for modal 3'),
#                      footer=(Button('A button'), 'This is the footer for modal 3',))
#         self.content = (RC(LI()),
#                         RCX('Text before buttons ', b1, b2, ' Text after buttons'),
#                         RC(LI()),
#                         RC(X('Text before button ', mdl3, ' Text after button')),
#                         RC(LI()))
#         return self
#
#
# class Test12(DPage):
#     """
#     Test modal
#     """
#     title = 'DjangoPages_Test12'
#     description = 'Demonstrate carousel'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         """
#         Build carousel test page
#         """
#         c1r = Markdown('#### Content 1', LI())
#         c2r = Markdown('#### Content 2', LI())
#         c3r = Markdown('#### Content 3', LI())
#         c4r = Markdown('#### Content 4', LI())
#         c1l = Markdown('#### Content 1', LI())
#         c2l = Markdown('#### Content 2', LI())
#         c3l = Markdown('#### Content 3', LI())
#         c4l = Markdown('#### Content 4', LI())
#         crsl1 = Carousel(c1r, c2r, c3r, c4r)
#         crsl2 = Carousel(c1l, c2l, c3l, c4l)
#         self.content = (RC(LI()),
#                         R(C3(Markdown('**Panel on left**')), C9(crsl1)),
#                         RC(LI()),
#                         R(C9(crsl2), C3(Markdown('**Panel on right**'))),
#                         RC(LI())
#                         )
#         return self
#
#
# class Test13(DPage):
#     title = 'DjangoPages_Test13'
#     description = 'Demonstrate links'
#     tags = ['test', ]
#
#     def get(self, *args, **kwargs):
#         self.content = (RC(Link('/dpages/DPagesList', 'Link to list page')),
#                         RC(Link('/dpages/Test07', 'Link to the form test page')),
#                         RC(Markdown('#### Link buttons')),
#                         RC((Link('/dpages/DPagesList', 'Link to list page', button=True), ' ',
#                              Link('/dpages/Test07', 'Link to the form test page', button=True),)
#                             )
#                         )
#         return self
