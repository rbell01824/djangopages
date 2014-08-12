.. DjangoPages overview.

Overview
========

DjangoPages has two main conceptual components:

* Pages created by subclassing DPage
* Widgets created by subclassing DWidget that provide content to pages

DPage Introduction
------------------

DPage(s) define DjangoPage(s). Typically a DjangoPage looks something like this::

    class ExamplePage(DPage):                                   # Class name defines URL
        title = 'Brief title'
        description = 'Longer description'
        tags = ['tag 1', 'tag 2']

        def page(self):                                         # Must override page
            page_content = MD('This is the panel body')         # Create page content
            self.content = RC(page_content)                     # Put content in the page layout
            return self

In the above example:

* MD is an abbreviation for Markdown() and renders markdown text
* RC is an abbreviation for Row(Column()) and renders its content in a bootstrap 3 row column

DPage(s) must:

* Inherit from DPage
* Override DPage.page
    * Define self.content
    * return self

DPage(s) may/should:

* Define their title
* Define their description
* Define one or more page tags

You can see many DPage examples in djangopages.views.

DPage Processing
++++++++++++++++

When a DjangoPage is created its URL is defined based on the page's class name.  It is not necessary to
create a urls.py entry.  Convenience methods are planned to facilitate control of the site url namespace.

DPages are rendered follows:

* The page's render method is executed.  As a general proposition DjangoPages need not and should not
  override the DPage render method.
* The Dpage render method renders each element of self.content
* The results are concatenated
* The results are passed to the page's template and a response object returned

The end result is that DjangoPages render using the underlying Django render/response methods.

DPage Details
+++++++++++++

.. autoclass:: djangopages.dpage.DPage
   :members: render, find, next, prev, siblings

Widget Introduction
-------------------

DWidget(s) create content for DjangoPages. For example::

    Text('Paragraph 1 text', 'Paragraph 2 text', para=True)         # outputs two paragraphs
    Text('Sentence 1 ', 'Sentence 2')                               # outputs 'Sentence 1 Sentence 2'

Widgets may contain other widgets. A DjangoPage will commonly contain code like this::

    Column(                             # outputs a bootstrap 3 column
            MD('##Some heading'),       # outputs a markdown level 2 heading
            LI()                        # outputs 1 loremipsum paragraph
           )

Widget Arguments
++++++++++++++++

Widgets take an arbitrary number of positional arguments.

Widgets have a default set of keyword arguments.

* classes: classes to be used with the DWidget
* style: styles to be used with the DWidget
* template: an override template for the DWidget
* kwargs: any remaining kwargs

Widgets may have widget specific keyword arguments.

Widgets are free to use these arguments as appropriate for their purpose.  As a general rule

* classes define extra classes to be added to any widget default classes
* style defines extra styles to be added to any widget default styles
* template may be used to override the widget's default template

Widget Signature
++++++++++++++++

DWidget(s) have the following signature::

    someDWidget(*content, **kwargs)

where

* content is the content for the widget
* kwargs are the widget's key word arguments

Widget Example
++++++++++++++

The Text widget is reasonably typical of widgets generally.::

    class Text(DWidget):
        """ Renders content to the page.

        | Text(content, para=False, classes='', style='', template=None)
        | T(...)
        | HTML(...)

        * para: If True wrap the output in <p>...</p>
        """
        template = '{content}'
        template_para = '<p {classes} {style}>{content}</p>'

        # def __init__(self, content, para=False, classes='', style='', template=None):
        #     super(Text, self).__init__(content, classes, style, template)
        #     self.para = para
        #     return

        def __init__(self, *content, **kwargs):
            super(Text, self).__init__(content, kwargs)
            return

        def render(self):
            """
            Render the Text object
            """
            content, classes, style, template, kwargs = self.render_setup()
            if self.kwargs.pop('para', None):
                return Text.template_para.format(content=content, classes=classes, style=style)
            return template.format(content=content, classes=classes, style=style)
    T = functools.partial(Text)
    HTML = functools.partial(Text)

DWidgets must:

* Inherit from DWidget
* Initialize the superclass
* Override DWidget.render to return the HTML representing the widget

You can see many examples DWidget examples in djangopages.dpage_texthtml.py and related modules.

DWidget Details
---------------

.. autoclass:: djangopages.dpage.DWidget
   :members: render_setup

Other base DjangoPage methods
-----------------------------

The following other methods play a useful role in DjangoPages.

.. autofunction:: djangopages.dpage.unique_name

