#!/usr/bin/env python
# coding=utf-8

""" Test/Demo view functions

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
from test_data.models import syslog_query, syslog_event_graph, VNode, VCompany

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

        doc = """
DjangoPages provides a set of technologies to quickly and easily:

 * Create responsive Django web pages using Bootstrap 3 and jQuery
 * Draw web page content from Django and related databases

The links below provide an introduction to DJangoPages.
        """
        content = (MD(doc),
                   page_list_for_pages(DPage.find('toc')))
        self.content = page_content_v(self, content, None)

        return self


class DPagesAll(DPage):
    """
    List all dpage pages
    """
    title = 'All'
    description = 'List all DjangoPages'
    tags = ['toc']

    def page(self):
        # noinspection PyUnresolvedReferences
        self.content = page_content_v(self, page_list_for_pages(DPage.pages_list), None)
        return self


class DPagesOverview(DPage):
    """
    List overview pages
    """
    title = 'DjangoPages Overview'
    description = 'List Overview DjangoPages'
    tags = ['toc']

    def page(self):
        doc = """
DjangoPages provides a set of technologies to quickly and easily:

 * Create responsive Django web pages using Bootstrap 3 and jQuery
 * Draw web page content from Django and related databases
        """
        content = (MD(doc), page_list_for_pages(DPage.find('overview')))
        self.content = page_content_v(self, content, None)

        return self


class DPagesText(DPage):
    """
    List text related pages
    """
    title = 'DjangoPages Text Widgets'
    description = 'List Text Widget DjangoPages'
    tags = ['toc']

    def page(self):
        doc = """
DjangoPages provides a variety of **_text_** widgets.
        """
        content = (MD(doc), page_list_for_pages(DPage.find('text')))
        self.content = page_content_v(self, content, None)
        return self

########################################################################################################################
#
# Development test class based view support functions
#
########################################################################################################################


def page_list_for_pages(pages):
    """
    Return content that will list the pages in pages.
    """
    out = []
    for page in pages:
        # get the class definition for this page
        cls = page['cls']
        # make a link button object to execute an instance of the class
        lnk = Link('/dpages/{name}'.format(name=cls.__name__), SP()+cls.title,
                   button='btn-default btn-sm btn-block',
                   style='margin-top:5px; text-align:left;')
        line = RC4(lnk)
        # lnk = Link('/dpages/{name}'.format(name=cls.__name__), cls.title,
        #            button='btn-primary btn-xs btn-block',
        #            style='margin-top:5px; text-align:left;')
        # lnkbtn = Button(lnk, btn_size='btn-xs')
        # Output a line with the link button, test title, and test description
        # line = R(X(C3(lnk), C6(cls.description)))
        # line = RC(lnk)
        out.append(line)
    return out


def doc_panel(dpage, text):
    """
    Support method to create the documentation panel for the examples/tests.
    """
    doc = Markdown(text)
    doc_heading = Markdown('###{title}\n'
                           '[Home](/dpages/DPagesList) [Prev](/dpages/{prev}) [Next](/dpages/{next})'
                           .format(title=dpage.title, next=next_dpage(dpage), prev=prev_dpage(dpage)))
    panel = Panel(doc, heading=doc_heading)
    return panel


def content_panel(content):
    """
    Support function for content.
    """
    return Panel(content, heading=Markdown('###Output'))


def page_content(dpage, text, content):
    """
    """
    doc = doc_panel(dpage, text)
    content = content_panel(content)
    return R(X(C6(doc), C6(content)))


def page_content_v(dpage, text, content):
    """
    """
    if content and len(content) > 0:
        return R(C(X(doc_panel(dpage, text),
                     MD('Below is the output for this page.'
                        '<hr style="box-shadow: 0 0 10px 1px black;">'),
                     content_panel(content))))
    else:
        return R(C(doc_panel(dpage, text)))

########################################################################################################################
#
# Development test/demonstrations
#
########################################################################################################################


class DPageConcepts000(DPage):
    title = 'Overview: DjangoPages Concepts'
    description = title
    tags = ['overview']

    def page(self):
        doc = """
