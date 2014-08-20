#!/usr/bin/env python
# coding=utf-8

"""
View and Test/Examples
**********************

.. module:: views
   :synopsis: Provides DPageView to process DPage request and various test/examples.

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

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

from djangopages.dpage import *
from djangopages.dpage_layout import *
from djangopages.dpage_bootstrap3 import *
from djangopages.dpage_graphs import *
from djangopages.dpage_texthtml import *
from django.http import HttpResponseNotFound
from django.views.generic import View

# todo 3: unused imports, shouldn't I have examples for these
# from test_data.models import syslog_query, syslog_event_graph, VNode, VCompany

########################################################################################################################
#
# Display and process a DPage
#
########################################################################################################################


class DPageView(View):
    """ DPageView provides url processing for DPage(s).  A DPage's class name defines its URL. DPageView
     may be used to process page references as follows:

    .. sourcecode:: python

        urlpatterns = patterns('',
                       url(r'^(.*$)', DPageView.as_view(), name='dpagesview'),
                       )

    .. note:: Additional urls may be defined for a DPage.

    """
    @staticmethod
    def get(request, name):
        """ get the named DPage

        :param request: the request object
        :type request: WSGIRequest
        :param name: DPage object class name
        :type name: str
        """
        try:
            # noinspection PyUnresolvedReferences
            dt = DPage.pages_dict[name]
            dpage = dt(request).page()
            return dpage.render()
        except KeyError:
            return HttpResponseNotFound('<h1>Page &lt;{}&gt; not found</h1>'.format(name))

    @staticmethod
    def post(request, name):
        """ post the named DPage

        :param request: the request object
        :type request: WSGIRequest
        :param name: DPage object class name
        :type name: str
        """
        # noinspection PyUnresolvedReferences
        dt = DPage.pages_dict[name]
        dpage = dt(request).page()
        return dpage.render()


########################################################################################################################
#
# Dpage that list the available DPage tests.
#
########################################################################################################################


class DPagesList(DPage):
    """
    Page to list DPages
    """
    title = 'DjangoPages List'
    description = 'List the test/demo DPages'
    tags = ['list_test']

    def page(self):
        """
        List available pages
        """
        t = '<a href="/dpages/{name}" ' \
            'class="btn btn-default btn-xs" ' \
            'role="button" ' \
            'style="width:400px;text-align:left;margin-bottom:2px;">' \
            '{text}' \
            '</a><br/>\n'
        # noinspection PyUnresolvedReferences
        pages = DPage.pages_list
        out = ''
        for page in pages:
            # get the class definition for this page
            cls = page['cls']
            # make a link button object to execute an instance of the class
            # lnk = Link('/dpages/{name}'.format(name=cls.__name__), cls.title)
            # lnkbtn = Button(lnk, btn_size='btn-xs')
            # Output a line with the link button, test title, and test description
            line = t.format(name=cls.__name__, text=cls.title)
            out += line
        self.content = out
        return self


########################################################################################################################
#
# Development test class based view support functions
#
########################################################################################################################


# def page_list_for_pages(pages):
#     """
#     Return content that will list the pages in pages.
#     """
#     out = []
#     for page in pages:
#         # get the class definition for this page
#         cls = page['cls']
#         # make a link button object to execute an instance of the class
#         lnk = Link('/dpages/{name}'.format(name=cls.__name__), SP()+cls.title,
#                    button='btn-default btn-sm btn-block',
#                    style='margin-top:5px; text-align:left;')
#         line = RC4(lnk)
#         # lnk = Link('/dpages/{name}'.format(name=cls.__name__), cls.title,
#         #            button='btn-primary btn-xs btn-block',
#         #            style='margin-top:5px; text-align:left;')
#         # lnkbtn = Button(lnk, btn_size='btn-xs')
#         # Output a line with the link button, test title, and test description
#         # line = R(X(C3(lnk), C6(cls.description)))
#         # line = RC(lnk)
#         out.append(line)
#     return out
#

