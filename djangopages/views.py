#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/7/14 - Initial creation

"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
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

import datetime
import qsstats

from django.views.generic import View
from django.db.models import Count
from django import forms

from djangopages.dpage import *
from djangopages.dpage_layout import *
from djangopages.dpage_bootstrap3 import *
from djangopages.dpage_graphs import *
from djangopages.dpage_texthtml import *

#todo 3: unused imports, shouldn't I have examples for these
from test_data.models import syslog_query, syslog_companies, syslog_hosts,\
    syslog_event_graph, \
    VNode, VCompany

########################################################################################################################
#
# Dpage that list the available DPage tests.
#
########################################################################################################################


class DPagesList(DPage):
    """
    Page to list DPages
    """
    title = 'DjangoPages_List'
    description = 'This page: list the available DPages'
    tags = []

    def page(self):
        """
        List available pages
        """
        # noinspection PyUnresolvedReferences
        pages = DPage.pages_list
        pages = sorted(pages, key=lambda x: x['name'])
        out = []
        for page in pages:
            # get the class definition for this page
            cls = page['cls']
            # make a link button object to execute an instance of the class
            lnk = Link('/dpages/{name}'.format(name=cls.__name__), 'Run test', button=True)
            # Output a line with the link button, test title, and test description
            line = RX(C3((lnk, ' ', cls.title,)), C6(cls.description))
            out.append(line)
        self.content = out
        return self

########################################################################################################################
#
# Display and process a DPage
#
########################################################################################################################


class DPagesView(View):
    """
    View class for dev testing.
    """
    @staticmethod
    def get(request, name):
        """
        Execute the graph method and display the results.
        :param request:
        """
        # noinspection PyUnresolvedReferences
        dt = DPage.pages_dict[name]
        dpage = dt(request).page()
        return dpage.render()

    @staticmethod
    def post(request, name):
        """
        Send the post data to the page and rerender.
        :param request:
        """
        # noinspection PyUnresolvedReferences
        dt = DPage.pages_dict[name]
        dpage = dt(request).page()
        return dpage.render()

########################################################################################################################
#
# Development test class based view
#
########################################################################################################################


class Test000a(DPage):
    title = 'DjangoPages_Test000a'
    description = 'DjangoPages concepts'
    tags = []

    def page(self):
        doc_heading = Markdown('### DjangoPages Concepts').render()
        doc = Markdown("""
DjangoPages is built on a few simple concepts uniformly applied.

Each Django page must

 * **inherit from the DPage class** and
 * **override the base class page method**, ie. it must set self.content to the page's html content.

To make it easy to create the page, ie. set self.content, DjangoPages provides a rich collection
of methods to:

 * Create text and graph content on the page, including DB driven content
 * Layout the page using bootstrap 3's grid technology
 * Use a large range of bootstrap 3 and jQuery widgets to create highly functional pages

The tests in this list were originally developed during development to validate DjangoPage
functionality.  They provide an introduction to DjangoPages and its features.

Of necessity, it was necessary to use some features before they are introduced.  However, if you
study the test in order you will encounter all DjangoPage's features.
        """)

        self.content = R(C(Panel(doc, heading=doc_heading)))
        return self


