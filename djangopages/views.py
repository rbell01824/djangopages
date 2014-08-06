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
    title = 'DjangoPages Concepts'
    description = 'DjangoPages concepts'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
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
study the test in order you will encounter all DjangoPage's features in a reasonably understandable
fashion.
        """)

        self.content = R(C(Panel(doc, heading=doc_heading)))
        return self


class Test000b(DPage):                              # The class name also defines the page's URL
    title = 'DjangoPages Overview'                  # Define the page title
    description = 'DjangoPage overview'             # Set the page's description
    tags = []                                       # Pages may have tags to facilitate searching

    def page(self):                                 # Override the page method to generate the page's HTML

        # Create some page content
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Markdown("""
The source for a DjangoPage generally looks something like this:

    class Test000b(DPage):                              # The class name also defines the page's URL
        title = 'DjangoPages Overview'                  # Define the page title
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


class Test001a(DPage):
    title = 'Text'
    description = 'Demonstrate Text widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
The Text widget simply outputs it's content.  It does not add an HTML wrapper.

 * Multiple content is concatenated.
 * Text can also output raw HTML
 * If content is an object, the output of it's render method is used.  This allows
   inclusion of the output of other DjangoPage widgets.

####Code
    content = Text('This is some Text content. ',
                   'This is some more Text content.',
                   '</br>Text can also output HTML.',
                   Markdown('**Embedded markdown bold text.**'),
                   Markdown(' *Embedded markdown italic text.*'
                            ' Note, Markdown wraps its output in an HTML paragraph.'))

**Note: These examples use a responsive bootstrap 3 grid layout. This will be explained in subsequent
examples/test.  You can see the responsive behavior by adjusting the browser width.**
        """), heading=doc_heading)
        content = Text('This is some Text content. ',
                       'This is some more Text content.',
                       '</br>Text can also output HTML.',
                       Markdown('**Embedded markdown bold text.**'),
                       Markdown(' *Embedded markdown italic text.*'
                                ' Note, Markdown wraps its output in an HTML paragraph.'))
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test001b(DPage):
    title = 'HTML'
    description = 'Demonstrate HTML widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
The HTML widget is **identical to the Text widget** and simply outputs it's content.  Text and
HTML may be used interchangeably.

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
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test001c(DPage):
    title = 'Markdown'
    description = 'Demonstrate Markdown widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
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
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test001d(DPage):
    title = 'LI_Paragraph'
    description = 'Demonstrate LI_Paragraph widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
LI_para(amount=1, para=True) generates amount loremipsum paragraphs.  This is often useful during page development.

 * **amount** is the number of paragraphs to generate
 * **para** if true wraps each paragraph in an HTML paragraph

####Code
    content = LI_Paragraph(2)       # Make two loremipsum paragraphs
        """), heading=doc_heading)
        content = LI_Paragraph(2)       # Make two loremipsum paragraphs
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test001e(DPage):
    title = 'LI_Sentence'
    description = 'Demonstrate LI_Sentence widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
LI_Sentence(amount=1, para=True) generates amount loremipsum sentences.  This is often useful during page development.

 * **amount** is the number of sentences to generate
 * **para** if true wraps the sentences in an HTML paragraph

####Code
    content = LI_para(5)
        """), heading=doc_heading)
        content = LI_Sentence(5)
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test001f(DPage):
    title = 'LI'
    description = 'Demonstrate LI widget'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
LI(amount=1, para=True)

* **amount** is
    * the number of pragraphs to generate or
    * a list of paragraph lengths in sentences
* **para** if true wraps the paragraphs in an HTML paragraph

By using amount=[n, n,...] you can control the paragraph length.

####Code
    content = LI([1, 2, 5])
        """), heading=doc_heading)
        content = LI([1, 2, 5])
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test002a(DPage):
    title = 'Multiple widgets on page'
    description = 'Multiple widgets on a page'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
Multiple widgets can be combined on a page.

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
        content = Panel(content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(content))
        return self


class Test002b(DPage):
    title = 'Simplify content creation'
    description = 'Simplify content creation'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
Using

    content = []
    content.append(Markdown('**Some bold Markdown text**'))
    ...

is needlessly verbose and can lead to difficult to understand code.  Alternately you can