# def doc_panel(dpage, text):
#     """
#     Support method to create the documentation panel for the examples/tests.
#     """
#     doc = Markdown(text)
#     doc_heading = Markdown('###{title}\n'
#                            '[Home](/dpages/DPagesList) [Prev](/dpages/{prev}) [Next](/dpages/{next})'
#                            .format(title=dpage.title, next=dpage.next(), prev=dpage.prev()))
#     panel = Panel(doc, heading=doc_heading)
#     return panel
#
#
# def content_panel(content):
#     """
#     Support function for content.
#     """
#     return Panel(content, heading=Markdown('###Output'))
#
#
# def page_content(dpage, text, content):
#     """
#     """
#     doc = doc_panel(dpage, text)
#     content = content_panel(content)
#     return R(C6(doc), C6(content))
#
#
# def page_content_v(dpage, text, content):
#     """
#     """
#     if content and len(content) > 0:
#         return R(C(doc_panel(dpage, text),
#                      MD('Below is the output for this page.'
#                         '<hr style="box-shadow: 0 0 10px 1px black;">'),
#                      content_panel(content)))
#     else:
#         return R(C(doc_panel(dpage, text)))


def page_content(dpage, code, output):
    template = '<h4>{title}</h4>' \
               '<a href="/dpages/DPagesList">Home </a>' \
               '<a href="/dpages/{prv}">Prev </a>' \
               '<a href="/dpages/{nxt}">Next</a>' \
               '<pre>{code}</pre>' \
               '<h4>Output for this code</h4>' \
               '<hr style="box-shadow: 0 0 10px 1px black;">' \
               '{output}'
    nxt = dpage.next()
    prv = dpage.prev()
    return template.format(title=dpage.title, code=code, output=output, nxt=nxt, prv=prv)


def escape(t):
    """HTML-escape the text in `t`."""
    return (t
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace("'", "&#39;").replace('"', "&quot;")
            )

########################################################################################################################
#
# Development test/demonstrations
#
########################################################################################################################


class TestText(DPage):
    """ TestText """
    title = 'Text: Text'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        code = escape("""
doc1 = Text('This is some Text content. ',
            'This is some more Text content.',
            '</br>Text can also output HTML.')
doc2 = T('Bisque packground style para', para=True, style='background-color:bisque;')
doc3 = T('Red templated text', template='<font color="red">{content}</font>')
content = doc1 + doc2 + doc3
        """)

        doc1 = Text('This is some Text content. ',
                    'This is some more Text content.',
                    '</br>Text can also output HTML.')
        doc2 = T('Bisque packground style para', para=True, style='background-color:bisque;')
        doc3 = T('Red templated text', template='<font color="red">{content}</font>')
        content = doc1 + doc2 + doc3
        self.content = page_content(self, code, content)
        return self


class TestMarkdown(DPage):
    """ TestMarkdown """
    title = 'Text: Markdown'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        code = """
content = Markdown('###Markdown h3\\n',
                   '**Markdown bold text**',
                   Markdown('*Embedded markdown object italic text.*'))
        """
        content = Markdown('###Markdown h3\n',
                           '**Markdown bold text**',
                           Markdown('*Embedded markdown object italic text.*'))
        self.content = page_content(self, code, content)
        return self


class TestLI(DPage):
    """ TestLI """
    title = 'Text: LI'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        code = """
content = T(LI(1, 2, 5),                                # make 3 paragraphs with different number of sentences
            LI(15, style='background-color:bisque;'))   # paragraph with background
        """

        # content = LI(1,2,3)
        content = T(LI(1, 2, 5),                                # make 3 paragraphs with different number of sentences
                    LI(15, style='background-color:bisque;'))   # paragraph with background
        self.content = page_content(self, code, content)
        return self