class Test000b(DPage):                              # The class name also defines the page's URL
    title = 'DjangoPages_Test000b'                  # Define the page title
    description = 'DjangoPage overview'             # Set the page's description
    tags = []                                       # Pages may have tags to facilitate searching

    def page(self):                                 # Override the page method to generate the page's HTML

        # Create some page content
        doc_heading = Markdown('### DjangoPage Overview')
        doc = Markdown("""
The source for a DjangoPage generally looks something like this:

    class Test000b(DPage):                              # The class name also defines the page's URL
        title = 'DjangoPages_Test000b'                  # Define the page title
        description = 'DjangoPage overview'             # Set the page's description
        tags = []                                       # Pages may have tags to facilitate searching

        def page(self):                                 # Override the page method to generate the page's HTML

            # Create some page content
            doc_heading = Markdown('### DjangoPage Overview')
            doc = Markdown('The source for a DjangoPage generally looks something like this:')
            panel = Panel(doc, heading=doc_heading)

            # Put it in a bootstrap 3 grid
            column = Column(panel)
            row = Row(column)
            self.content = row
            return self

The code is generally self descriptive.

 * Markdown creates a markdown object.
 * Panel(doc, heading=doc_heading)) creates a bootstrap 3 panel with a heading
 * Column() creates a full width bootstrap 3 column to contain the panel
 * Row() creates a bootstrap 3 row that contains the column


Most DjangoPages follow this general pattern.

While the page could be written in this fashion, most pages take advantage of various convenience
methods and techniques to reduce the code count.  Many of these techniques are introduced in the
tests that follow.
        """)

        # Put the content in a bootstrap 3 responsive grid
        self.content = Row(Column(Panel(doc, heading=doc_heading)))
        return self


