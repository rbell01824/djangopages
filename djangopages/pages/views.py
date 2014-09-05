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

from djangopages.pages.dpage import *
from djangopages.widgets.layout import *
from djangopages.widgets.bootstrap import *
from djangopages.widgets.texthtml import *
from djangopages.widgets.graph import GraphCK
from djangopages.widgets.form import *

from django.http import HttpResponseNotFound
from django.views.generic import View
from django import forms

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
    def get(request, name, *args, **kwargs):
        """ get the named DPage

        :param request: the request object
        :type request: WSGIRequest
        :param name: DPage object class name
        :type name: str
        """
        try:
            # noinspection PyUnresolvedReferences
            dpage_obj = DPage.pages_dict[name]
            cls_obj = dpage_obj()
            rtn = cls_obj.get(request, *args, **kwargs)
            return rtn
        except KeyError:
            return HttpResponseNotFound('<h1>Page &lt;{}&gt; not found</h1>'.format(name))

    @staticmethod
    def post(request, name, *args, **kwargs):
        """ post the named DPage

        :param request: the request object
        :type request: WSGIRequest
        :param name: DPage object class name
        :type name: str
        """
        try:
            # noinspection PyUnresolvedReferences
            dpage_obj = DPage.pages_dict[name]
            cls_obj = dpage_obj()
            rtn = cls_obj.post(request, *args, **kwargs)
            return rtn
        except KeyError:
            return HttpResponseNotFound('<h1>Page &lt;{}&gt; not found</h1>'.format(name))


########################################################################################################################
#
# Dpage that list the available DPage tests.
#
########################################################################################################################


class DPagesList(DPage):
    """ Page to list test DPages """
    title = 'DjangoPages List'
    description = 'List the test/demo DPages'
    tags = ['test', 'list']

    # noinspection PyMethodMayBeStatic
    def generate(self, request, *args, **kwargs):
        t = '<a href="/dpages/{name}" ' \
            'class="btn btn-default btn-xs" ' \
            'role="button" ' \
            'style="width:400px;text-align:left;margin-bottom:2px;">' \
            '{text}' \
            '</a><br/>\n'
        # noinspection PyUnresolvedReferences
        pages = DPage.find('test')
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
        return out


########################################################################################################################
#
# Development test class based view support functions
#
########################################################################################################################


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
    rtn = template.format(title=dpage.description, code=code, output=output, nxt=nxt, prv=prv)
    return rtn


def escape(t):
    """HTML-escape the text in `t`.

    .. sourcecode:: python

        escape('<h3>A heading</h3>')

    :param t: Text to escape
    :type t: str or unicode
    :return: string with html characters escaped
    :rtype: str
    """
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
    """ Test Text widget """
    title = 'Text: Text'
    description = 'Demonstrate ' + title
    tags = ['test', 'text']

    def generate(self, request, *args, **kwargs):
        code = escape("""
doc1 = 'This is some Text content. This is some more Text content. </br>Text can also output HTML.'
doc2 = Text('Bisque packground style para', para=True, style='background-color:bisque;')
doc3 = Text('Red templated text', template='<font color="red">{content}</font>')
content = doc1 + doc2 + doc3
        """)

        doc1 = 'This is some Text content. This is some more Text content. </br>Text can also output HTML.'
        doc2 = Text('Bisque packground style para', para=True, style='background-color:bisque;')
        doc3 = Text('Red templated text', style='color:red;')
        content = doc1 + doc2 + doc3
        content = page_content(self, code, content)
        return content


class TestMarkdown(DPage):
    """ Test Markdown widget"""
    title = 'Text: Markdown'
    description = 'Demonstrate ' + title
    tags = ['test', 'text']

    def generate(self, request, *args, **kwargs):
        code = """
c1 = Markdown('###Markdown h3')
c2 = Markdown(('**Markdown bold text**',
               '*Embedded markdown object italic text.*',
               'Note: markdown always generates a paragraph.'))
content = c1 + c2
        """
        c1 = Markdown('###Markdown h3')
        c2 = Markdown(('**Markdown bold text**',
                       '*Embedded markdown object italic text.*',
                       'Note: markdown always generates a paragraph.'))
        content = c1 + c2
        content = page_content(self, code, content)
        return content