#### Code
    # create the content for column 2 panel
    panel_heading = Markdown('###Output')
    panel_content = (Markdown('**Some bold Markdown text**'),
                     LI([3, 5]))
    # create c2 panel
    c2 = Panel(panel_content, heading=panel_heading)
    # put documentation and column 2 panel in a single row
    # with two columns of width 6
    self.content = RX(C6(doc), C6(c2))
    return self
        """), heading=doc_heading)
        # create the content for column 2 panel
        panel_heading = Markdown('###Output')
        panel_content = (Markdown('**Some bold Markdown text**'),
                         LI([3, 5]))
        # create c2 panel
        c2 = Panel(panel_content, heading=panel_heading)
        # put documentation and column 2 panel in a single row
        # with two columns of width 6
        self.content = RX(C6(doc), C6(c2))
        return self


class Test003a(DPage):
    title = 'Bootstrap 3 grids'
    description = 'Demonstrate bootstrap 3 Row and Column layout basics'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
Row and Column can be used to create responsive bootstrap 3 page grid layouts.

The basic methods are

 * Row(content, ...) to create a bootstrap 3 row
 * Column(content, ..., [width=n]) to create a bootstrap 3 column of width n.

#### Code
    r1 = Markdown('####Text in row 1')
    r2 = Markdown('####Text in row 2')

    panel_heading = Markdown('###Output')
    panel_content = X(Row(Column(r1, width=12)),
                      Row(Column(r2, width=12)))

    panel = Panel(panel_content, heading=panel_heading)
    c1 = Column(doc, width=6)
    c2 = Column(panel, width=6)
    self.content = Row(X(c1, c2))
    return self

**Note: Row(X(c1, c2))** The inner X() renders its content.

DjangoPage widgets generally accept either a single argument or a list.  When given a list, widgets
are applied to each member of the list individually so that

    Row(c1, c2) is equivalent to Row(c1)+Row(c2)

On the example/test pages we want a single row containing two columns.  By using **X(c1, c2)**
we create a single object for the row, ie. we get a single row with two columns not two rows with
a single column each..

Alternately we could have written **Row((c1, c2))**.  The inner () create a list object which
is evaluated before Row is applied.

In the following examples several other convenience methods are introduced.
    """), heading=doc_heading)
        r1 = Markdown('####Text in row 1')
        r2 = Markdown('####Text in row 2')

        panel_heading = Markdown('###Output')
        panel_content = X(Row(Column(r1, width=12)),
                          Row(Column(r2, width=12)))

        panel = Panel(panel_content, heading=panel_heading)
        c1 = Column(doc, width=6)
        c2 = Column(panel, width=6)
        self.content = Row(X(c1, c2))
        return self


class Test003b(DPage):
    title = 'R and C'
    description = 'Demonstrate R and C convenience methods'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
DjangoPages provides a number of convenience methods and techniques to simplify creating
responsive bootstrap 3 grid layouts.  These reduce typing and properly used can make the
page layout clear.

The R and C convenience methods can be used to reduce typing.  They are equivalent to Row
and Column respectively.

####Code
    # create panel's content
    r1 = Markdown('####Text in row 1')
    r2 = Markdown('####Text in row 2')
    # create panel
    panel = Panel(X(R(C(r1, width=12)),         # layout clearly defined
                    R(C(r2, width=12))),
                  heading=Markdown('###Output'))
    # define page content (documentation and output panel)
    self.content = R(X(C6(doc), C6(panel)))
    return self

This technique makes the grid layout clearer and avoids several lines of code and intermediate
values.  In DjangoPages it is generally convenient to define the page content then 'pour' the
content into the grid layout.
        """), heading=doc_heading)
        # create panel's content
        r1 = Markdown('####Text in row 1')
        r2 = Markdown('####Text in row 2')
        # create panel
        panel = Panel(X(R(C(r1, width=12)),         # layout clearly defined
                        R(C(r2, width=12))),
                      heading=Markdown('###Output'))
        # define page content (documentation and output panel)
        self.content = R(X(C6(doc), C6(panel)))
        return self


class Test003c(DPage):
    title = 'R and C: all the details'
    description = 'Row and Column details'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
DjangoPages contains a number of convenience methods to make bootstrap grid layout easy.

    C===Column width defaults to 12
    Cn===Column(..., width=n), 1 <= n <= 12
    CX===Column(X(...))
    CnX===Column(X(...), width=n), 1 <= n <= 12
    R===Row
    RX===Row(X(...))
    RC===Row(Column(...))
    RCn===Row(Column(..., width=n)
    RXC===Row(X(Column(...)))
    RXCn===Row(X(Column(..., width=n)))
    RCX===Row(Column(X(...)))
    RCnX===Row(Column(X(...), width=n)
    RXCX===Row(X(Column(X(...))))
    RXCnX===Row(X(Column(X(...), width=n)))

Some of these convenience methods are rather advanced and as a practical matter probably shouldn't
generally be used as there exact meaning is not clear at a glance.  However, if you need them they
are available.

        """), heading=doc_heading)
        self.content = RC(doc)
        return self