DjangoPages is built on a few simple concepts uniformly applied.

Each Django page must

 * **inherit from the DPage class** and
 * **override the base class page method** by defining the page content, ie.
 it must set self.content to the page's html content.

To make it easy to create the page, DjangoPages provides a rich collection
of widgets to:

 * Create content for the page.  Widgets provide for text, html, markdown, graph, tables, etc.
 * Create a responsive page layout using Bootstrap 3's grid technology

DjangoPage widgets can be easily extended and modified.
        """

        self.content = page_content_v(self, doc, None)
        return self


class DPageConcepts002(DPage):                      # The class name also defines the page's URL
    title = 'Overview: DjangoPages Definition'      # Define the page title
    description = title                             # Set the page's description
    tags = ['overview']                             # Pages may have tags to facilitate searching

    def page(self):                                 # Override the page method to generate the page's HTML

        # Create some page content
        doc = """
The source for a DjangoPage generally looks something like this:

    class Test000b(DPage):                              # The class name also defines the page's URL
        title = 'Overview: DjangoPages Definition'      # Define the page title
        description = title                             # Set the page's description
        tags = ['overview']                             # Pages may have tags to facilitate searching

        def page(self):                                 # Override the page method to generate the page's HTML

            # Create content panel
            doc_heading = Markdown('### DjangoPage Overview')       # Create heading using markdown
            doc = 'This is the panel body'                          # Create body using markdown
            doc = Markdown(doc)
            doc_panel = Panel(doc, heading=doc_heading)             # Create the panel

            # Create layout and save panel
            column = Column(doc_panel)                              # Put it in a bootstrap 3 column
            row = Row(column)                                       # Put the column in a bootstrap 3 row
            self.content = row                                      # set our content
            return self

The code is generally self descriptive.

 * Markdown creates a markdown object.
 * Panel(doc, heading=doc_heading)) creates a bootstrap 3 panel with a heading
 * Column() creates a full width bootstrap 3 column to contain the panel. C() is a shortcut for Column().
 * Row() creates a bootstrap 3 row that contains the column. R() is a shortcut for Row().

Most DjangoPages follow this general pattern.

 * Page content is created
 * The content is put in a layout

While the page could be written in this fashion, most pages take advantage of various convenience
methods and techniques to reduce the code count.  Many of these techniques are introduced in the
tests that follow.
        """

        # Put the content in a bootstrap 3 responsive grid
        self.content = Row(Column(doc_panel(self, doc)))
        return self


class DPageConcepts003(DPage):
    title = 'Overview: DjangoPages Definition 2'
    description = title
    tags = ['overview']

    def page(self):
        doc = """