class TestPlusMul(DPage):
    """ TestPlusMul """
    title = 'Text: + and *'
    description = 'Demonstrate ' + title
    tags = ['text', 'content']

    def page(self):
        code = """
li = LI(12, style='background-color:bisque;')
content = li + li * 2

+ and * force immediate rendering of the widget.
        """
        li = LI(12, style='background-color:bisque;')
        content = li + li * 2

        self.content = page_content(self, code, content)
        return self


class TestBRSP(DPage):
    """ TestBRSP """
    title = 'Text: BR & SP'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        code = """
content = T('line brake here', BR(), 'second line', BR(2), 'third', SP(5), 'line', BR(), AS('*** ', 2))
        """

        content = T('line brake here', BR(), 'second line', BR(2), 'third', SP(5), 'line', BR(), AS('*** ', 2))
        self.content = page_content(self, code, content)
        return self


class TestMultipleWidgets(DPage):
    """ TestMultipleWidgets """
    title = 'Content: Multiple widgets on page'
    description = 'Demonstrate ' + title
    tags = ['content']

    def page(self):
        code = escape("""
content = T(Markdown('**Some bold Markdown text**'),
            HTML('<i><b>Some italic bold HTML text</b></i>'),
            Text('</br>Some Text text'),
            LI(3, 5))
        """)

        # noinspection PyListCreation
        content = T(Markdown('**Some bold Markdown text**'),
                    HTML('<i><b>Some italic bold HTML text</b></i>'),
                    Text('</br>Some Text text'),
                    LI(3, 5))
        self.content = page_content(self, code, content)
        return self


class TestColumn(DPage):
    """ TestColumn """
    title = 'Layout: Bootstrap 3 Column'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        code = escape("""
t = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
content = T('<div class="row">',
            C(t, width=3, style='background-color:powderblue;'),
            C6(t+'mighty ducks '*30, width=6, style='background-color:bisque;'),
            C3(t, style='background-color:violet'),
            '</div>')
        """)

        # Create some text for two rows
        t = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
        content = T('<div class="row">',
                    C(t, width=3, style='background-color:powderblue;'),
                    C6(t+'mighty ducks '*30, width=6, style='background-color:bisque;'),
                    C3(t, style='background-color:violet'),
                    '</div>')
        self.content = page_content(self, code, content)
        return self


class TestColumnList(DPage):
    """ TestColumnList """
    title = 'Layout: Bootstrap 3 Column List'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        code = escape("""
t1 = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
t2 = '<b>Ducks</b>' + 'Ducks ' * 70
content = T('<div class="row">',
            C6(t1, t2, style='border:1px solid;'),
            '</div>')
       """)

        t1 = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
        t2 = '<b>Ducks</b>' + 'Ducks ' * 70
        content = T('<div class="row">',
                    C6(t1, t2, style='border:1px solid;'),
                    '</div>')
        self.content = page_content(self, code, content)
        return self


class TestRow(DPage):
    """ TestRow """
    title = 'Layout: Bootstrap 3 Row'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        code = """
content = T(R(C6(LI(5), LI(2, 3), style='border:1px solid;')),
            R(C(LI(20, style='background-color:powderblue;'))))
        """

        # Create some text for two rows
        content = T(R(C6(LI(5), LI(2, 3), style='border:1px solid;')),
                    R(C(LI(20, style='background-color:powderblue;'))))
        self.content = page_content(self, code, content)
        return self


class TestRowColumn(DPage):
    """ TestRowColumn """
    title = 'Layout: Bootstrap 3 RowColumn/RC'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        code = """
 * RowColumn(content, [width=n]), or
        """

        # Create content
        content = RowColumn(LI(8), LI(5), width=6)
        self.content = page_content(self, code, content)
        return self


class TestMapRowColumn(DPage):
    """ TestMapRowColumn """
    title = 'Layout: Map RC'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        code = escape("""
li = LI(5, para=False).render()[0]
t = MD('**Text in a row column.** ' + li)
content = RC6M((t, t),
               (t, t), style='border:1px solid;')
        """)

        li = LI(5, para=False).render()[0]
        t = MD('**Text in a row column.** ' + li)
        content = RC6M((t, t),
                       (t, t), style='border:1px solid;')
        self.content = page_content(self, code, content)
        return self