class Test003d(DPage):
    title = 'R and C complex layouts'
    description = 'Row and Column details'
    tags = []

    def page(self):
        doc_heading = Markdown('###{}'.format(self.title))
        doc = Panel(Markdown("""
Row and Column can be used to create arbitrarily complex responsive bootstrap 3 layouts.

Here is the code to create a row with two columns of width 6.

* The left column contains this description in a panel (code not shown).
* The right column contains a panel with two rows
    * Row 1 contains a 5 sentence LI paragraph
    * Row 2 contains 2 columns of width 6 (Note: bootstrap 3 creates a 12 wide grid in each grid cell)
        * The left column contains two LI paragraphs
        * The right column contains a single LI paragraph

####Code
    # define the content
    r1 = LI([5])                    # text for row 1
    r2c1 = LI([3, 2])               # text for row 2 column 1
    r2c2 = LI(1)                    # text for row 2 column 2

    # create layout for panel content
    panel_content = (R(C(r1)), R(X(C6(r2c1), C6(r2c2))))
    panel = Panel(panel_content, heading=Markdown('###Output'))
    self.content = RX(C6(doc), C6(panel))
    return self
        """), heading=doc_heading)
        # define the content
        r1 = LI([5])                    # text for row 1
        r2c1 = LI([3, 2])               # text for row 2 column 1
        r2c2 = LI(1)                    # text for row 2 column 2

        # create layout for panel content
        panel_content = (R(C(r1)), R(X(C6(r2c1), C6(r2c2))))
        panel = Panel(panel_content, heading=Markdown('###Output'))
        self.content = RX(C6(doc), C6(panel))
        return self


class Test003e(DPage):
    """
    Complex render test
    """
    title = 'Complex layout'
    description = 'Demonstrate complex row/column layout'
    tags = []

    def page(self):
        """
        Override
        """
        intro = Markdown("""
**DjangoPages** easily creates complex bootstrap layouts with multiple rows and multiple columns per row.

    def page(self):
        # Create some page content
        x1 = Text('Row 1: This text comes from dpage.Text')
        x21 = Markdown('Row 2 col 1: **Bold Markdown Text**')
        x22 = HTML('<p>Row 2 col 2: </p>')
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(LI()))    # LI generates loremipsum text
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(LI()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(LI()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(LI()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(LI()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(LI()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(LI()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(LI()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(LI()))

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
        x3 = HTML('<p>Row 3: Text from loremipsum. {}</p>'.format(LI()))
        x41 = HTML('<p>Row 4 col 1:{}</p>'.format(LI()))
        x42 = HTML('<p>Row 4 col 2:{}</p>'.format(LI()))
        x51 = HTML('<p>Row 5 col 1:{}</p>'.format(LI()))
        x521 = HTML('<p>Row 5 col 2 row 1:{}</p>'.format(LI()))
        x522 = HTML('<p>Row 5 col 2 row 2:{}</p>'.format(LI()))
        x5231 = HTML('<p>Row 5 col 2 row 3 col 1: {}</p>'.format(LI()))
        x5232 = HTML('<p>Row 5 col 2 row 3 col 2: {}</p>'.format(LI()))
        x5233 = HTML('<p>Row 5 col 2 row 3 col 3: {}</p>'.format(LI()))

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
                               '{}\n\n'.format(LI()) +
                               '{}\n\n'.format(LI()) +
                               '{}\n\n'.format(LI()))
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
                        RC(LI()),
                        RC(Markdown('#Button Panel')),
                        RXC6(('The button is in the left column.', bpn, bpc,
                              'The panel is in the right column', LI()),
                             (LI(), Markdown('#### Node panel will appear here'), pn,
                              LI(), Markdown('#### Company panel will appear here'), pc)
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
        mdl1 = Modal(RC(Markdown('#This is modal 1'), LI(), LI()))
        b1 = ButtonModal('Click to display modal 1', mdl1)
        mdl2 = Modal(RC(Markdown('#This is modal 2'), LI(), LI()))
        b2 = ButtonModal('Click to display modal 2', mdl2)
        mdl3 = Modal(LI(), LI(),
                     button='Modal 3 button',
                     header=Markdown('####Markdown header for modal 3'),
                     footer=(Button('A button'), 'This is the footer for modal 3',))
        self.content = (RC(LI()),
                        RCX('Text before buttons ', b1, b2, ' Text after buttons'),
                        RC(LI()),
                        RC(X('Text before button ', mdl3, ' Text after button')),
                        RC(LI()))
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
        c1r = Markdown('#### Content 1', LI())
        c2r = Markdown('#### Content 2', LI())
        c3r = Markdown('#### Content 3', LI())
        c4r = Markdown('#### Content 4', LI())
        c1l = Markdown('#### Content 1', LI())
        c2l = Markdown('#### Content 2', LI())
        c3l = Markdown('#### Content 3', LI())
        c4l = Markdown('#### Content 4', LI())
        crsl1 = Carousel(c1r, c2r, c3r, c4r)
        crsl2 = Carousel(c1l, c2l, c3l, c4l)
        self.content = (RC(LI()),
                        RX(C3(Markdown('**Panel on left**')), C9(crsl1)),
                        RC(LI()),
                        RX(C9(crsl2), C3(Markdown('**Panel on right**'))),
                        RC(LI())
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