class TestLI(DPage):
    """ Test LI widget"""
    title = 'Text: LI'
    description = 'Demonstrate ' + title
    tags = ['test', 'text']

    def generate(self, request, *args, **kwargs):
        code = """
content = (LI(5, style='background-color:azure;') +
           LI((1, 2, 5)) +
           LI(15, style='background-color:bisque;'))
        """

        # content = LI(1,2,3)
        content = (LI(5, style='background-color:azure;') +
                   LI((1, 2, 5)) +
                   LI(15, style='background-color:bisque;'))
        content = page_content(self, code, content)
        return content


class TestBRSP(DPage):
    """ Test StringDup, BR, & SP widgets """
    title = 'Text: StringDup, BR, & SP'
    description = 'Demonstrate ' + title
    tags = ['test', 'text']

    def generate(self, request, *args, **kwargs):
        code = """
content = ('line brake here' + BR() +
           'Second line followed by two newlines' + BR(2) +
           'Third 5 spaces' + SP(5) + 'line' + BR() +
           'Six red * surrounded by ():(' + SD('***', 2, style='color:red;') + ')')
        """

        content = ('line brake here' + BR() +
                   'Second line followed by two newlines' + BR(2) +
                   'Third 5 spaces' + SP(5) + 'line' + BR() +
                   'Six red * surrounded by ():(' + SD('***', 2, style='color: red;') + ')')
        content = page_content(self, code, content)
        return content


class TestColumn(DPage):
    """ Test Column widget"""
    title = 'Bootstrap: Column'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = escape("""
t = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
c1 = C(t, width=3, style='background-color:powderblue;')
c6 = C6(t+'mighty ducks '*30, width=6, style='background-color:bisque;')
c3 = C3(t, style='background-color:violet')
cl = C3((t, t, t))
content = ('<div class="row">{}{}{}</div>'.format(c1, c6, c3) +
           '<div class="row">{}</div>'.format(cl))
        """)

        t = '<b>Some text</b> ' + 'Be kind to your web footed friends. ' * 15
        c1 = C(t, width=3, style='background-color:powderblue;')
        c6 = C6(t+'mighty ducks '*30, width=6, style='background-color:bisque;')
        c3 = C3(t, style='background-color:violet')
        cl = C3((t, t, t))
        content = ('<div class="row">{}{}{}</div>'.format(c1, c6, c3) +
                   '<div class="row">{}</div>'.format(cl))
        content = page_content(self, code, content)
        return content


class TestRow(DPage):
    """ Test Row  widget"""
    title = 'Bootstrap: Row'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = """
content = (R(C6((LI(5), LI((2, 3))), style='border:1px solid;')) +
           R(C(LI(20, style='background-color:powderblue;'))))
        """

        # Create some text for two rows
        content = (R(C6((LI(5), LI((2, 3))), style='border:1px solid;')) +
                   R(C(LI(20, style='background-color:powderblue;'))))
        content = page_content(self, code, content)
        return content


class TestRowColumn(DPage):
    """ Test RowColumn widget """
    title = 'Bootstrap: RowColumn/RC'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = """
t = LI(5, para=False)
content = RowColumn((('Row 1 Col 1 ' + t, 'Row 1 Col 2 ' + t),
                     ('Row 2 Col 1 ' + t, 'Row 2 Col 2 ' + t)),
                    width=6)
        """
        t = LI(5, para=False)
        content = RowColumn((('Row 1 Col 1 ' + t, 'Row 1 Col 2 ' + t),
                             ('Row 2 Col 1 ' + t, 'Row 2 Col 2 ' + t)),
                            width=6)
        content = page_content(self, code, content)
        return content