class TestButton(DPage):
    """ TestButton """
    title = 'Buttons'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'buttons']

    def page(self):
        code = """
btn = Button('Button 1', 'Button 2')
content = RC2M((btn,),
               (BTN('Success', button='btn-success btn-xs'),),
               (BTN('Default'), BTN('Large button', button='btn-lg')),
               (BTN('Button 6')+BTN('Button 7'),),
               style='margin-top:2px;')

Note: These 6 lines of djangopage code generated approximately 170 lines of html! 30x productivity.
        """

        # define content objects
        btn = Button('Button 1', 'Button 2')
        content = RC2M((btn,),
                       (BTN('Success', button='btn-success btn-xs'),),
                       (BTN('Default'), BTN('Large button', button='btn-lg')),
                       (BTN('Button 6')+BTN('Button 7'),),
                       style='margin-top:2px;')
        self.content = page_content(self, code, content)
        return self


class TestGlyphicons(DPage):
    """ TestGlyphicons """
    title = 'Glyphicons'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'glyphicons', 'text']

    def page(self):
        code = """
content = RCM((Glyphicon('star'), GL('heart'), GL('music')),
              (GL('zoom-in'), GL('refresh'), GL('qrcode')))
        """

        # define the content
        content = RC2M((T('Three glyphs on a line: '), Glyphicon('star'), GL('heart'), GL('music')),
                       (T('Two then one glyph on a line:'), GL('zoom-in', 'refresh'), GL('qrcode')))
        self.content = page_content(self, code, content)
        return self


class TestJumbotron(DPage):
    """ TestJumbotron """
    title = 'Jumbotron'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'jumbotron', 'text']

    def page(self):
        code = escape("""
t = '#Heading\n' \
    'Some text after the heading.'
r1 = Jumbotron(MD(t))
r2 = Jumbotron(T(MD('#Jumbotron 2'), T('Some text'), Button('Button')))
content = RC(r1, r2)
        """)

        # define the content
        t = '#Heading\n' \
            'Some text after the heading.'
        r1 = Jumbotron(MD(t))
        r2 = Jumbotron(T(MD('#Jumbotron 2'), T('Some text'), Button('Button')))
        content = RC(r1, r2)
        self.content = page_content(self, code, content)
        return self


class TestLabel(DPage):
    """ TestLabel """
    title = 'Label'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'label', 'text']

    def page(self):
        code = escape("""
r1 = Label('default', 'Default',
           'primary', 'Primary',
           'success', 'Success')
r2 = '<h3>Example heading'+XS(Label('default', 'New'))+'</h3>'
content = RC(r1, r2)
        """)

        # define the content
        r1 = Label('default', 'Default',
                   'primary', 'Primary',
                   'success', 'Success')
        r2 = '<h3>Example heading'+XS(Label('default', 'New'))+'</h3>'
        content = RC(r1, r2)
        self.content = page_content(self, code, content)
        return self


class TestLink(DPage):
    """ TestLink """
    title = 'Link'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'link']

    def page(self):
        code = """
# define content objects
r1 = Link('/dpages/DPagesList', 'DPagesList link')
r2 = Link('/dpages/DPagesList', 'DPagesList link',
          button='btn-info btn-xs')
r3 = Link('/dpages/DPagesList', 'DPagesList link with style and classes',
          button='btn-success btn-lg',
          style='color:white;width:400px;margin-top:5px;margin-bottom:5px;')
r4 = Link('/dpages/DPagesList', 'DPagesList link',
          '/dpages/DPagesList', 'DPagesList link',
          button='btn-xs', style='margin:2px;')

# put into layout
content = RC(r1, r2, r3, r4)
        """

        # define content objects
        r1 = Link('/dpages/DPagesList', 'DPagesList link')
        r2 = Link('/dpages/DPagesList', 'DPagesList link',
                  button='btn-info btn-xs')
        r3 = Link('/dpages/DPagesList', 'DPagesList link with style and classes',
                  button='btn-success btn-lg',
                  style='color:white;width:400px;margin-top:5px;margin-bottom:5px;')
        r4 = Link('/dpages/DPagesList', 'DPagesList link',
                  '/dpages/DPagesList', 'DPagesList link',
                  button='btn-xs', style='margin:2px;')

        # put into layout
        content = RC(r1, r2, r3, r4)
        self.content = page_content(self, code, content)
        return self


