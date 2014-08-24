.. DjangoPages documentation master file, created by
   sphinx-quickstart on Tue Aug 12 11:01:36 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to DjangoPages's documentation!
***************************************

**DjangoPages** provides a set of technologies to quickly and easily create rich DB driven responsive
web pages with graphs, tables, forms, and other elements.

**DjangoPages** are created by subclassing the DPage class and defining the page's generate method.  You may
create a url.py entry for a DjangoPage but you don't have to.  Instead DjangoPages will use the DPage child
class method to provide a standard URL for the page.  One less thing to do.

A DjangoPage might look something like this:

.. sourcecode:: python

    class ExampleDjangoPage(DPage):
        """ Example DjangoPage """
        title = 'Example DjangoPage'                # short title
        description = 'Longer description'          # longer description
        tags = ['example']                          # queryable tags to support searching

        def generate(self, request):                # create the page's HTML
            c1 = Markdown('###Markdown h3')         # Markdown widget
            content = RC(c1, c2)                    # bootstrap row column widget
            return content                          # return the page's content

.. Note:: The page's generate method is used to create the page content and lay it out on the page.  You may
          but need not use a template.

**DjangoPages** page content is created using DjangoPage widgets. Widgets

* Can provide content such as Markdown above
* Define the page's layout such as RC above

Widgets provide a powerful set of tools to create content and layouts in a declarative fashion that is
dramatically less verbose and much easier to use than traditional templates.  Just as Django's
declarative ORM makes creating databases easier, DjangoPage widgets provides a declarative style for page
content creation and layout. For example

.. sourcecode:: python

        def generate(self, request):
            t = LI(5, para=False)
            content = RowColumn((('Row 1 Col 1 ' + t, 'Row 1 Col 2 ' + t),
                                 ('Row 2 Col 1 ' + t, 'Row 2 Col 2 ' + t)),
                                width=6)
            return content

creates a page with a responsive bootstrap grid of two rows with two 6 wide columns.

.. Note:: DjangoPages typically provides a 4:1 to 20:1 reduction in the amount of code needed to
    create a page. Additionally, the code intent is generally much clearer and there is much less
    chance of defective html.

**DjangoPages** also allows page content to be created using the Django admin interface in a 'flatpage'
like fashion. A conventional Django model is used to hold DPage definitions as illustrated above. This allows pages
to be created, updated, or deleted without needing to update and restart the server.

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   dpage
   widgets
   text
   layout
   bootstrap3
   graphs
   libs
   view

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

