#!/usr/bin/env python
# coding=utf-8

"""
DPage
*****

.. module:: dpage
   :synopsis: Provides base DjangoPage DPage and DWidget

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

5/9/14 - Initial creation

DjangoPages replaces the conventional Django notion of HTML templates, views, and URLs.
Instead, DjangoPages uses a declarative approach similar to Django's models.Model and
forms.Form. This declarative approach is used both for page definition and creation of
content on the page.

DPage(s)
++++++++

DjangoPages pages are created by subclassing DPage and overriding DPage.generate.

.. note:: The DPage class name defines the page's url.  It is no longer necessary to maintain
          urls.py for DPage(s)!  That's one less thing to do.

The override **generate** method defines the page's content and layout. Generally, widgets
are used to create content. Typically a DPage looks something like this::

    class ExamplePage(DPage):                               # Class name defines URL
        title = 'Brief title'                               # Brief title useful in list, etc.
        description = 'Longer description'                  # Longer description
        tags = ['example', 'MD', 'RC']                      # Queryable tags

        def generate(self, *args, **kwargs):                # Must override generate
            page_content = MD('This is the panel body')     # Create markdown page content with MD DWidget
            content = RC(page_content)                      # Put content in a bootstrap row & column with RC DWidget
            return content

Generally, DPage(s) define some content and then place that content in a layout.

DPage(s) typically define:

* A short title for the page that is useful in page list, etc.
* A longer description for the page.
* Zero or more tages that are useful for organizing and querying pages.

Details
+++++++
"""


from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/9/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

# todo 3: add class to deal with file like objects and queryset objects
# todo 3: add support for select2 https://github.com/applegrew/django-select2
# todo 3: https://github.com/digi604/django-smart-selects provides chained selects for django models

# todo 3: allow form to specify custom template
# todo 2: support rest of bootstrap form attributes
# todo 2: syntactic suggar for Form

# todo 3: here check text type and deal with file like objects and queryset objects
# for now just deal with actual text
# todo 2: add markdown kwargs options here

########################################################################################################################
#
# DPage class
#
########################################################################################################################


class _DPageRegister(type):
    """ Internal metaclass to register DPage child objects.  Do not mess with this! """
    # noinspection PyMissingConstructor,PyUnusedLocal
    def __init__(cls, name, base, attrs):
        if not hasattr(cls, 'pages_list'):
            # Executed when processing DPageRegister class itself.
            # Use class variables so there is only one copy of pages_list and pages_dict
            # Insert pages_list and pages_dict into the class definition of the class using this metaclass
            cls.pages_list = []          # List of subclasses to allow listing
            cls.pages_dict = {}          # Dictionary of subclasses to allow quick name lookup
        else:
            # This is a plugin implementation of this class that needs to be registered.
            # Save the class name and cls object.
            cls.pages_list.append({'cls': cls, 'name': name})       # Put in list
            cls.pages_dict[name] = cls                              # Put in dict