class TestRowRowColumn(DPage):
    """ Test RowRowColumn widget """
    title = 'Bootstrap: RowRowColumn/RRC'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = """
t = LI(5, para=False)
content = RowRowColumn((('Row 1 Col 1 ' + t, 'Row 1 Col 2 ' + t),
                     ('Row 2 Col 1 ' + t, 'Row 2 Col 2 ' + t)),
                    width=6)
        """
        t = LI(5, para=False)
        content = RowRowColumn((('Row 1 Col 1 ' + t, 'Row 1 Col 2 ' + t),
                                ('Row 2 Col 1 ' + t, 'Row 2 Col 2 ' + t)),
                               width=6)
        content = page_content(self, code, content)
        return content


class TestWList(DPage):
    """ Test WList widget """
    title = 'Bootstrap: WList'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = """
t = LI(5, para=False)
content = WL(R(WL(C2(t), C4(t))),
             R(WL(C4(t), C3(t), C2(t))))
        """
        t = LI(5, para=False)
        content = WL(R(WL(C2(t), C4(t))),
                     R(WL(C4(t), C3(t), C2(t))))
        content = page_content(self, code, content)
        return content


class TestLayout(DPage):
    """ Test Layout widget """
    title = 'Bootstrap: layout'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'layout']

    def generate(self, request, *args, **kwargs):
        code = """
t = LI(5, para=False)
content = WL(R(WL(C2(t), C4(t))),
             R(WL(C4(t), C3(t), C2(t))))
        """
        t = LI(5, para=False)
        content = Layout((C2(t), C4(t), C3(t)),
                         (C4(t), C3(t), C2(t)),
                         (C4(t), C5(t)))
        content = page_content(self, code, content)
        return content


class TestAccordion(DPage):
    """ Test Accordion widget """
    title = 'Bootstrap: Accordion'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = """
content = Accordion((AccordionPanel('<h3>heading 1</h3>', 'content 1', expand=True),
                     AccordionPanel(MD('###heading 2'), LI((3, 5, 12))))
        """
        content = Accordion((AccordionPanel('<h3>heading 1</h3>', 'content 1', expand=True),
                             AccordionPanelSuccess(MD('###heading 2'), LI((3, 5, 12)))))
        content = page_content(self, code, content)
        return content


class TestButton(DPage):
    """ Test Button widget """
    title = 'Buttons'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = """
btn = Button(('Button 1', 'Button 2'))
content = RC((btn,
              BTN('Success', button='btn-success btn-xs'),
              BTN('Default') + BTN('Large info button', button='btn-lg btn-info'),
              BTNXS('XSButton 6')+BTNXSSuccess('XS Sucess Button 7'),),
             style='margin-top:2px;')

Note: These 6 lines of djangopage code generated approximately 57 lines of html! 9x productivity!
        """

        btn = Button(('Button 1', 'Button 2'))
        content = RC((btn,
                      BTN('Success', button='btn-success btn-xs'),
                      BTN('Default') + BTN('Large info button', button='btn-lg btn-info'),
                      BTNXS('XSButton 6')+BTNXSSuccess('XS Sucess Button 7'),),
                     style='margin-top:2px;')
        content = page_content(self, code, content)
        return content


class TestGlyphicons(DPage):
    """ Test Glyphicons widget """
    title = 'Glyphicons'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = """
r1 = T('Three glyphs on a line: ') + Glyphicon('star') + GL('heart') + GL('music')
r2 = T('Two then one glyph on a line: ') + GL(('zoom-in', 'refresh')) + T(' some space ') + GL('qrcode')
content = RC((r1, r2, BTNSSuccess(GL('star')+'Success')))
        """

        r1 = T('Three glyphs on a line: ') + Glyphicon('star') + GL('heart') + GL('music')
        r2 = T('Two then one glyph on a line: ') + GL(('zoom-in', 'refresh')) + T(' some space ') + GL('qrcode')
        content = RC((r1, r2, BTNSSuccess(GL('star')+'Success')))
        # content = GL('star')
        content = page_content(self, code, content)
        return content