In practice DjangoPages are much less verbose than the first example.  Generally the page
would look something like this:

    class Test000b(DPage):
        title = 'Overview: DjangoPages Definition'
        description = title
        tags = ['overview']

        def page(self):
            doc_panel = Panel(MD('This is the panel body',
                              MD('### DjangoPage Overview'))
            self.content = RC(doc_panel)
            return self

DjangoPages provides a number of convenience methods and abbreviations to simplify page creation
and reduce code.
        """

        # Put the content in a bootstrap 3 responsive grid
        self.content = Row(Column(doc_panel(self, doc)))
        return self


class DPageConcepts004(DPage):
    title = 'Overview: DjangoPage Widgets'
    description = title
    tags = ['overview']

    def page(self):
        doc = '''
Much of DjangoPage's utility comes from DjangoPage widgets. You have already seen several and will encounter
others in these tests/examples.

Widgets must

 * Inherit from Content
 * Initialize any custom arguments they use
 * Override the default render method and return the widgets result HTML

DjangoPage widgets are generally simple and easy to create.  They look something like this:

    class Glyphicon(Content):
        """
        Convenience method to output bootstrap 3 glyphicons
        """

        template = """
        <span {classes} {style}></span>
        """

        def __init__(self, content, classes='', style='', template=None):
            super(Glyphicon, self).__init__(content, classes, style, template)
            return

        def render(self):
            extra = 'glyphicon glyphicon-{}'.format(self.content)
            content, classes, style, template = self.render_setup(extra_classes=extra)
            out = template.format(style=style,
                                  classes=classes)
            return out

    GL = functools.partial(Glyphicon)

Many widgets, not all, contain a template.  The template simply defines some html that the widget
customizes based on its arguments.

The __init__ method is responsible for initializing the base class and saving any custom arguments the
widget uses.

All widgets take
 * content: The widget's content. Typically, data central to the widget's output.
 * classes: Any additional classes to be applied to the widget.
 * style: Any additional styles to be applied to the widget.
 * template: Value that will override the widget's default template.

The render method is responsible for generating the widget's html output.  Generally, it creates any extra
classes and/or styles and uses self.render_setup() to create final values for the widget's content, classes,
style, and template.

render_setup will evaluates methods used to define the widget's content, classes, style, and template. This is
an extremely important service as it allows the use of other widgets to create these elements.
        '''

        # Put the content in a bootstrap 3 responsive grid
        self.content = Row(Column(doc_panel(self, doc)))
        return self


class DPageConcepts005(DPage):
    title = 'Overview: DjangoPages page processing'
    description = title
    tags = ['overview']

    def page(self):
        doc = """
When a DjangoPage is created its URL is defined based on the page's class name.  It is not necessary to
create a urls.py entry.  Convenience methods are planned to facilitate control of the site url namespace.

When the url is used the page is rendered as follows:

 * The page's render method is executed.  As a general proposition DjangoPages need not and should not
   override the DPage render method.
 * The Dpage render method renders each element of self.content
 * The results are concatenated
 * The results are passed to the page's template and a response object returned

The end result is that DjangoPages render using the underlying Django render/response methods.
        """

        self.content = R(C(doc_panel(self, doc)))
        return self


class DPageConcepts006(DPage):
    title = 'Overview: DjangoPages test/examples'
    description = title
    tags = ['overview']

    def page(self):
        doc = """
The tests in this list were originally created during development to validate DjangoPage
functionality.  They provide an introduction to DjangoPages and its features.

It was necessary to use some features before they are introduced.  However, if you
study the test in order you will encounter all DjangoPage's features in a reasonably tutorial
fashion.

Note, the initial examples are intentionally verbose so they may be more easily understood.
As the examples proceed, they become less verbose and more production oriented.
        """

        self.content = R(C(doc_panel(self, doc)))
        return self


class TestTextHTML(DPage):
    title = 'Text: Text/HTML'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """
Text(content_1, ...)
T(content_1, ...)
HTML(content_1, ...)

 * contents: text to output

The Text and HTML widgets simply output their content.  They do not add an HTML wrapper.

 * Multiple content is concatenated.
 * Text, T, and HTML can be used interchangeably.
 * If content is an object, the output of it's render method is used.  This allows
   inclusion of the output of other DjangoPage widgets, ex. Markdown.

####Code
    content = Text('This is some Text content. ',
                   'This is some more Text content.',
                   '</br>Text can also output HTML.',
                   Markdown('**Embedded markdown bold text.**'),
                   Markdown(' *Embedded markdown italic text.*'
                            ' Note, Markdown wraps its output in an HTML paragraph.'))

    or HTML

    content = HTML('<strong>This is some strong HTML content.</strong> ',
                   '<i>This is some italic HTML content.</i>',
                   '</br><u>Text can also output underlined HTML.</u>',
                   Markdown('**Embedded markdown bold text.**'))

    or T convenience method

    content = T('<strong>This is some strong HTML content.</strong> ',
                '<i>This is some italic HTML content.</i>',
                '</br><u>Text can also output underlined HTML.</u>',
                Markdown('**Embedded markdown bold text.**'))
**Note: These examples use a responsive bootstrap 3 grid layout. This will be explained in subsequent
examples/test.  You can see the responsive behavior by adjusting the browser width.**
        """

        content = Text('This is some Text content. ',
                       'This is some more Text content.',
                       '</br>Text can also output HTML.',
                       Markdown('**Embedded markdown bold text.**'),
                       Markdown(' *Embedded markdown italic text.*'
                                ' Note, Markdown wraps its output in an HTML paragraph.'))
        self.content = page_content(self, doc, content)
        return self


class TestMarkdown(DPage):
    title = 'Text: Markdown'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """

Markdown(*content, **kwargs)

 * content: markdown text
 * kwargs: keyword args
    * extensions: markdown extensions

Markdown renders markdown text.  Note it may also contain HTML.

####Code
    content = Markdown('###Markdown h3',
                       '**Markdown bold text**',
                       Markdown('*Embedded markdown object italic text.*'))

    or M convenience method

    content = M('###Markdown h3',
                '**Markdown bold text**',
                M('*Embedded markdown object italic text.*'))
        """

        content = Markdown('###Markdown h3',
                           '**Markdown bold text**',
                           Markdown('*Embedded markdown object italic text.*'))
        self.content = page_content(self, doc, content)
        return self


# noinspection PyPep8Naming
class TestLIParagraph(DPage):
    title = 'Text: LIParagraph'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """
LI_para(amount=1, para=True)

 * **amount** is the number of loremipsum paragraphs to generate
 * **para** if true wraps each paragraph in an HTML paragraph

####Code
    content = LIParagraph(2)       # Make two loremipsum paragraphs

As a practical matter LI is far more frequently used than LIParagraph.
        """

        content = LIParagraph(2)       # Make two loremipsum paragraphs
        self.content = page_content(self, doc, content)
        return self


# noinspection PyPep8Naming
class TestLISentence(DPage):
    title = 'Text: LISentence'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """
LISentence(amount=1, para=True)

 * **amount** is the number of loremipsum sentences to generate
 * **para** if true wraps the sentences in an HTML paragraph

####Code
    content = LISentence(5)        # make one loremipsum paragraph of 5 sentences

As a practical mater LI is far more frequently used than LISentence.
        """

        content = LISentence(5)        # make one loremipsum pragraph of 5 sentences
        self.content = page_content(self, doc, content)
        return self


class TestLI(DPage):
    title = 'Text: LI'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """
LI(amount=1, para=True)

* **amount** is
    * the number of pragraphs to generate or
    * a list of paragraph lengths in sentences
* **para** if true wraps the paragraphs in an HTML paragraph

By using amount=[n, n,...] you can control the paragraph length.

####Code
    content = LI([1, 2, 5])     # make 3 paragraphs with different number of sentences
        """

        content = LI([1, 2, 5])         # make 3 paragraphs with different number of sentences
        self.content = page_content(self, doc, content)
        return self


class TestPlusMul(DPage):
    title = 'Text: + and *'
    description = 'Demonstrate ' + title
    tags = ['text', 'content']

    def page(self):
        doc = """
DjangoPage widgets support the string methods + and *.

####Code
    content = LISentence(2) + LISentence(2) + \\
        '<p>' + Text('This phrase will output 3 times.  ') * 3 + '</p>'
        """
        content = LISentence(2) + LISentence(2) + \
            '<p>' + Text('This phrase will output 3 times.  ') * 3 + '</p>'

        self.content = page_content(self, doc, content)
        return self


class TestBRSP(DPage):
    title = 'Text: BR & SP'
    description = 'Demonstrate ' + title
    tags = ['text']

    def page(self):
        doc = """
Sometimes it is useful to output multiple spaces or new lines.

 * BR(amount=1)
    * amount: number of &lt;br/&gt; to output
 * SP(amount=1)
    * amount: number of &amp;nbsp; to output

####Code
    content = (R(C(MD('####SP'))),
               R(C(('two', SP(), 'words'))),
               R(C(MD('####BR'))),
               R(C(('two', BR(), 'lines'))))

R(C((..., ...))) will be explained shortly.
        """

        content = (Row(C(MD('####SP'))),
                   R(C(('two', SP(), 'words'))),
                   R(C(MD('####BR'))),
                   R(C(('two', BR(), 'lines'))))
        self.content = page_content(self, doc, content)
        return self

# fixme: move this to overview


class TestSequence(DPage):
    title = 'Content: Widget sequence arguments'
    description = 'Demonstrate ' + title
    tags = ['content']

    def page(self):
        doc = """
Most DjangoPage widgets take a single content argument. However, it is often convenient to combine
the output of multiple widgets as the content of another widget.

Wrapping the inner widgets in a sequence allows the combined arguments to be passed as a single content
argument.

    R(C(('two ', 'words')))

is more convenient and generally clearer than

    r = 'two ' + 'words'
    R(C(r))

If you wish you can make this more explicit with the X widget that renders its arguments and
concatenates the result.

    R(C(X('two ', 'words')))
        """

        self.content = page_content_v(self, doc, '')
        return self


class TestMultipleWidgets(DPage):
    title = 'Content: Multiple widgets on page'
    description = 'Demonstrate ' + title
    tags = ['content']

    def page(self):
        doc = """
Multiple widgets can be combined on a page as previously illustrated.

####Code
    content = []
    content.append(Markdown('**Some bold Markdown text**'))
    content.append(HTML('<i><b>Some italic bold HTML text</b></i>'))
    content.append(Text('</br>Some Text text'))
    content.append(LI([3, 5]))
        """

        # noinspection PyListCreation
        content = []
        content.append(Markdown('**Some bold Markdown text**'))
        content.append(HTML('<i><b>Some italic bold HTML text</b></i>'))
        content.append(Text('</br>Some Text text'))
        content.append(LI([3, 5]))
        self.content = page_content(self, doc, content)
        return self


class TestClassesStyles(DPage):
    title = 'Content: Widget classes and styles'
    description = 'Demonstrate ' + title
    tags = ['content']

    def page(self):
        doc = """
It is generally convenient to pass extra classes and styles to widgets.

Most DjangoPage widgets take

 * classes='list of additional classes'
 * styles='additional styles'

arguments.

####Code
    content = (Row(C(LI([5])), style='border-style:solid;border-color:red;'),
               Row((C6(LI([2]), style='border-style:solid;border-width:1px'),
                    C6(LI([2]), style='border-style:solid;border-width:1px'))))
        """

        content = (Row(C(LI([5])), style='border-style:solid;border-color:red;'),
                   Row((C6(LI([2]), style='border-style:solid;border-width:1px'),
                        C6(LI([2]), style='border-style:solid;border-width:1px'))))
        self.content = page_content(self, doc, content)
        return self


class TestRowColumn(DPage):
    title = 'Layout: Bootstrap 3 Row/Column'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        doc = """
 * Row(content, classes='', style='', template=None)
 * R(...)
     * content: the row content
     * classes: other class for the widget
     * style: styles for the widget
     * template: override default template
 * Column(content, width=12, classes='', style='', template=None)
 * C(...)
     * content: the column content
     * classes: other class for the widget
     * style: styles for the widget
     * template: override default template

Row and Column can be used to create responsive bootstrap 3 page grid layouts. They are mutually nestable, ie.

 * Rows may contain multiple columns
 * Columns may contain multiple rows

#### Code
    # Create some text for two rows
    text = MD(LI([5], para=False))
    row1 = MD('**Text in row 1** '+text)
    row2col1 = MD('**Text in row 2 col 1**' + text)
    row2col2 = MD('**Text in row 2 col 2**' + text)

    content = (Row(Column(row1)),                                   # with Row & Column
               R((C(row2col1, width=6), C(row2col2, width=6))))     # with R & C
        """

        # Create some text for two rows
        text = MD(LI([5], para=False))
        row1 = MD('**Text in row 1** '+text)
        row2col1 = MD('**Text in row 2 col 1**' + text)
        row2col2 = MD('**Text in row 2 col 2**' + text)

        content = (Row(Column(row1)),                                   # with Row & Column
                   R((C(row2col1, width=6), C(row2col2, width=6))))     # with R & C
        self.content = page_content(self, doc, content)
        return self


class TestCn(DPage):
    title = 'Layout: Cn convenienc method'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        doc = """
The Cn family of methods may be used to more conveniently define columns with a width of n.

The basic methods Cn are

 * C = functools.partial(Column)
 * C1 = functools.partial(Column, width=1)
 * C2 = functools.partial(Column, width=2)
 * C3 = functools.partial(Column, width=3)
 * C4 = functools.partial(Column, width=4)
 * C5 = functools.partial(Column, width=5)
 * C6 = functools.partial(Column, width=6)
 * C7 = functools.partial(Column, width=7)
 * C8 = functools.partial(Column, width=8)
 * C9 = functools.partial(Column, width=9)
 * c10 = functools.partial(Column, width=10)
 * c11 = functools.partial(Column, width=11)
 * C12 = functools.partial(Column, width=12)

#### Code
    # Create some text for two rows
    text = LI([5], para=False)
    row1 = MD('**Text in row 1** ' + text)
    row2col1 = MD('**Text in row 2 col 1**' + text)
    row2col2 = MD('**Text in row 2 col 2**' + text)
    row2col3 = MD('**Text in row 2 col 3**' + text)

    content = (R(C(row1)),                                          # with R & C
               R(X(C4(row2col1), C4(row2col2), C4(row2col3))))      # with R & C4
        """

        # Create some text for two rows
        text = LI([5], para=False)
        row1 = MD('**Text in row 1** ' + text)
        row2col1 = MD('**Text in row 2 col 1**' + text)
        row2col2 = MD('**Text in row 2 col 2**' + text)
        row2col3 = MD('**Text in row 2 col 3**' + text)

        content = (R(C(row1)),                                          # with R & C
                   R(X(C4(row2col1), C4(row2col2), C4(row2col3))))      # with R & C4
        self.content = page_content(self, doc, content)
        return self


class TestRC(DPage):
    title = 'Layout: RowColumn/RC convenience methods'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        doc = """
 * RowColumn(content, [width=n]), or
 * RC(content, [width=n])
 * RCn(content, [width=n])  where n specified the column width

where

 * content is the content to place in the column
 * width is the bootstrap 3 width, default 12

RowColumn addresses the common case Row(Column(content, ...)).

#### Code
    # Create content
    text = MD('**Text in a row column.** '+LI([5], para=False))
    content = RC(text)
        """

        # Create content
        text = MD('**Text in a row column.** '+LI([5], para=False))
        content = RC(text)
        self.content = page_content(self, doc, content)
        return self


class TestRCList(DPage):
    title = 'Layout: RC list'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        doc = """

 * RCn([[row 1 col 1, row 1 col 2], ...])

RCn creates multiple rows each containing multiple columns in a single statement.

#### Code
    # Create content
    text = MD('**Text in a row column.** '+LI([5], para=False))
    content = RC6([[text, text], [text, text]])C6([[text, text], [text, text]])
        """

        # Create content
        text = MD('**Text in a row column.** '+LI([5], para=False))
        content = RC6([[text, text], [text, text]])
        self.content = page_content(self, doc, content)
        return self


class TestRList1(DPage):
    """
    """
    title = 'Layout: R list with individual column widths'
    description = 'Demonstrate ' + title
    tags = ['layout']

    def page(self):
        doc = """

 * R([Cn([row 1 col 1, row 1 col 2]), ...])

R([Cn(),...]) creates multiple rows each containing multiple columns of different specified widths.

#### Code
    # Create content
    text = MD('**Text in a row column.** '+LI([5], para=False))
    content = R([C(text),
                 C6([text, text]),
                 C4([text, text, text])])
        """

        # Create content
        text = MD('**Text in a row column.** '+LI([5], para=False))
        content = R([C(text),
                     C6([text, text]),
                     C4([text, text, text])])
        self.content = page_content(self, doc, content)
        return self


class TestGlyphicons(DPage):
    title = 'Glyphicons'
    description = 'Demonstrate ' + title
    tags = ['glyphicons', 'text']

    def page(self):
        doc = """
 * Gliphicon(content, classes='', style='', template=None)
 * GL(content, classes='', style='', template=None)

where

 * content: the glypy name, ex. star is glyphicon-star.
 * classes: other class for the widget
 * style: styles for the widget
 * template: override default template

####Code
    # define the content
    glyphs = [(Glyphicon('star'), GL('heart'), GL('music')),
              (GL('zoom-in'), GL('refresh'), GL('qrcode'))]
    content = RC(glyphs))
        """

        # define the content
        glyphs = [(Glyphicon('star'), GL('heart'), GL('music')),
                  (GL('zoom-in'), GL('refresh'), GL('qrcode'))]
        content = RC(glyphs)
        self.content = page_content(self, doc, content)
        return self


class TestButton(DPage):
    title = 'Buttons'
    description = 'Demonstrate ' + title
    tags = ['buttons']

    def page(self):
        doc = """