class TestModal(DPage):
    """ TestModal """
    title = 'Modal'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'modal']

    def page(self):
        code = escape("""
mt = MD('####Modal title')
mb = T(MD('**Body**'), LI(5, 5, 5, 2))
mf = MD('**Modal footer**')
r1 = Modal(mt, mb, mf, 'Show modal')
r2 = Modal(mt, mb, mf, 'Show modal small', modal_size='modal-sm')
r3 = Modal(mt, mb, mf, 'Show modal button', button_type='btn-success btn-xs')

Note: Modal() generates 18 lines of active HTML for 1 line of definition!
Note: Actual HTML generated by 6 line test is 124!
        """)

        # define content objects
        mt = MD('####Modal title')
        mb = T(MD('**Body**'), LI(5, 5, 5, 2))
        mf = MD('**Modal footer**')
        r1 = Modal(mt, mb, mf, 'Show modal')
        r2 = Modal(mt, mb, mf, 'Show modal small', modal_size='modal-sm')
        r3 = Modal(mt, mb, mf, 'Show modal button', button_type='btn-success btn-xs')

        # put into layout
        content = RC(T(r1, r2), r3, style='padding-top:5px;')
        self.content = page_content(self, code, content)
        return self


class TestPanel(DPage):
    """ TestPanel """
    title = 'Panel'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'panel']

    def page(self):
        code = escape("""
r1 = Panel(MD('Panel text 1'), '')
r2 = Panel(MD('Panel text 2'), MD('####Panel heading 2'))
r3 = Panel(MD('Panel text 3'), MD('####Panel heading 3'),
           MD('Panel text 4'), MD('####Panel heading 4'))
        """)

        # define content objects
        r1 = Panel(MD('', 'Panel text 1'))
        r2 = Panel(MD('####Panel heading 2'), MD('Panel text 2'))
        r3 = Panel(MD('####Panel heading 3'), MD('Panel text 3'),
                   MD('####Panel heading 4'), MD('Panel text 4'))

        # put into layout
        content = RC(r1, r2, r3)
        self.content = page_content(self, code, content)
        return self


class TestAccordion(DPage):
    """ TestAccordion """
    title = 'Accordion'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'accordion']

    def page(self):
        code = escape("""
# define content objects
r1 = Accordion('Heading 1', LI(5,6),
               'Heading 2', LI(3,4,5),
               'Heading 3', LI(7,4,2))

# put into layout
content = RC(r1)
        """)

        # define content objects
        r1 = Accordion('Heading 1', LI(5, 6),
                       'Heading 2', LI(3, 4, 5),
                       'Heading 3', LI(7, 4, 2))

        # put into layout
        content = RC(r1)
        self.content = page_content(self, code, content)
        return self


class TestAccordionM(DPage):
    """ TestAccordionM """
    title = 'AccordionM'
    description = 'Demonstrate ' + title
    tags = ['bootstrap', 'accordionm']

    def page(self):
        code = escape("""
# define content objects
r1 = Accordion('Heading 1', LI(5,6),
               'Heading 2', LI(3,4,5),
               'Heading 3', LI(7,4,2))

# put into layout
content = RC(r1)
        """)

        # define content objects
        r1 = AccordionM('Heading 1', LI(5, 6),
                        'Heading 2', LI(3, 4, 5),
                        'Heading 3', LI(7, 4, 2))

        # put into layout
        content = RC(r1)
        self.content = page_content(self, code, content)
        return self