class TestHn(DPage):
    """ Test Hn widget """
    title = 'Hn'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
content = RC((H3('Level 3 heading'), H6('Level 6 heading')))
        """)

        content = RC((H3('Level 3 heading'), H6('Level 6 heading')))
        content = page_content(self, code, content)
        return content


class TestSmall(DPage):
    """ Test Small widget """
    title = 'Small'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
content = RC(H3('Level 3 heading'+Small(' subheading text')))
        """)

        content = RC(H3('Level 3 heading'+Small(' subheading text')))
        content = page_content(self, code, content)
        return content


class TestHeader(DPage):
    """ Test Header widget """
    title = 'Header'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
content = Header(H2('Level 2 heading'+Small(' subheading text')))
        """)

        content = Header((H2('Level 2 heading'+Small(' subheading text')),
                          H3('Level 3 heading')))
        # content = Header(H2('Level 2 heading'+Small(' subheading text')))
        content = page_content(self, code, content)
        return content


class TestJumbotron(DPage):
    """ Test Jumbotron widget """
    title = 'Jumbotron'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
t = '#Heading\n' \
    'Some text after the heading.'
r1 = Jumbotron(MD(t))
r2 = Jumbotron(T(MD('#Jumbotron 2'), T('Some text'), Button('Button')))
content = RC(r1, r2)
        """)

        t = '#Heading\n' \
            'Some text after the heading.'
        r1 = Jumbotron(MD(t))
        r2 = Jumbotron(MD('#Jumbotron 2') + 'Some text' + BTNSInfo('Button'))
        content = RC((r1, r2))
        content = page_content(self, code, content)
        return content


class TestLabel(DPage):
    """ Test Label widget """
    title = 'Label'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
content = RC(('<h3>Example label ' + Label('New') + '</h3>',
              H3('H3 header '+Label('h3 header')),
              Label('MD more or less ok')+MD('####MD level 4'),
              MD("### MD doesn't work well here"), Label('MD3')))
        """)

        content = RC(('<h3>Example label ' + Label('New') + '</h3>',
                      H3('H3 header '+Label('h3 header')),
                      Label('MD more or less ok')+MD('####MD level 4'),
                      MD("### MD doesn't work well here"), Label('MD3')))
        content = page_content(self, code, content)
        return content


class TestLink(DPage):
    """ Test Link widget """
    title = 'Link'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap', 'link']

    def generate(self, request, *args, **kwargs):
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
                  button='btn-info btn-xs', style='margin-top:5px;')
        r3 = Link('/dpages/DPagesList', 'DPagesList link with style and classes',
                  button='btn-success btn-lg',
                  style='color:white;width:400px;margin-top:5px;margin-bottom:5px;')
        r4 = LNKXSDanger('/dpages/DPagesList', 'DPagesList link')
        r5 = LNK('/dpages/DPagesList', 'DPagesList link', button='')

        content = RC((r1, r2, r3, r4, r5))
        content = page_content(self, code, content)
        return content


class TestPanel(DPage):
    """ Test Panel widget """
    title = 'Bootstrap: Panel'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = """
p1 = Panel('Default panel')
p2 = PanelPrimary('Primary panel')
p3 = PanelSuccess('Panel 3 success with string heading', 'Panel 3 heading success str')
p4 = PanelSuccess('Panel 4 success with string heading and footer',
                  'Panel 4 heading success str',
                  'Panel 4 footer str')
p5 = PanelWarning('Panel 5 warning with heading and footer',
                  PanelHeading('Panel 5 heading warning'),
                  PanelFooter('Panel 5 footer'))