Button(content, btn_extras='', disabled=False, classes='', style='', template=None)

 * content: text of the widget
 * btn_extras: bootstrap 3 btn- classes
 * disabled: disabled
 * classes: other class for the widget
 * style: styles for the widget
 * template: override default template

####Code
    # define content objects
    r1 = Button('Button')                                               # basic
    r2 = (BR(),
          Button('Large', btn_extras='btn-lg'),                         # large
          Button('XS Success', btn_extras='btn-xs btn-success'))        # XS success
    r3 = (BR(), Button('Block with red text',
                       btn_extras='btn-block', style='color:red;'))     # block red
    r4 = (BR(), Button((GL('star'), 'Star Button'),
                       btn_extras='btn-primary'))                       # primary glyph
    r5 = (BR(), Button('Disabled', disabled=True))                      # disabled
    r6 = Button('Warning with style',
                btn_extras='btn-warning',
                style='color:white; width:200px;margin-top:5px;')       # styles

    # put into layout
    content = RC([r1, r2, r3, r4, r5, r6])
        """

        # define content objects
        r1 = Button('Button')                                               # basic
        r2 = (BR(),
              Button('Large', btn_extras='btn-lg'),                         # large
              Button('XS Success', btn_extras='btn-xs btn-success'))        # XS success
        r3 = (BR(), Button('Block with red text',
                           btn_extras='btn-block', style='color:red;'))     # block red
        r4 = (BR(), Button((GL('star'), 'Star Button'),
                           btn_extras='btn-primary'))                       # primary glyph
        r5 = (BR(), Button('Disabled', disabled=True))                      # disabled
        r6 = Button('Warning with style',
                    btn_extras='btn-warning',
                    style='color:white; width:200px;margin-top:5px;')       # styles

        # put into layout
        content = RC([r1, r2, r3, r4, r5, r6])
        self.content = page_content(self, doc, content)
        return self


class TestLink(DPage):
    title = 'Link'
    description = 'Demonstrate ' + title
    tags = ['link']

    def page(self):
        doc = """