class TestBasicGraphs(DPage):
    """ TestBasicGraphs """
    title = 'Graphs'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        code = """
#
# see example source for data definitions
#

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
        """

        # data for chart
        browser_stats = [['Chrome', 52.9],
                         ['Firefox', 27.7],
                         ['Opera', 1.6],
                         ['Internet Explorer', 12.6],
                         ['Safari', 4]]
        exchange = {'2001-01-31': 1.064, '2002-01-31': 1.1305,
                    '2003-01-31': 0.9417, '2004-01-31': 0.7937,
                    '2005-01-31': 0.7609, '2006-01-31': 0.827,
                    '2007-01-31': 0.7692, '2008-01-31': 0.6801,
                    '2009-01-31': 0.7491, '2010-01-31': 0.7002,
                    '2011-01-31': 0.7489, '2012-01-31': 0.7755,
                    '2013-01-31': 0.7531,
                    }
        temperature = [{u'data': {'2012-00-01 00:00:00 -0700': 7,
                                  '2012-01-01 00:00:00 -0700': 6.9,
                                  '2012-02-01 00:00:00 -0700': 9.5,
                                  '2012-03-01 00:00:00 -0700': 14.5,
                                  '2012-04-01 00:00:00 -0700': 18.2,
                                  '2012-05-01 00:00:00 -0700': 21.5,
                                  '2012-06-01 00:00:00 -0700': 25.2,
                                  '2012-07-01 00:00:00 -0700': 26.5,
                                  '2012-08-01 00:00:00 -0700': 23.3,
                                  '2012-09-01 00:00:00 -0700': 18.3,
                                  '2012-10-01 00:00:00 -0700': 13.9,
                                  '2012-11-01 00:00:00 -0700': 9.6},
                        u'name': u'Tokyo'},
                       {u'data': {'2012-00-01 00:00:00 -0700': -0.2,
                                  '2012-01-01 00:00:00 -0700': 0.8,
                                  '2012-02-01 00:00:00 -0700': 5.7,
                                  '2012-03-01 00:00:00 -0700': 11.3,
                                  '2012-04-01 00:00:00 -0700': 17,
                                  '2012-05-01 00:00:00 -0700': 22,
                                  '2012-06-01 00:00:00 -0700': 24.8,
                                  '2012-07-01 00:00:00 -0700': 24.1,
                                  '2012-08-01 00:00:00 -0700': 20.1,
                                  '2012-09-01 00:00:00 -0700': 14.1,
                                  '2012-10-01 00:00:00 -0700': 8.6,
                                  '2012-11-01 00:00:00 -0700': 2.5},
                        u'name': u'New York'},
                       {u'data': {'2012-00-01 00:00:00 -0700': -0.9,
                                  '2012-01-01 00:00:00 -0700': 0.6,
                                  '2012-02-01 00:00:00 -0700': 3.5,
                                  '2012-03-01 00:00:00 -0700': 8.4,
                                  '2012-04-01 00:00:00 -0700': 13.5,
                                  '2012-05-01 00:00:00 -0700': 17,
                                  '2012-06-01 00:00:00 -0700': 18.6,
                                  '2012-07-01 00:00:00 -0700': 17.9,
                                  '2012-08-01 00:00:00 -0700': 14.3,
                                  '2012-09-01 00:00:00 -0700': 9,
                                  '2012-10-01 00:00:00 -0700': 3.9,
                                  '2012-11-01 00:00:00 -0700': 1},
                        u'name': u'Berlin'},
                       {u'data': {'2012-00-01 00:00:00 -0700': 3.9,
                                  '2012-01-01 00:00:00 -0700': 4.2,
                                  '2012-02-01 00:00:00 -0700': 5.7,
                                  '2012-03-01 00:00:00 -0700': 8.5,
                                  '2012-04-01 00:00:00 -0700': 11.9,
                                  '2012-05-01 00:00:00 -0700': 15.2,
                                  '2012-06-01 00:00:00 -0700': 17,
                                  '2012-07-01 00:00:00 -0700': 16.6,
                                  '2012-08-01 00:00:00 -0700': 14.2,
                                  '2012-09-01 00:00:00 -0700': 10.3,
                                  '2012-10-01 00:00:00 -0700': 6.6,
                                  '2012-11-01 00:00:00 -0700': 4.8},
                        u'name': u'London'}]
        areas = {'2013-07-27 07:08:00 UTC': 4, '2013-07-27 07:09:00 UTC': 3,
                 '2013-07-27 07:10:00 UTC': 2, '2013-07-27 07:04:00 UTC': 2,
                 '2013-07-27 07:02:00 UTC': 3, '2013-07-27 07:00:00 UTC': 2,
                 '2013-07-27 07:06:00 UTC': 1, '2013-07-27 07:01:00 UTC': 5,
                 '2013-07-27 07:05:00 UTC': 5, '2013-07-27 07:03:00 UTC': 3,
                 '2013-07-27 07:07:00 UTC': 3}

        # create the pie chart and set it's title & subtitle
        # log.debug('@@@@@ define Graph')
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

        # Layout the content on the page
        # content = RC(T(MD('##Can have other DjangoPage content on the page with the graph.'),
        #               pie_graph,
        #               MD('####Explanation of graph') + LI(8, 5)))
        content = T(pie_graph, column_graph, bar_graph,
                    line_graph, multi_line_graph,
                    area_graph)
        # log.debug('@@@@@ page_content')
        self.content = page_content(self, code, content)
        return self