class DPage(View):
    """ DPage classes define Django Page objects, ie. pages that can be displayed.

    .. note:: As a general rule, you need not perform initialization in the DPage child class.
              However, if you do these parameters are available.

        :param request: The request object
        :type request: WSGIRequest
        :param context: Additional context values for the page
        :type context: dict
        :param template: template name to use for this DPage object.  If None, DPageDefaultTemplate specified in
                         settings is used.
        :type template: unicode
        :param title: brief title for this DPage object
        :type title: unicode
        :param description: longer description for this DPage object
        :type description: unicode
        :param tags: list of tags for this DPage
        :type tags: list

    .. note:: It is legal and sometimes useful to define a DPage and render it as part of another DPage.

                .. sourcecode:: python

                    content = dpage.one.render()
    """
    __metaclass__ = _DPageRegister              # use DPageRegister to register child classes

    def __init__(self, request=None, context=None, template=None,
                 title='', description='', tags=None, **kwargs):
        """
        Initialize the DPage.
        """
        super(DPage, self).__init__(**kwargs)
        self.request = request
        self.context = context
        self.template = template if template else settings.DPAGE_DEFAULT_TEMPLATE
        if not self.title:
            self.title = title
        if not self.description:
            self.description = description
        if not self.tags:
            if tags:
                self.tags = tags
            else:
                self.tags = list()
        self.content = []
        return

    def get(self, request):
        """ Base class default get method

        Child classes need not provide a get method but *MUST* provide a generate
        method.
        """
        content = self.generate(request)
        return render(request, self.template, {'content': content})

    def generate(self, request):
        """ Generate the page content. The subclass must define this method to create the page content.

        .. sourcecode:: python

            def generate(self, request):
                xr1 = Text('This text comes from dpage.Text')
                xr2 = Markdown('**Bold Markdown Text**')
                xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                self.content(RC([xr1, xr2, xr3])
                return self

        Conceptually, the page's generate method creates HTML content that will
        subsequently be provided as a context value to the page's template.
        """
        raise NotImplementedError("Subclasses should implement DPage.generate!")

    def __unicode__(self):
        return self.__class__.__name__

    def __str__(self):
        return unicode(self).encode('utf8')

    @staticmethod
    def find(tag):
        """ Return list of DPage(s) with this tag.

        .. sourcecode:: python

            find('tag_to_find')

        :param tag: to find
        :type tag: unicode
        :return: List of DPage(s) with this tag.
        :rtype: list
        """
        # noinspection PyUnresolvedReferences
        pages = DPage.pages_list
        lst = []
        for p in pages:
            cls = p['cls']
            if tag in cls.tags:
                lst.append(p)
        return lst

    def next(self, obj=False):
        """ Return DPage after this DPage in the DPage list.
        .. sourcecode:: python

            next()

        :param obj: If true, return the object.  Otherwise return the name.
        :type obj: bool
        :return: Next dpage in the list
        :rtype: str or DPage object
        """
        # noinspection PyUnresolvedReferences
        pl = DPage.pages_list
        # noinspection PyBroadException
        try:
            pi = pl.index({'name': self.__class__.__name__, 'cls': self.__class__})
            if obj:
                return pl[pi+1]
            else:
                return pl[pi+1]['name']
        except:
            return None

    def prev(self, obj=False):
        """Return DPage before this DPage in the DPage list.
        .. sourcecode:: python

            prev()

        :param obj: If true, return the object.  Otherwise return the name.
        :type obj: bool
        :return: Previous page in the list
        :rtype: str or DPage object
        """
        # noinspection PyUnresolvedReferences
        pl = DPage.pages_list
        # noinspection PyBroadException
        try:
            pi = pl.index({'name': self.__class__.__name__, 'cls': self.__class__})
            if obj:
                return pl[pi-1]
            else:
                return pl[pi-1]['name']
        except:
            return None

    def siblings(self, obj=False):
        """ Return DPage(s) before and after this DPage in the list.
        .. sourcecode:: python

            siblings()

        :param obj: If true, return the objects.  Otherwise return the names.
        :type obj: bool
        :return: Siblings in the list
        :rtype: tuple
        """
        return self.prev(obj), self.next(obj)