Link(href, content, button='', classes='', style='', template=None)

 * href: link href
 * content: link content
 * button: button classes, ex. 'btn-success btn-sm'
 * classes: other class for the widget
 * style: styles for the widget
 * template: override default template

####Code
    # define content objects
    r1 = Link('/dpages/DPagesList', 'Link to DPagesList')
    r2 = Link('/dpages/DPagesList', 'Button link to DPagesList',
              button='btn-info btn-xs')
    r3 = Link('/dpages/DPagesList', 'Button with style and classes to DpagesList',
              button='btn-success btn-sm',
              style='color:white;width:r00px;margin-top:5px;')

    # put into layout
    content = RC([r1, r2, r3])
        """

        # define content objects
        r1 = Link('/dpages/DPagesList', 'Link to DPagesList')
        r2 = Link('/dpages/DPagesList', 'Button link to DPagesList',
                  button='btn-info btn-xs')
        r3 = Link('/dpages/DPagesList', 'Button with style and classes to DpagesList',
                  button='btn-success btn-sm',
                  style='color:white;width:r00px;margin-top:5px;')

        # put into layout
        content = RC([r1, r2, r3])
        self.content = page_content(self, doc, content)
        return self


class TestBasicGraphs(DPage):
    """
    Basic test of Graph facility.
    """
    title = 'Graphs'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        doc = """
 * Graph(graph_type, data, options=None, **kwargs)

