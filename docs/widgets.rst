.. Widgets overview.

Widgets
+++++++

Widgets create content, including layouts, for DjangoPages. For example::

    Text(('Paragraph 1 text', 'Paragraph 2 text'), para=True)       # outputs two paragraphs
    Text('Sentence 1')                                              # outputs 'Sentence 1'

Widgets may contain other widgets. A DjangoPage will commonly contain code like this::

    Column(                             # outputs a bootstrap 3 column
            MD('##Some heading'),       # outputs a markdown level 2 heading
            LI()                        # outputs 1 loremipsum paragraph
           )


Widget implementations typically look something like this::

    # noinspection PyPep8Naming
    def Text(content, para=False, classes='', style='', template=None):
        """ Renders text content to the page.

        .. sourcecode:: python

            Text('this is some text content.  More text content. <b>Can contain html</b>')

        | Synonym: T(...), useful abbreviation
        | Synonym: HTML(...), useful to indicate intent

        :param content: content
        :type content: str or unicode
        :param para: if True wrap output in a paragraph
        :type para: bool
        :param classes: classes to add to output
        :type classes: str or unicode
        :param style: styles to add to output
        :type style: str or unicode
        :param template: override template
        :type template: str or unicode
        """
        if isinstance(content, tuple):
            rtn = ''
            for c in content:
                rtn += Text(c, para, classes, style, template)
            return rtn
        if classes:
            classes = 'class="{}" '.format(classes)
        if style:
            style = 'style="{}" '.format(style)
        if template:
            return template.format(content=content)
        if para:
            return '<p {classes} {style}>{content}</p>'.format(classes=classes, style=style, content=content)
        if classes or style:
            return '<span {classes} {style}>{content}</span>'.format(classes=classes, style=style, content=content)
        return content
    T = functools.partial(Text)
    HTML = functools.partial(Text)

Widgets ultimately are responsible for returning well formed error free HTML based on the widget's
arguments. Widgets are rather simple code generators and you are free to create/extend widgets.

You can see many examples DWidget examples in djangopages.widgets.dpage_texthtml.py and related modules.