p6 = PanelInfo(MD('MD panel body'), MD('###MD panel header'), MD('MD panel footer'))
content = RC((p1, p2, p3, p4, p5, p6))
        """
        p1 = Panel('Default panel')
        p2 = PanelPrimary('Primary panel')
        p3 = PanelSuccess('Panel 3 success with string heading', 'Panel 3 heading success str')
        p4 = PanelSuccess('Panel 4 success with string heading and footer',
                          'Panel 4 heading success str',
                          'Panel 4 footer str')
        p5 = PanelWarning('Panel 5 warning with heading and footer',
                          PanelHeading('Panel 5 heading warning'),
                          PanelFooter('Panel 5 footer'))
        p6 = PanelInfo(MD('MD panel body'), MD('###MD panel header'), MD('MD panel footer'))
        content = RC((p1, p2, p3, p4, p5, p6))
        # content = p5.render()
        content = page_content(self, code, content)
        return content


class TestPanelC(DPage):
    """ Test collapsable panel widget """
    title = 'Bootstrap: PanelC'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = """
content = Accordion((AccordionPanelM('<h3>heading 1</h3>', 'content 1', expand=True),
                     AccordionPanelM(MD('###heading 2'), LI((3, 5, 12))))
        """
        content = T([PanelC('<h3>heading 1</h3>', 'content 1', expand=True),
                     PanelCPrimary(MD('###heading 2'), LI((3, 5, 12)))])
        content = page_content(self, code, content)
        return content


class TestModal(DPage):
    """ Test Modal widget """
    title = 'Modal'
    description = 'Demonstrate ' + title
    tags = ['test', 'bootstrap']

    def generate(self, request, *args, **kwargs):
        code = escape("""
m_header = MD('####Modal header')
m_body = MD('**Body**' + LI(5, 5, 5, 2))
m_footer = MD('**Modal footer**')
r1 = Modal(m_header, m_body, m_footer, 'Show modal')
r2 = Modal(m_header, m_body, m_footer, 'Show modal small', modal_size='modal-sm')
r3 = Modal(m_header, m_body, m_footer, 'Show modal button', button_type='btn-success btn-xs')

Note: Modal() generates 18 lines of active HTML for 1 line of definition!
Note: Actual HTML generated by 6 line test is 124!
        """)

        m_header = MD('####Modal header')
        m_body = MD('**Body**' + LI([5, 5, 5, 2]))
        m_footer = MD('**Modal footer**')
        r1 = Modal('Modal header', 'Modal body', 'Modal footer')
        r2 = Modal(m_header, m_body, m_footer, 'Show modal small', modal_size='modal-sm')
        r3 = Modal(m_header, m_body, m_footer, 'Show modal button')
        r4 = Modal(m_header, m_body, '', ModalButton('Modal button', 'success', size='xs'))
        r5 = Modal(ModalHeader(MD('##MD modal header')),
                   ModalBody(m_body),
                   ModalFooter(m_footer),
                   'Test modal...')

        content = RC((T((r1, r2)), r3, r4, r5), style='padding-top:5px;')
        content = page_content(self, code, content)
        return content


class GraphData(object):
    """ Data for graph tests """
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


class TestBasicGraphs(DPage):
    """ Test basic graphs """
    title = 'Basic graphs'
    description = 'Demonstrate ' + title
    tags = ['test', 'graphs']

    def generate(self, request, *args, **kwargs):
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

        # create the pie chart and set it's title & subtitle
        # log.debug('@@@@@ define Graph')
        browser_stats = GraphData.browser_stats
        exchange = GraphData.exchange
        temperature = GraphData.temperature
        areas = GraphData.areas
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

        content = RC((pie_graph, column_graph, bar_graph,
                      line_graph, multi_line_graph,
                      area_graph))
        # log.debug('@@@@@ page_content')
        content = page_content(self, code, content)
        return content


class TestMultipleGraphs(DPage):
    """ Test multiple graphs in RC """
    title = 'Multiple graphs in RC'
    description = 'Demonstrate ' + title
    tags = ['test', 'graphs']

    def generate(self, request, *args, **kwargs):
        code = """
pie_graph = GraphCK('pie', GraphData.browser_stats, options={'height': '400px',
                                                             'title.text': 'Browser Stats',
                                                             'subtitle.text': 'Graphs may have subtitles'})
column_graph = GraphCK('column', GraphData.browser_stats, options={'height': '400px',
                                                             'title.text': 'Browser Stats',
                                                             'subtitle.text': 'Graphs may have subtitles'})
bar_graph = GraphCK('bar', GraphData.browser_stats, options={'height': '400px',
                                                             'title.text': 'Browser Stats',
                                                             'subtitle.text': 'Graphs may have subtitles'})
        """
        browser_stats = GraphData.browser_stats
        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})

        content = (RC(MD('##Can have other DjangoPage content on the page with the graph.')) +
                   R(C4((pie_graph, column_graph, bar_graph))) +
                   RC(MD('####Explanation of graph') + LI([8, 5])))
        content = page_content(self, code, content)
        return content


class TestMultipleGraphsInPanels(DPage):
    """ Test multiple graphs in panels """
    title = 'Multiple graphs in panels'
    description = 'Demonstrate ' + title
    tags = ['test', 'graphs']

    def generate(self, request, *args, **kwargs):
        code = """
pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})
column_graph = GraphCK('column', browser_stats, options={'height': '400px',
                                                         'title.text': 'Browser Stats',
                                                         'subtitle.text': 'Graphs may have subtitles'})
