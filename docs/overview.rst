.. DjangoPages overview.

Overview
========

DjangoPages has two main conceptual components:

* Pages created by subclassing DPage
* Content widgets created by subclassing DWidget

DPage
-----

DPage(s) define DjangoPage(s). Typically a DjangoPage looks something like this::

    class Test000b(DPage):

        def page(self):                                         # Must override page
            page_content = MD('This is the panel body')         # Create page content
            self.content = RC(page_content)                     # Put content in the page layout
            return self

In the above example:

* MD is an abbreviation for Markdown() and renders markdown text
* RC is an abbreviation for Row(Column()) and renders its content in a bootstrap 3 row column

DjangoPages must:

* Inherit from DPage
* Override DPage.page
    * Define self.content
    * return self

You can see many DPage examples in djangopages.views.


# fixme: finish this

next_dpage
prev_dpage
sibling_dpage

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


DWidget Introduction
--------------------

DWidget(s) create content for DjangoPages.  Typically a DWidget looks something like this::

    class LIParagraph(DWidget):
        """ Generate amount loremipsum paragraphs

        LIParagraph(amount=1, para=True)
            amount: number of paragraphs to return
            para: if true, wrap each returned paragraph in <p>...</p>
        """
        def __init__(self, amount=1, para=True):
            super(LIParagraph, self).__init__()
            self.amount = amount
            self.para = para
            pass

        def render(self):
            amount = self.amount
            para = self.para
            li = loremipsum.get_paragraphs(amount)
            if not para:
                return li
            out = ''
            for p in li:
                out += '<p>{}</p>'.format(p)
            return out

DWidgets must:

* Inherit from DWidget
* Initialize the superclass
* Save widget unique arguments
* Override DWidget.render to return the HTML representing the widget

You can see many examples DWidget examples in djangopages.dpage_texthtml.py and related modules.

DWidget Details
---------------

.. autoclass:: djangopages.dpage.DWidget
   :members: render_setup, render_objects

Other base DjangoPage methods
-----------------------------

The following other methods play a useful role in DjangoPages.

.. autofunction:: djangopages.dpage.unique_name