class TestMultipleGraphs(DPage):
    """ TestMultipleGraphs """
    title = 'Multiple Graphs'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        code = """
browser_stats = [['Chrome', 52.9],
                 ['Firefox', 27.7],
                 ['Opera', 1.6],
                 ['Internet Explorer', 12.6],
                 ['Safari', 4]]

pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})
column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                         'title.text': 'Browser Stats',
                                                         'subtitle.text': 'Graphs may have subtitles'})
bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})
        """
        # data for chart
        browser_stats = [['Chrome', 52.9],
                         ['Firefox', 27.7],
                         ['Opera', 1.6],
                         ['Internet Explorer', 12.6],
                         ['Safari', 4]]

        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})

        content = T(RC(MD('##Can have other DjangoPage content on the page with the graph.')),
                    RC4(pie_graph, column_graph, bar_graph),
                    RC(MD('####Explanation of graph') + LI(8, 5)))
        self.content = page_content(self, code, content)
        return self


class TestMultipleGraphsInAccordionM(DPage):
    """ TestMultipleGraphsInAccordionM """
    title = 'Multiple Graphs in AccordionM'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        code = """
browser_stats = [['Chrome', 52.9], ['Firefox', 27.7], ['Opera', 1.6], ['Internet Explorer', 12.6], ['Safari', 4]]

pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})
column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                         'title.text': 'Browser Stats',
                                                         'subtitle.text': 'Graphs may have subtitles'})
bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})

content = T(RC(MD('##Can have other DjangoPage content on the page with the graph.')),
            AccordionM('Pie', pie_graph,
                       'Column', column_graph,
                       'Bar', bar_graph),
            RC(MD('####Explanation of graph') + LI(8, 5)))
        """
        browser_stats = [['Chrome', 52.9], ['Firefox', 27.7], ['Opera', 1.6],
                         ['Internet Explorer', 12.6], ['Safari', 4]]

        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})

        content = T(RC(MD('##Can have other DjangoPage content on the page with the graph.')),
                    AccordionM('Pie', pie_graph,
                               'Column', column_graph,
                               'Bar', bar_graph),
                    RC(MD('####Explanation of graph') + LI(8, 5)))
        self.content = page_content(self, code, content)
        return self