bar_graph = GraphCK('bar', browser_stats, options={'height': '400px',
                                                   'title.text': 'Browser Stats',
                                                   'subtitle.text': 'Graphs may have subtitles'})

content = T([RC(MD('##Can have other DjangoPage content on the page with the graph.')),
             Panel(pie_graph, 'Pie graph'),
             Panel(column_graph, 'Column graph'),
             Panel(bar_graph, 'Bar graph'),
             RC(MD('####Explanation of graph') + LI(8, 5))])
        """
        browser_stats = GraphData.browser_stats
        pie_graph = GraphCK('pie', browser_stats, options={'height': '400px',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})
        column_graph = GraphCK('column', browser_stats, options={'height': '400px', 'chart.width': '400',
                                                                 'title.text': 'Browser Stats',
                                                                 'subtitle.text': 'Graphs may have subtitles'})
        bar_graph = GraphCK('bar', browser_stats, options={'height': '400px', 'chart.width': '400',
                                                           'title.text': 'Browser Stats',
                                                           'subtitle.text': 'Graphs may have subtitles'})

        content = T([RC(MD('##Can have other DjangoPage content on the page with the graph.')),
                     RC4((PanelCInfo('Pie graph', pie_graph, expand=True),
                          PanelC('Column graph', column_graph),
                          PanelCPrimary('Bar graph', bar_graph))),
                     RC(MD('####Explanation of graph') + LI((8, 5)))])
        content = page_content(self, code, content)
        return content


class TestDForm001(DPage):
    """ DForm support """
    title = 'DForm support 001'
    description = 'Demonstrate ' + title
    tags = ['test', 'forms']

    code = """
class NameForm(forms.Form):
    name = forms.CharField(label='Your name', initial='Your name',
                           help_text='Enter your name', max_length=100)
    subject = forms.CharField(max_length=100, help_text='100 characters max.')
    message = forms.CharField(help_text='Message you would like to send')
    sender = forms.EmailField(help_text='A valid email address, please.')
    cc_myself = forms.BooleanField(required=False)

def get(self, request, *args, **kwargs):
    form = self.NameForm(initial={'name': 'Enter your name here'})
    reset = LNKSPrimary('/dpages/TestDForm001', 'Reset')
    form = DForm(request, form)
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)

