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
========

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
=======
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
from django.http import HttpResponse

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

    def _get_post(self, request, *args, **kwargs):
        """ DPage shared default get/post processing """
        content = self.generate(request, *args, **kwargs)
        if isinstance(content, DPage):
            content = self.content
        elif isinstance(content, (str, unicode)):
            pass
        elif isinstance(content, HttpResponse):
            return content
        else:
            raise ValueError("Generate returned illegal type {}.".format(type(content)))
        return render(request, self.template, {'content': content})

    def get(self, request, *args, **kwargs):
        """ Base class default get method

        Invokes self.generate(request. *args, **kwargs).  If generate returns str/unicode renders with returned
        value.  If generate returns DPage, renders self.content.  If generate returns HTTPResponse, returns response.
        """
        return self._get_post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Base class default post method

        Invokes self.generate(request. *args, **kwargs).  If generate returns str/unicode renders with returned
        value.  If generate returns DPage, renders self.content.  If generate returns HTTPResponse, returns response.
        """
        return self._get_post(request, *args, **kwargs)

    def generate(self, request, *args, **kwargs):
        """ Generate the page content. The subclass must define this method to create the page content.

        .. sourcecode:: python

            def generate(self, request, *args, **kwargs):
                xr1 = Text('This text comes from dpage.Text')
                xr2 = Markdown('**Bold Markdown Text**')
                xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                self.content(RC([xr1, xr2, xr3])
                return self

            or

            def generate(self, request, *args, **kwargs):
                xr1 = Text('This text comes from dpage.Text')
                xr2 = Markdown('**Bold Markdown Text**')
                xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                content(RC([xr1, xr2, xr3])
                return content



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
