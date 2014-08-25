#!/usr/bin/env python
# coding=utf-8

"""

Libs
****

.. module:: libs
    :synopsis: support libs for DjangoPages


.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

5/14/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/14/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.template import add_to_builtins

from taggit.models import TaggedItem

########################################################################################################################
#
# Taggit List filter for admin
#
########################################################################################################################


class TaggitListFilter(SimpleListFilter):
    """
    A custom filter class that can be used to filter by taggit tags in the admin.

    code from https://djangosnippets.org/snippets/2807/
    """

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('tags')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    # noinspection PyUnusedLocal,PyShadowingBuiltins,PyMethodMayBeStatic
    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each tuple is the coded value
        for the option that will appear in the URL query. The second element is the
        human-readable name for the option that will appear in the right sidebar.
        :param model_admin:
        :param request:
        """
        list = []
        tags = TaggedItem.tags_for(model_admin.model)
        for tag in tags:
            list.append((tag.name, _(tag.name)), )
        return list

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value provided in the query
        string and retrievable via `self.value()`.
        :param queryset:
        :param request:
        """
        if self.value():
            return queryset.filter(tags__name__in=[self.value()])

########################################################################################################################
#
# Force load of template tags that are generally needed by graphpages
#
# This is important: If the function is called early, and some of the custom
# template tags use superclasses of django template tags, or otherwise cause
# the following situation to happen, it is possible that circular imports
# cause problems:
#
# If any of those superclasses import django.template.loader (for example,
# django.template.loader_tags does this), it will immediately try to register
# some builtins, possibly including some of the superclasses the custom template
# uses. This will then fail because the importing of the modules that contain
# those classes is already in progress (but not yet complete), which means that
# usually the module's register object does not yet exist.
#
# In other words:
#       {custom-templatetag-module} ->
#       {django-templatetag-module} ->
#       django.template.loader ->
#           add_to_builtins(django-templatetag-module)
#           <-- django-templatetag-module.register does not yet exist
#
# It is therefor imperative that django.template.loader gets imported *before*
# any of the templatetags it registers.
#
########################################################################################################################


def load_templatetags():
    """
    Load custom template tags so they are always available.  See https://djangosnippets.org/snippets/342/.

    In your settings file:

    TEMPLATE_TAGS = ( "djutils.templatetags.sqldebug", )

    Make sure load_templatetags() gets called somewhere, for example in your apps init.py
    """

    #
    # Note: For reasons I don't understand this code gets ececuted twice when
    # Django starts.  Nothing bad seems to happen so I'll use the technique.
    # print '=== in utilities init ==='

    #
    # Register the template tag as <application>.templatetags.<template tag lib>
    #
    try:
        for lib in settings.TEMPLATE_TAGS:
            add_to_builtins(lib)
    except AttributeError:
        pass

########################################################################################################################
#
# Dictionary nested set
#
########################################################################################################################


def dict_nested_set(dic, key, value):
    """
    Set value in nested dictionary.

    :param dic: dictionary where value needs to be set
    :type dic: dict
    :param key: a.b.c key into dic
    :type key: unicode
    :param value:
    :type value: varies
    :return: dictionary with value set for specified key
    :rtype: dict
    """
    keys = key.split('.')
    xdic = dic
    for k in keys[:-1]:
        xdic = xdic.setdefault(k, {})
    xdic[keys[-1]] = value
    return dic

########################################################################################################################
#
# Insure that a string startw with a value
#
########################################################################################################################


def ssw(value, lead_string):
    """ If value is not '', insure that it starts with lead_string.

    :param value: current value
    :type value: str or unicode
    :param lead_string: lead string
    :type lead_string: str or unicode
    :return: string starting with lead_string if string is not ''
    :rtype: unicode
    """
    if value and not value.startswith(lead_string):
        return lead_string + value
    return value

########################################################################################################################
#
# Static name generator.  Generates names for ID's etc.
#
########################################################################################################################


def unique_name(base_name='x'):
    """ Returns a unique name of the form 'base_name'_counter.

    .. sourcecode:: python

        unique_name('basename')


    :param base_name: the base name
    :type base_name: str or unicode
    :return: basename+n, ie. x0, x1, ...
    :rtype: str

    .. note:: This function is used by widgets and for other internal purposes to
              create unique names for id(s) and other purposes.
    """
    if not hasattr(unique_name, "counter"):
        unique_name.counter = 0  # it doesn't exist yet, so initialize it
    unique_name.counter += 1
    return '{}_{}'.format(base_name, unique_name.counter)

# todo 3: consider using these instead of inline code.  somewhat briefer but opaque
# def set_classes_style(classes, style, extra_classes=''):
#     if classes or extra_classes:
#         if extra_classes:
#             extra_classes += ' '
#         classes = 'class="{extra_classes}{classes}" '.format(classes=classes, extra_classes=extra_classes)
#     if style:
#         style = 'style="{}" '.format(style)
#     return classes, style
#
#
# def process_iterable(iterable, function, *arguments, **kwargs):
#     print arguments
#     print kwargs
#     # noinspection PyBroadException
#     if isinstance(iterable, basestring):
#         return ''
#     try:
#         rtn = ''
#         for i in iterable:
#             rtn += function(i, *arguments, **kwargs)
#             pass
#         return rtn
#     except:
#         return ''
