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

DWidget
-------

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