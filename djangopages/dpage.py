#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/9/14 - Initial creation

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

import collections
import functools

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

# todo 3: add class to deal with file like objects and queryset objects
# todo 3: add support for select2 https://github.com/applegrew/django-select2
# todo 3: https://github.com/digi604/django-smart-selects provides chained selects for django models

# todo 3: allow form to specify custom template
# todo 2: support rest of bootstrap 3 form attributes
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
    """
    Internal metaclass to register DPage child objects.  Do not mess with this!
    """
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


class DPage(object):
    """
    DPage classes define Django Page objects, ie. pages that can be displayed.

    As a general rule, you need not perform initialization in the DPage child class.  However, if you do these
    parameters are available.

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
    """
    __metaclass__ = _DPageRegister              # use DPageRegister to register child classes

    def __init__(self, request=None, context=None, template=None,
                 title='', description='', tags=None):
        """
        Initialize the DPage.
        """
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
        pass

    def page(self):
        """
        Define the page.  The subclass must define this method to create the page content.

        The page method defines the page.  Example:

            def page(self):
                xr1 = Text('This text comes from dpage.Text')
                xr2 = Markdown('**Bold Markdown Text**')
                xr3 = HTML('<h3>H3 text from DPageHTML</h3>')
                self.content(RC([xr1, xr2, xr3])
                return self
        """
        raise NotImplementedError("Subclasses should implement DPage.page!")

    def render(self):
        """
        Render this DPage and return a Django response object.

        :return: response object
        :rtype: HttpResponse
        """
        # init context if nothing in it
        if not self.context:
            self.context = {}

        # render all our objects
        content = render_objects(self.content)

        # if there was nothing, use the default content
        if len(content) == 0:
            content = settings.DPAGE_DEFAULT_CONTENT

        self.context['content'] = content

        return render(self.request, self.template, self.context)

    def __unicode__(self):
        return self.__class__.__name__

    def __str__(self):
        return unicode(self).encode('utf8')

    # fixme: rename these method, document, change globally

    @staticmethod
    def find(tag):
        """
        Find all the DPage(s) with this tag.
            :param tag: Tag
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
        """
        Return next dpage in the dpage list.
            :param obj: If true, return the object.  Otherwise return the name.
            :type obj: bool
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
        """
        Return previous dpage in the dpage list.
            :param obj: If true, return the object.  Otherwise return the name.
            :type obj: bool
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
        """
        Return the prev and next dpage objects from the list
            :param obj: If true, return the object.  Otherwise return the name.
            :type obj: bool
        """
        return self.prev(obj), self.next(obj)

########################################################################################################################
#
# Content classes and methods
#
########################################################################################################################


class DWidget(object):
    """ DWidget(s) provide content for DPage(s)

    DWidget(content='', classes='', style='', template=None, kwargs=None)
    # def __init__(self, content='', classes='', style='', template=None, kwargs=None):

    * content: the widget's content
    * style: extra styles for the widget
    * template: template override for the widget
    * kwargs: additional widget arguments

    The base class initialization saves the arguments.

    DWidget provides a default render method that MUST be overridden in the child class.
    The default render method raises NotImplementedError.

    DWidget implements

    * __add__
    * __radd__
    * __mul__
    * __str__
    * __repr__

    as a convenience.
    """
    template = ''

    def __init__(self, content, kwargs):
        self.content = content
        self.classes = kwargs.pop('classes', None)
        self.style = kwargs.pop('style', None)
        self.template = kwargs.pop('template', self.template)
        self.kwargs = kwargs
        return

    def render(self):
        """
        Render this content object.
        """
        raise NotImplementedError("Subclasses should implement Content.render!")

    def render_setup(self, extra_classes=None, extra_style=None):
        """ Provides default setup for render.

        content, classes, style, template = self.render_setup(extra_classes=None, extra_style=None)

        * extra_classes: if sepcified extra classes to apply to the widget
        * extra_style: if specified extra styles to apply to the widget

        Applies render_objects to content, classes, extra_classes, style, extra_style,
        and template.

        Returns (content, classes, style, template, kwargs)

        * content: content string for the widget
        * classes: class string for the widget adding extra_classes or ''
        * style: style string for the widget adding extra_styles
        * template: template to use with the widget

        See tbd for how this method should be used.
        """
        content = RO(self.content)
        classes = ''
        if self.classes or extra_classes:
            classes = 'class="{} {}"'.format(RO(self.classes),
                                             RO(extra_classes))
        style = ''
        if self.style or extra_style:
            style = 'style="{}"'.format(RO(self.style))
        template = RO(self.template)
        return content, classes, style, template

    def __add__(self, other):
        return self.render() + other

    def __radd__(self, other):
        return other + self.render()

    def __mul__(self, other):
        return self.render() * other

    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()

########################################################################################################################
#
# Support Routines
#
########################################################################################################################


def render_objects(*content):
    """ Render the content.

    DWidget.render_objects(<content>, [<content>, ...])

    * content: the content to render

    Returns

    * content.render()+...

    Example:

    DWidget.render_objects('thing 1', ('thing 2', MD('thing'))

    Synonyms: X, RO.
    """
    out = ''
    for con in content:
        if isinstance(con, basestring):                     # strings are just themselves
            out += con
        elif hasattr(con, 'render'):                        # objects with render methods know how to render themselves
            out += con.render()
        elif isinstance(con, collections.Iterable):         # collections are walked
            for con1 in con:
                out += render_objects(con1)                 # recurse to render this collection item
        else:                                               # this should never happen
            raise ValueError('Unknown content type in render_objects {}'.format(con))
    return out
X = functools.partial(render_objects)                       # convenience method for render objects
RO = X


def unique_name(base_name='x'):
    """ Returns a unique name of the form 'base_name'_counter.

    This function is used by widgets and for other internal purporse to
    create unique names for id(s) and other purposes.

    * basename: the base name to use for the name

    Returns a name of the form <basename>n where n is 0, 1, 2, ... on subsequent uses.
    """
    if not hasattr(unique_name, "counter"):
        unique_name.counter = 0  # it doesn't exist yet, so initialize it
    unique_name.counter += 1
    return '{}_{}'.format(base_name, unique_name.counter)
