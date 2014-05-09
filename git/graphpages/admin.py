#!/usr/bin/env python

"""

11/18/13 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '11/18/13'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"
__status__ = "dev"

import uuid
import copy

# from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# from django.utils.text import slugify
from django.forms import Textarea, TextInput
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from django_ace import AceWidget

from .models import GraphPage

from taggit.models import TaggedItem
from taggit_suggest.utils import suggest_tags


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

    # noinspection PyUnusedLocal,PyShadowingBuiltins
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


class GraphPageAdmin(admin.ModelAdmin):
    """
    Graphpage admin
    """
    model = GraphPage
    search_fields = ('title', 'description',)
    list_display_links = ('title',)
    list_display = ('display_graph', 'title', 'description', 'tags_slug',)
    readonly_fields = ('tags_suggest',)
    fieldsets = (
        (None, {'classes': ('suit-tab suit-tab-general',),
                'fields': ('title', 'description', ('tags', 'tags_suggest'))}),
        ('Form', {'classes': ('suit-tab suit-tab-form',),
                  'fields': ('form_ref', 'form',)}),
        ('Form Page', {'classes': ('suit-tab suit-tab-formpage',),
                       'fields': ('form_page_ref', 'form_page',)}),
        ('Query', {'classes': ('suit-tab suit-tab-query',),
                   'fields': ('query_ref', 'query',)}),
        ('Graph Page', {'classes': ('suit-tab suit-tab-graphpage',),
                        'fields': ('graph_page_ref', 'graph_page',)}),
    )
    list_filter = (TaggitListFilter,)
    suit_form_tabs = (('general', 'General'),
                      ('form', 'Form'),
                      ('formpage', 'Form Page'),
                      ('query', 'Query'),
                      ('graphpage', 'Graph Page')
                      )
    save_on_top = True
    ordering = ('title',)
    actions = ['delete_selected', 'duplicate_records']
    pass

    # noinspection PyMethodMayBeStatic
    def display_graph(self, obj):
        """
        Create display graph button.
        :type obj: graphpages.models.GraphPage
        :return: HTML for button
        :rtype: unicode
        """
        rtn = u"<div><a class='btn btn-primary btn-sm' href='/graphpages/graphpage/%s'>Display</a></div>" % obj.id
        return rtn
    display_graph.short_description = ''
    display_graph.allow_tags = True

    # noinspection PyMethodMayBeStatic
    def tags_slug(self, obj):
        """
        Make list of tags seperated by ';'
        :type obj: graphpages.models.GraphPage
        :return: list of tags
        :rtype: unicode
        """
        if len(obj.tags.names()) == 0:
            return '--'
        rtn = ''
        for tag in obj.tags.names():
            rtn += '; ' + tag
        return rtn[1:]

    # noinspection PyMethodMayBeStatic
    def tags_suggest(self, obj):
        """
        Suggest tags based on description
        :type obj: graphpages.models.GraphPage
        :return: suggested tags
        :rtype: unicode
        """
        rtn = suggest_tags(obj.description).values_list('name', flat=True)
        return ', '.join(rtn)

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Set widgets for the form fields.
        :type db_field: CharField or TextField or ForeignKey or TaggableManager or unknown
        :param kwargs:
        :return: modified formfield widget list
        """
        if db_field.name == 'title':
            kwargs['widget'] = TextInput(attrs={'class': 'span12', 'size': '140'})
        if db_field.name == 'description':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '2', 'cols': '140'})
        if db_field.name == 'form':
            # kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
            kwargs['widget'] = AceWidget(mode='python', theme='chrome', width='100%', height='500px',
                                         attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'form_page':
            # kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
            kwargs['widget'] = AceWidget(mode='html', theme='chrome', width='100%', height='500px',
                                         attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'query':
            # kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
            kwargs['widget'] = AceWidget(mode='python', theme='chrome', width='100%', height='500px',
                                         attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'graph_page':
            # kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
            kwargs['widget'] = AceWidget(mode='html', theme='chrome', width='100%', height='500px',
                                         attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        return super(GraphPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def duplicate_records(self, request, queryset):
        """
        Duplicate the selected records
        :param queryset: Queryset of records to duplicate
        :param request: Request object.  Unused.
        :return: None
        """
        for obj in queryset:
            newobj = copy.deepcopy(obj)
            newobj.id = None
            newobj.title += ' duplicate ' + uuid.uuid1().hex
            newobj.save()
            # noinspection PyStatementEffect
            newobj.tags.add(*obj.tags.all())
        return
    duplicate_records.short_description = "Duplicate selected records"

admin.site.register(GraphPage, GraphPageAdmin)