########################################################################################################################
#
# Content classes and methods
#
########################################################################################################################
#
#
# class DWidget(object):
#     """ DWidget(s) provide content for DPage(s)
#
#     DWidgets have a signature that looks generally like this:
#
#     .. sourcecode:: python
#
#         some_widget( content1, content2, ..., kwargs)
#
#     The following kwargs are available to all widgets:
#         * template: template override for the widget
#         * classes: extra classes for the widget
#         * style: extra styles for the widget
#
#     Widgets are free to define other kwargs as required.
#
#     DWidget provides a default render and generate methods.
#     Derived classes **must** override (preferably) generate or (if needed) render.
#
#     DWidget implements
#
#     * __add__
#     * __radd__
#     * __mul__
#     * __str__
#     * __repr__
#
#     as a convenience.
#
#     .. note:: add (+) and mul (*) force immediate rendering of the widget.
#     """
#     template = ''
#
#     def __init__(self, content, kwargs):
#         # log.debug('-----in dwidget init')
#         self.content = content
#         self.template = kwargs.pop('template', self.template)
#         self.classes = kwargs.pop('classes', None)
#         self.style = kwargs.pop('style', None)
#         self.kwargs = kwargs
#         # log.debug('-----done dwidget init')
#         return
#
#     def render(self):
#         """ Render the widget's content, classes, style, and template.
#         Invoke the generate method, likely the child class generate, to actually
#         create the output HTML.
#
#         .. sourcecode:: python
#
#             render()
#
#         :return: widgets HTML
#         :rtype: str
#
#         .. note:: Widgets may, though probably shouldn't, override the default render method.
#         """
#         # log.debug('##### in dwidget render')
#         content = _render(self.content)
#         classes = ''
#         if self.classes:
#             classes = 'class="{}"'.format(_renderstr(self.classes))
#         style = ''
#         if self.style:
#             style = 'style="{}"'.format(_renderstr(self.style))
#         template = ''
#         if self.template:
#             template = _renderstr(self.template)
#         # todo: should _render be applied to kwargs
#         kwargs = self.kwargs
#         out = self.generate(template, content, classes, style, kwargs)
#         # log.debug('##### done dwidget render')
#         return out
#
#     def generate(self, template, content, classes, style, kwargs):
#         """ Generate the widget's content.
#
#         :param template: The widget's template with all objects rendered.
#         :type template: varies, typically str or tuple
#         :param content: The widget's content with all objects rendered.
#         :type content: varies, typically str or tuple
#         :param classes: The widget's classes with all objects rendered.
#         :type classes: varies, typically str
#         :param style: The widget's styles with all objects rendered.
#         :type style: varies, typically str
#         :param kwargs: The widget's kwargs.  Note, objects are **not rendered**.
#         :type kwargs: dict
#         :return: The widget's HTML
#         :rtype: str
#
#         .. note:: Widgets should almost always override this method.
#         """
#         log.debug('!!!!! in DWidget generate')
#         try:
#             c = ' '.join(content)
#             return template.format(content=c, classes=classes, style=style)
#         except TypeError:
#             raise TypeError('Non string content for default DWidget generate')
#
#     def __add__(self, other):
#         return self.render() + other
#
#     def __radd__(self, other):
#         return other + self.render()
#
#     def __mul__(self, other):
#         return self.render() * other
#
#     def __str__(self):
#         return self.render()
#
#     def __repr__(self):
#         return self.render()
#
#     @staticmethod
#     def add_classes(existing, new):
#         """ Add classes to existing classes for the widget.  Typically used by the widget's generate method
#         to add classes that the widget needs to those created by the widget definition.
#
#         .. sourcecode:: python
#
#             add( existing_classes, 'classes_to_add')
#
#         :param existing: Existing class string, ex. class="someclass another_class"
#         :type existing: str or unicode
#         :param new: Classes to add, ex. "a_class_to_add"
#         :type new: str or unicode
#         :return: new class string, ex. class="someclass another_class a_class_to_add"
#         :rtype: str
#         """
#         if existing == '':
#             return 'class="{}"'.format(new)
#         return existing[:-1] + ' ' + new + '"'
#
#     @staticmethod
#     def add_style(existing, new):
#         """Add style(s) to existing style(s) for the widget.  Typically used by the widget's generate method
#         to add styles that the widget needs to those created by the widget definition.
#
#         .. sourcecode:: python
#
#             add_style( existing_styles, 'styles_to_add')
#
#         :param existing: Existing style string, ex. style="style1;style2;"
#         :type existing: str or unicode
#         :param new: Styles to add, ex. "style3;style4;"
#         :type new: str or unicode
#         :return: new style string, ex. style="style1;style2;style3;style4;"
#         :rtype: str
#         """
#         if existing == '':
#             return 'style="{}"'.format(new)
#         return existing[:-1] + ' ' + new + '"'

########################################################################################################################
#
# Support Routines
#
########################################################################################################################


# def _render(content):
#     """ Render the content.  As a general rule this internal method should **not** be used.  However,
#     there are exceptions.
#
#     .. sourcecode:: python
#
#         _render(content)
#
#     | Synonym: X
#
#     :param content: content to render
#     :type content: varies
#     :return: the rendered content
#     :rtype: varies
#     """
#     # log.debug('in _render with <<{}>> type {}'.format(content, type(content)))
#     if isinstance(content, basestring):
#         return content
#     if hasattr(content, 'render'):
#         return content.render()
#     if isinstance(content, (int, long, float)):
#         return content
#     if isinstance(content, tuple):
#         tpl = tuple()
#         for con in content:
#             tpl += (_render(con),)
#         return tpl
#     if isinstance(content, list):
#         lst = list()
#         for con in content:
#             lst.append(_render(con))
#         return lst
#     return content
# X = functools.partial(_render)
#
#
# def _renderstr(content):
#     """ Render content, concatenate result basestrings.
#
#     .. sourcecode:: python
#
#         _renderstr(content)
#
#
#     | Synonym: XS(...)
#
#     :param content: content to render
#     :return: rendered content
#     :rtype: basestring
#     """
#     rtn = _render(content)
#     out = ''
#     for r in rtn:
#         if isinstance(r, basestring):
#             out += r
#     return out
# XS = functools.partial(_renderstr)