where

 * graph_type: is one of the supported graph types
    * line
    * pie
    * column
    * bar
    * area
 * data: is the data for the graph
 * options: the 'with' options for chartkick
 * kwargs: rfu
        """

        # data for chart
        browser_stats = [['Chrome', 52.9],
                         ['Firefox', 27.7],
                         ['Opera', 1.6],
                         ['Internet Explorer', 12.6],
                         ['Safari', 4]]

        # create the pie chart and set it's title & subtitle
        pie_graph = Graph('pie', browser_stats)
        pie_graph.options = {'height': '400px',
                             'title.text': 'Browser Stats',
                             'subtitle.text': 'Graphs may have subtitles'}

        # Layout the content on the page
        content = RC([MD('##Can have other DjangoPage content on the page with the graph.'),
                      pie_graph,
                      MD('####Explanation of graph') + LI([8, 5])])
        self.content = page_content(self, doc, content)
        return self


class TestMultipleGraphsInRow(DPage):
    """
    Basic test of Graph facility.
    """
    title = 'Graphs: Multiple graphs in row'
    description = 'Demonstrate ' + title
    tags = ['graphs']

    def page(self):
        # data for chart
        browser_stats = [['Chrome', 52.9],
                         ['Firefox', 27.7],
                         ['Opera', 1.6],
                         ['Internet Explorer', 12.6],
                         ['Safari', 4]]

        # create the pie chart and set it's title & subtitle
        pie_graph = Graph('pie', browser_stats)
        pie_graph.options = {'height': '400px',
                             'title.text': 'Browser Stats',
                             'subtitle.text': 'Graphs may have subtitles'}

        # Layout the content on the page
        self.content = RC([MD('##Can have other DjangoPage content on the page with the graph.'),
                           pie_graph,
                           MD('####Explanation of graph') + LI([8, 5])])
        return self


class TestBasicGraphsB(DPage):
    """
    Basic test of Graph facility with two graphs in a row.
    """
    title = 'Graphs'
    description = 'Demonstrate ' + title
    tags = ['graphs']

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
        self.content = (RC(text_top),
                        RC6((col_graph, pie_graph)),
                        RC(text_bottom))
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
        self.content = (RC12(xr1),
                        R(C4(xrform), C6(xr2)),
                        RC3(xr4))
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
                        R(C3X(company_tit, company_tbl),
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
        pn = Panel(X(node_tit, node_tbl))
        bpn = ButtonPanel('Open the node panel', pn)
        pc = Panel(X(company_tit, company_tbl))
        bpc = ButtonPanel('Open the company panel', pc)

        ###################
        # Put content on page
        ###################
        # Define the content layout
        self.content = (Markdown('**Side by side panels**'),
                        R(C2(Panel(company_tit, company_tbl, button='Show Companies')),
                           C6(Panel(node_tit, node_tbl, button='Show Nodes'))),
                        RC(LI()),
                        RC(Markdown('#Button Panel')),
                        RC6(('The button is in the left column.', bpn, bpc,
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
                        R(C3(Markdown('**Panel on left**')), C9(crsl1)),
                        RC(LI()),
                        R(C9(crsl2), C3(Markdown('**Panel on right**'))),
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
                        RC((Link('/dpages/DPagesList', 'Link to list page', button=True), ' ',
                             Link('/dpages/Test07', 'Link to the form test page', button=True),)
                            )
                        )
        return self