class Test001(DPage):
    title = 'DjangoPages_Test001'
    description = 'Demonstrate Text widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### Text(&lt;content&gt;[,...])').render()
        doc = Panel(Markdown("""
The Text widget simply outputs it's content.  It does not add an HTML wrapper.

 * Multiple content is concatenated.
 * Text can also output raw HTML
 * If content is an object, it's render method is called and the output concatenated.

####Code
    content = Text('This is some Text content. ',
                   'This is some more Text content.',
                   '</br>Text can also output HTML',
                   Markdown('**Embedded markdown bold text.**'))
        """), heading=doc_heading)
        content = Text('This is some Text content. ',
                       'This is some more Text content.',
                       '</br>Text can also output HTML.',
                       Markdown('**Embedded markdown bold text.**'))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test002(DPage):
    title = 'DjangoPages_Test002'
    description = 'Demonstrate HTML widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### HTML(&lt;content&gt;[,...])').render()
        doc = Panel(Markdown("""
The HTML widget is identical to the Text widget and simply outputs it's content.
It does not add an HTML wrapper.

 * Multiple content is concatenated.
 * If content is an object, it's render method is called and the output concatenated.

####Code
    content = HTML('<strong>This is some strong HTML content.</strong> ',
                   '<i>This is some italic HTML content.</i>',
                   '</br><u>Text can also output underlined HTML.</u>',
                   Markdown('**Embedded markdown bold text.**'))
        """), heading=doc_heading)
        content = HTML('<strong>This is some strong HTML content.</strong> ',
                       '<i>This is some italic HTML content.</i>',
                       '</br><u>Text can also output underlined HTML.</u>',
                       Markdown('**Embedded markdown bold text.**'))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test003(DPage):
    title = 'DjangoPages_Test003'
    description = 'Demonstrate Markdown widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### Markdown(&lt;content&gt;[,...])').render()
        doc = Panel(Markdown("""
The Markdown widget accepts Markdown text and renders the HTML equivalent.

 * Multiple content is concatenated.
 * If content is an object, it's render method is called and the output concatenated.

####Code
    content = Markdown('###Markdown h3',
                       '**Markdown bold text**',
                       Markdown('*Embedded markdown object italic text.*'))
        """), heading=doc_heading)
        content = Markdown('###Markdown h3',
                           '**Markdown bold text**',
                           Markdown('*Embedded markdown object italic text.*'))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test004(DPage):
    title = 'DjangoPages_Test004'
    description = 'Demonstrate LI_paragraph widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### LI_paragraph() generates loremipsum paragraphs').render()
        doc = Panel(Markdown("""
LI_para(amount=1, para=True) generates amount loremipsum paragraphs.  This is often useful during page development.

 * **amount** is the number of paragraphs to generate
 * **para** if true wraps each paragraph in an HTML paragraph

####Code
    content = Text(LI_paragraph(2))
        """), heading=doc_heading)
        content = Text(LI_paragraph(2))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test005(DPage):
    title = 'DjangoPages_Test005'
    description = 'Demonstrate LI_sentence widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### LI_sentence() generates loremipsum sentences').render()
        doc = Panel(Markdown("""
LI_sentence(amount=1, para=True) generates amount loremipsum sentences.  This is often useful during page development.

 * **amount** is the number of sentences to generate
 * **para** if true wraps the sentences in an HTML paragraph

####Code
    content = Text(LI_para(5))
        """), heading=doc_heading)
        content = Text(LI_sentence(5))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test006(DPage):
    title = 'DjangoPages_Test006'
    description = 'Demonstrate LI widget'
    tags = []

    def page(self):
        doc_heading = Markdown('### LI() generates loremipsum paragraphs').render()
        doc = Panel(Markdown("""
LI(amount=1, para=True) generates amount loremipsum paragraphs if amount is an int/long.
If amount is a list, it specifies the length in sentences of each generated paragraph.
  This is often useful during page development.

 * **amount** is the number of pragraphs to generate or a list of paragraph lengths in sentences
 * **para** if true wraps the paragraphs in an HTML paragraph

####Code
    content = Text(LI([1, 2, 5]))
        """), heading=doc_heading)
        content = Text(LI([1, 2, 5]))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test007(DPage):
    title = 'DjangoPages_Test007'
    description = 'Demonstrate Text, HTML, Markdown, and LI widgets on same page'
    tags = []

    def page(self):
        doc_heading = Markdown('### Text, HTML, Markdown, and LI output can be combined').render()
        doc = Panel(Markdown("""
Text, HTML, Markdown, and LI content can be combined on a page.

####Code
    content = []
    content.append(Markdown('**Some bold Markdown text**'))
    content.append(HTML('<i><b>Some italic bold HTML text</b></i>'))
    content.append(Text('</br>Some Text text'))
    content.append(LI([3, 5]))
        """), heading=doc_heading)
        # noinspection PyListCreation
        content = []
        content.append(Markdown('**Some bold Markdown text**'))
        content.append(HTML('<i><b>Some italic bold HTML text</b></i>'))
        content.append(Text('</br>Some Text text'))
        content.append(LI([3, 5]))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test008(DPage):
    title = 'DjangoPages_Test008'
    description = 'Demonstrate Row and Column layout basics'
    tags = []

    def page(self):
        doc_heading = Markdown('### Row and Column layout basics').render()
        doc = Panel(Markdown("""
Row and Column can be used to create responsive page grid layouts.

The basic methods are

 * Row to create a bootstrap 3 row
 * Column to create a bootstrap 3 column

####Code
    r1 = Markdown('####Text in row 1')
    r2 = Markdown('####Text in row 2')

    content = []
    content.append(Row(Column(r1)))
    content.append(Row(Column(r2)))
    content = Panel(content, heading=Markdown('###Code output').render())
    self.content = RX(C6(doc), C6(content))
        """), heading=doc_heading)
        r1 = Markdown('####Text in row 1')
        r2 = Markdown('####Text in row 2')

        # noinspection PyListCreation
        content = []
        content.append(Row(Column(r1)))
        content.append(Row(Column(r2)))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test009(DPage):
    title = 'DjangoPages_Test009'
    description = 'Demonstrate R and C convenience methods'
    tags = []

    def page(self):
        doc_heading = Markdown('### Convenience methods & techniques for grid layouts').render()
        doc = Panel(Markdown("""
DjangoPages provides a number of convenience methods and techniques to simplify creating
responsive bootstrap 3 grid layouts.

The R and C convenience methods can be used to reduce typing.

The content can be built without creating an explicit content list.

####Code
    r1 = Markdown('####Text in row 1')
    r2 = Markdown('####Text in row 2')

    content = Panel([R(C(r1)),
                     R(C(r2))],
                    heading=Markdown('###Code output').render())
    self.content = RX(C6(doc), C6(content))

This technique makes the grid layout clearer and avoids several lines of code.

You can even do this:

####Code
    content = Panel([R(C(Markdown('####Text in row 1'))),
                     R(C(Markdown('####Text in row 2')))],
                    heading=Markdown('###Code output').render())
    self.content = RX(C6(doc), C6(content))

You may use whatever style you find comfortable.
        """), heading=doc_heading)
        r1 = Markdown('####Text in row 1')
        r2 = Markdown('####Text in row 2')

        content = Panel([R(C(r1)),
                         R(C(r2))],
                        heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self


class Test020(DPage):
    title = 'DjangoPages_Test020'
    description = 'Demonstrate Row and Column layout basics'
    tags = []

    def page(self):
        doc_heading = Markdown('### Row and Column layout basics').render()
        doc = Panel(Markdown("""
Row and Column can be used to create responsive page grid layouts.

The basic methods are

 * Row to create a bootstrap 3 row
 * Column to create a bootstrap 3 column

The convenience methods R for Row and C for Column save typing and make layout creation easier.

In bootstrap 3, columns have a width of 1 - 12 within their container.  The convenience method
Cn specified a bootstrap 3 column of width n, ex C3 specified a bootstrap 3 column of width 3.

Generally, when DjangoPage widgets receive a list argument the widget applies itself to each
element in the list, ie. **widget(a, b) === widget(a)+widget(b)**.  This is almost always the
desired behavior.  When it is not use the X widget, ie.
**widget(X(a,b)) === widget(a.render()+b.render()).

####Code
    r1 = LI([5])                    # text for row 1
    r2c1 = LI([3, 2])               # text for row 2 column 1
    r2c2 = LI(1)                    # text for row 2 column 2

    # create layout
    content = []
    content.append(R(C(r1)))
    content.append(R(X(C6(r2c1), C6(r2c2))))
    content = Panel(content, heading=Markdown('###Code output').render())
    self.content = RX(C6(doc), C6(content))
        """), heading=doc_heading)
        r1 = LI([5])                    # text for row 1
        r2c1 = LI([3, 2])               # text for row 2 column 1
        r2c2 = LI(1)                    # text for row 2 column 2

        # create layout
        content = []
        content.append(R(C(r1)))
        content.append(R(X(C6(r2c1), C6(r2c2))))
        content = Panel(content, heading=Markdown('###Code output').render())
        self.content = RX(C6(doc), C6(content))
        return self



class Test02(DPage):
    """
    Basic test of layout facility.
    """
    title = 'DjangoPages_Test02'
    description = 'Demonstrate row/column layout of text objects'
    tags = []

    def page(self):
        """
        Override
        """
        intro = Markdown("""
**DjangoPages** provides a number of ways to layout content using bootstrap3.

This code layout creates 3 rows spanning the full page.  If you resize the browser you will see that the page
 is responsive.

    def page(self):
        # Create some page content
        xr1 = HTML('<h3> H3 Text on row 1</h3>')
        xr2 = Markdown('**Markdown bold text on row 2.**  Followed by regular text. ')
        xr3 = Text('Text on row 3')

        # Layout the content on the page
        self.content = (RC(xr1), RC(xr2), RC(xr3), RC('Raw strings are OK'))
        return self

**Many** other methods can be used to layout content.

Below is the output for this page.
<hr style="box-shadow: 0 0 10px 1px black;">
        """)
        # Create some page content
        xr1 = Markdown('This is row 1')
        xr2 = Markdown('**Markdown bold text on row 2.**  Followed by regular text. ')
        xr3 = Text('Text on row 3')

        # Layout the content on the page
        self.content = (RC(intro), RC(xr1), RC(xr2), RC(xr3), RC('Raw strings are OK'))
        return self


class Test03(DPage):
    """
    Complex render test
    """
    title = 'DjangoPages_Test03'
    description = 'Demonstrate complex row/column layout'
    tags = []

    def page(self):
        """
        Override
        """
        intro = Markdown("""
**DjangoPages** easily creates complex bootstrap layouts with multiple rows and multiple of columns per row.

This code layout creates 3 rows spanning the full page.  If you resize the browser you will see that the page
 is responsive.

Note: GP generates loremipsum text.

    def page(self):
        # Create some page content
        x1 = Text('Row 1: This text comes from dpage.Text')
        x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
        x22 = HTML('<p>Row 2 col 2: </p>')
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(GP()))    # GP generates loremipsum text
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(GP()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(GP()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(GP()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(GP()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(GP()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(GP()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(GP()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(GP()))

        # Layout the content on the page. This layout generates roughly 200 lines of Bootstrap 3 html!
        self.content = (RC(x1),                         # row with 1 full width column
                        RC6(x21, x22),                  # row with 2 column each is 6 wide
                        RC(x3),                         # row with 1 full width column
                        RX(C3(x41), C9(x42)),           # row with 1 column 3 wide and 1 column 9 wide
                        RX(C3(x51), C9(RC(x521),        # row with 1 column 3 wide and 1 column 9 wide
                                                        # 9 wide column has 3 rows, the last of chich has 3 columns
                                       RC(x522),
                                       RX(C4(x5231), C4(x5232), C4(x5233))
                                       )
                           )
                        )
        return self

Below is the output for this page.
<hr style="box-shadow: 0 0 10px 1px black;">
        """)

        # Create some page content
        x1 = Text('Row 1: This text comes from dpage.Text')
        x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
        x22 = HTML('<p>Row 2 col 2: </p>')
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(GP()))    # GP generates loremipsum text
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(GP()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(GP()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(GP()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(GP()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(GP()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(GP()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(GP()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(GP()))

        # Layout the content on the page. This layout generates roughly 200 lines of Bootstrap 3 html!
        self.content = (RC(intro),                      # output the intro
                        RC(x1),                         # row with 1 full width column
                        RC6(x21, x22),                  # row with 2 column each is 6 wide
                        RC(x3),                         # row with 1 full width column
                        RX(C3(x41), C9(x42)),           # row with 1 column 3 wide and 1 column 9 wide
                        RX(C3(x51), C9(RC(x521),        # row with 1 column 3 wide and 1 column 9 wide
                                                        # 9 wide column has 3 rows, the last of chich has 3 columns
                                       RC(x522),
                                       RX(C4(x5231), C4(x5232), C4(x5233))
                                       )
                           )
                        )
        return self

# todo 1: start here to upgrade examples


class Test04(DPage):
    """
    Basic test of Graph facility with two graphs in a row.
    """
    title = 'DjangoPages_Test04'
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
                               '{}\n\n'.format(GP()) +
                               '{}\n\n'.format(GP()) +
                               '{}\n\n'.format(GP()))
        ###################
        # Layout the content on the page
        ###################
        self.content = (RXC(text_top),
                        RXC6(col_graph, pie_graph),
                        RXC(text_bottom))
        return self


class Test05(DPage):
    """
    Multiple graphs on page with multiple kinds of graphs
    """
    title = 'DjangoPages_Test05'
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
        # noinspection PyRedundantParentheses
        return (RC4(cbt, cecbn, eecbn), RC(errbt),)

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
        xxx = RX(C4(cbt), C8(errbt))
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


class Test06(DPage):
    """
    Test accordion
    """
    title = 'DjangoPages_Test06'
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


class Test07(DPage):
    """
    Test form support
    """
    title = 'DjangoPages_Test07'
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
                      action_url='/dpages/Test07')
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
        self.content = (RXC12(xr1),
                        R(C4(xrform), C6(xr2)),
                        RXC3(xr4))
        return self


class Test08(DPage):
    """
    Test table2 support
    """
    title = 'DjangoPages_Test08'
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
        # self.content = (RC(xr1),
        #                 R(C3(X(company_tit, company_tbl)),
        #                   C6(X(node_tit, node_tbl))),
        #                 RC(xr3))
        self.content = (RC(xr1),
                        RX(C3X(company_tit, company_tbl),
                           C6(X(node_tit, node_tbl))),
                        RC(xr3))
        # self.content = t_node
        return self

# fixme: test09 failing

class Test09(DPage):
    """
    Test button pannels
    """
    title = 'DjangoPages_Test09'
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
        self.content = (Markdown('**Side by side panels**'),
                        RX(C2(Panel(company_tit, company_tbl, button='Show Companies')),
                           C6(Panel(node_tit, node_tbl, button='Show Nodes'))),
                        RC(GP()),
                        RC(Markdown('#Button Panel')),
                        RXC6(('The button is in the left column.', bpn, bpc,
                              'The panel is in the right column', GP()),
                             (GP(), Markdown('#### Node panel will appear here'), pn,
                              GP(), Markdown('#### Company panel will appear here'), pc)
                             ),
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
        b2 = Button('Primary', btn_type='btn-primary')
        b3 = Button('Success', btn_type='btn-success')
        b4 = Button('Info', btn_type='btn-info')
        b5 = Button('Warning', btn_type='btn-warning')
        b6 = Button('Danger', btn_type='btn-danger')
        b7 = Button('Link', btn_type='btn-link')
        b8 = Button('Link', btn_type='btn-primary', btn_size='btn-lg')
        b9 = Button('Link', btn_type='btn-primary', btn_size='')
        b10 = Button('Link', btn_type='btn-primary', btn_size='btn-sm')
        b11 = Button('Link', btn_type='btn-primary', btn_size='btn-xs')
        b12 = Button(X(Markdown('### Markdown title\nSome additional text')))
        b13 = Button('btn-block button', btn_extra='btn-block')
        self.content = (RC12(Markdown('Buttons come in different colors/styles')),
                        R(C12X(b1, b2, b3, b4, b5, b6, b7)),
                        RC12(Markdown('Buttons come in sizes')),
                        R(C12X(b8, b9, b10, b11)),
                        R(C12X('<br/>', b12)),
                        RC4(b13))
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
        mdl1 = Modal(RC(Markdown('#This is modal 1'), GP(), GP()))
        b1 = ButtonModal('Click to display modal 1', mdl1)
        mdl2 = Modal(RC(Markdown('#This is modal 2'), GP(), GP()))
        b2 = ButtonModal('Click to display modal 2', mdl2)
        mdl3 = Modal(GP(), GP(),
                     button='Modal 3 button',
                     header=Markdown('####Markdown header for modal 3'),
                     footer=(Button('A button'), 'This is the footer for modal 3',))
        self.content = (RC(GP()),
                        RCX('Text before buttons ', b1, b2, ' Text after buttons'),
                        RC(GP()),
                        RC(X('Text before button ', mdl3, ' Text after button')),
                        RC(GP()))
        return self


class Test12(DPage):
    """
    Test modal
    """
    title = 'DjangoPages_Test12'
    description = 'Demonstrate carousel'
    tags = []

    def page(self):
        """
        Build carousel test page
        """
        c1r = Markdown('#### Content 1', GP())
        c2r = Markdown('#### Content 2', GP())
        c3r = Markdown('#### Content 3', GP())
        c4r = Markdown('#### Content 4', GP())
        c1l = Markdown('#### Content 1', GP())
        c2l = Markdown('#### Content 2', GP())
        c3l = Markdown('#### Content 3', GP())
        c4l = Markdown('#### Content 4', GP())
        crsl1 = Carousel(c1r, c2r, c3r, c4r)
        crsl2 = Carousel(c1l, c2l, c3l, c4l)
        self.content = (RC(GP()),
                        RX(C3(Markdown('**Panel on left**')), C9(crsl1)),
                        RC(GP()),
                        RX(C9(crsl2), C3(Markdown('**Panel on right**'))),
                        RC(GP())
                        )
        return self


class Test13(DPage):
    title = 'DjangoPages_Test13'
    description = 'Demonstrate links'
    tags = []

    def page(self):
        self.content = (RC(Link('/dpages/DPagesList', 'Link to list page')),
                        RC(Link('/dpages/Test07', 'Link to the form test page')),
                        RC(Markdown('#### Link buttons')),
                        RXC((Link('/dpages/DPagesList', 'Link to list page', button=True), ' ',
                             Link('/dpages/Test07', 'Link to the form test page', button=True),)
                            )
                        )
        return self