class TestMultipleGraphsInAccordionMInRow(DPage):
    """ TestMultipleGraphsInAccordionMInRow """
    title = 'Multiple Graphs in AccordionM in RC'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        code = """

        """
        browser_stats = [['Chrome', 52.9], ['Firefox', 27.7],
                         ['Opera', 1.6], ['Internet Explorer', 12.6], ['Safari', 4]]

        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})

        content = T(RC(MD('##Can have other DjangoPage content on the page with the graph.')),
                    RC4(AccordionM('Pie', pie_graph),
                        AccordionM('Column', column_graph),
                        AccordionM('Bar', bar_graph)),
                    RC(MD('####Explanation of graph') + LI(8, 5)))
        self.content = page_content(self, code, content)
        return self


# class TestBasicGraphsB(DPage):
#     """
#     Basic test of Graph facility with two graphs in a row.
#     """
#     title = 'Graphs'
#     description = 'Demonstrate ' + title
#     tags = ['graphs']
#
#     def page(self):
#         """
#         Override
#         """
#         ###################
#         # Get the DB data we need
#         ###################
#
#         # set the company and node since no form yet
#         company = 'BMC_1'
#         node = 'A0040CnBPGC1'
#
#         # get the syslog data for this company/node
#         qs = syslog_query(company, node)
#
#         # Count all the syslog records
#         all_count_host = qs.count()
#
#         # Get count by type data
#         xqs = qs.values('message_type').annotate(num_results=Count('id'))
#         # Format for bar chart
#         count_by_type = map(list, xqs.order_by('message_type').values_list('message_type', 'num_results'))
#         # Sort data for pie chart
#         count_by_type_sorted_by_count = sorted(count_by_type, lambda x, y: cmp(x[1], y[1]), None, True)
#
#         ###################
#         # Create the charts
#         ###################
#         # create the column chart and set it's title
#         col_graph = Graph('column', count_by_type)
#         col_graph.options = {'height': '400px',
#                              'title.text': 'Syslog records by type',
#                              'subtitle.text': '{} node {}'.format(company, node)}
#
#         # create the pie chart and set it's title
#         pie_graph = Graph('pie', count_by_type_sorted_by_count)
#         pie_graph.options = {'height': '400px',
#                              'title.text': 'Syslog records by type',
#                              'subtitle.text': '{} node {}'.format(company, node)}
#         ###################
#         # Create title and other page content
#         ###################
#         # put some explanation text above and below the charts
#         text_top = Markdown('### Error count by type for {} Node {} '.format(company, node) +
#                             'Total errors {}'.format(all_count_host))
#         text_bottom = Markdown('### Analysis\n'
#                                'Here is where the analysis can go.\n\n' +
#                                '{}\n\n'.format(LI()) +
#                                '{}\n\n'.format(LI()) +
#                                '{}\n\n'.format(LI()))
#         ###################
#         # Layout the content on the page
#         ###################
#         self.content = (RC(text_top),
#                         RC6((col_graph, pie_graph)),
#                         RC(text_bottom))
#         return self
#
#
# class Test05(DPage):
#     """
#     Multiple graphs on page with multiple kinds of graphs
#     """
#     title = 'DjangoPages_Test05'
#     description = 'Demonstrate syslog graphs and multi-panels'
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
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
#     tags = []
#
#     def page(self):
#         self.content = (RC(Link('/dpages/DPagesList', 'Link to list page')),
#                         RC(Link('/dpages/Test07', 'Link to the form test page')),
#                         RC(Markdown('#### Link buttons')),
#                         RC((Link('/dpages/DPagesList', 'Link to list page', button=True), ' ',
#                              Link('/dpages/Test07', 'Link to the form test page', button=True),)
#                             )
#                         )
#         return self