def post(self, request, *args, **kwargs):
    form = self.NameForm(request.POST)
    reset = LNKSPrimary('/dpages/TestDForm001', 'Reset')
    if form.is_valid():
        content = RC((reset, MD("### Success")))
        content = page_content(self, self.code, content)
        return self.render(request, content)
    form = DForm(request, form, 'table', 'Fire phasers', '/dpages/TestDForm001')
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)
        """

    class NameForm(forms.Form):
        name = forms.CharField(label='Your name', initial='Your name',
                               help_text='Enter your name', max_length=100)
        subject = forms.CharField(max_length=100, help_text='100 characters max.')
        message = forms.CharField(help_text='Message you would like to send')
        sender = forms.EmailField(help_text='A valid email address, please.')
        cc_myself = forms.BooleanField(required=False)

    def get(self, request, *args, **kwargs):
        form = self.NameForm(initial={'name': 'Enter your name here'})
        reset = LNKSPrimary('/dpages/TestDForm001', 'Reset')
        form = DForm(request, form)
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)

    def post(self, request, *args, **kwargs):
        form = self.NameForm(request.POST)
        reset = LNKSPrimary('/dpages/TestDForm001', 'Reset')
        if form.is_valid():
            content = RC((reset, MD("### Success")))
            content = page_content(self, self.code, content)
            return self.render(request, content)
        form = DForm(request, form, 'table', 'Fire phasers', '/dpages/TestDForm001')
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)


class TestDBForm001(DPage):
    """ DBForm support """
    title = 'Django DBForm support 001'
    description = 'Demonstrate ' + title
    tags = ['test', 'forms']

    code = """
class NameForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    myname = forms.CharField(label='My very long name', max_length=100)

def get(self, request, *args, **kwargs):
    form = self.NameForm(initial={'name': 'Enter your name here'})
    reset = LNKSPrimary('/dpages/TestDBForm001', 'Reset')
    form = DBForm(request, form, 'Fire phasers', width=(2, 4))
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)

def post(self, request, *args, **kwargs):
    form = self.NameForm(request.POST)
    reset = LNKSPrimary('/dpages/TestDBForm001', 'Reset')
    if form.is_valid():
        content = RC((reset, MD("### Success")))
        content = page_content(self, self.code, content)
        return self.render(request, content)
    form = DBForm(request, form, 'Fire phasers', width=(2, 4))
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)
        """

    class NameForm(forms.Form):
        name = forms.CharField(label='Your name', max_length=100)
        myname = forms.CharField(label='My very long name', max_length=100)

    def get(self, request, *args, **kwargs):
        form = self.NameForm(initial={'name': 'Enter your name here'})
        reset = LNKSPrimary('/dpages/TestDBForm001', 'Reset')
        form = DBForm(request, form, 'Fire phasers', width=(2, 4))
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)

    def post(self, request, *args, **kwargs):
        form = self.NameForm(request.POST)
        reset = LNKSPrimary('/dpages/TestDBForm001', 'Reset')
        if form.is_valid():
            content = RC((reset, MD("### Success")))
            content = page_content(self, self.code, content)
            return self.render(request, content)
        form = DBForm(request, form, 'Fire phasers', width=(2, 4))
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)


class TestDBForm002(DPage):
    """ DBForm support """
    title = 'Django DBForm support 002 (with help)'
    description = 'Demonstrate ' + title
    tags = ['test', 'forms']

    code = """
class NameForm(forms.Form):
    name = forms.CharField(label='Your name', initial='Your name',
                           help_text='Enter your name', max_length=100)
    subject = forms.CharField(max_length=100, help_text='100 characters max.')
    message = forms.CharField(help_text='Message you would like to send')
    sender = forms.EmailField(help_text='A valid email address, please.')
    cc_myself = forms.BooleanField(required=False)

    class Meta:
        foobar = 'something'

def get(self, request, *args, **kwargs):
    form = self.NameForm(initial={'name': 'Enter your name here'})
    # for f in form.fields:
    #     print f
    reset = LNKSPrimary('/dpages/TestDForm002', 'Reset')
    form = DBForm(request, form, 'Fire phasers', '/dpages/TestDBForm002')
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)

def post(self, request, *args, **kwargs):
    form = self.NameForm(request.POST)
    reset = LNKSPrimary('/dpages/TestDBForm002', 'Reset')
    if form.is_valid():
        content = RC((reset, MD("### Success")))
        content = page_content(self, self.code, content)
        return self.render(request, content)
    # for f in form.fields:
    #     print f
    form = DBForm(request, form, 'Fire phasers', '/dpages/TestDBForm002')
    content = RC((reset, form))
    content = page_content(self, self.code, content)
    return self.render(request, content)
        """

    class NameForm(forms.Form):
        name = forms.CharField(label='Your name', initial='Your name',
                               help_text='Enter your name', max_length=100)
        subject = forms.CharField(max_length=100, help_text='100 characters max.')
        message = forms.CharField(help_text='Message you would like to send')
        sender = forms.EmailField(help_text='A valid email address, please.')
        cc_myself = forms.BooleanField(required=False)

        class Meta:
            foobar = 'something'

    def get(self, request, *args, **kwargs):
        form = self.NameForm(initial={'name': 'Enter your name here'})
        for f in form.fields:
            print f
        reset = LNKSPrimary('/dpages/TestDForm002', 'Reset')
        form = DBForm(request, form, 'Fire phasers', '/dpages/TestDBForm002')
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)

    def post(self, request, *args, **kwargs):
        form = self.NameForm(request.POST)
        reset = LNKSPrimary('/dpages/TestDBForm002', 'Reset')
        if form.is_valid():
            content = RC((reset, MD("### Success")))
            content = page_content(self, self.code, content)
            return self.render(request, content)
        # for f in form.fields:
        #     print f
        form = DBForm(request, form, 'Fire phasers', '/dpages/TestDBForm002')
        content = RC((reset, form))
        content = page_content(self, self.code, content)
        return self.render(request, content)

class FLD(object):
    def __init__(self, fld):
        self.field = fld

class TestBForm001(DPage):
    """ Bootstrap form support """
    title = 'Bootstrap BForm support 001'
    description = 'Demonstrate ' + title
    tags = ['test', 'forms']

    code = """
class NameForm(forms.Form):
        """

    class TestForm(Form):
        name = forms.CharField(label='Your name', initial='Your name',
                               help_text='Enter your name', max_length=100)
        subject = forms.CharField(max_length=100, help_text='100 characters max.')
        message = forms.CharField(help_text='Message you would like to send')
        # sender = forms.EmailField(help_text='A valid email address, please.')
        cc_myself = forms.BooleanField(required=False)

        class Meta:
            button = 'Submit'
            method = 'Post'
            form_type = 'horizontal'
            layout = [FLD('name'), FLD('subject')]

    def reset_link(self):
        reset = LNKSPrimary('/dpages/TestBForm001', 'Reset')
        return reset

    def get(self, request, *args, **kwargs):
        reset = self.reset_link()
        form = self.TestForm(request)
        # for f in form.fields:
        #     print f
        content = Layout(C(reset), C6(form))
        content = page_content(self, self.code, content)
        return self.render(request, content)

    def post(self, request, *args, **kwargs):
        form = self.TestForm(request)
        reset = self.reset_link()
        if form.is_valid():
            content = RRC((reset, MD("### Success")))
            content = page_content(self, self.code, content)
            return self.render(request, content)
        # for f in form.fields:
        #     print f
        content = Layout(C(reset), C6(form))
        content = page_content(self, self.code, content)
        return self.render(request, content)
