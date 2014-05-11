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
from taggit.models import TaggedItem
from taggit_suggest.utils import suggest_tags

from djangopages.models import DjangoPage
from djangopages.dpage import TaggitListFilter


class DjangoPageAdmin(admin.ModelAdmin):
    """
    DjangoPage admin
    """
    model = DjangoPage
    search_fields = ('title', 'description',)
    list_display_links = ('title',)
    list_display = ('display_graph', 'title', 'description', 'tags_slug',)
    readonly_fields = ('tags_suggest',)
    fieldsets = (
        (None, {'classes': ('suit-tab suit-tab-general',),
                'fields': ('title', 'description', ('tags', 'tags_suggest'))}),
        ('Query', {'classes': ('suit-tab suit-tab-query',),
                   'fields': ('template', 'djangopage',)}),
    )
    list_filter = (TaggitListFilter,)
    suit_form_tabs = (('general', 'General'),
                      ('query', 'Query'),
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
        if db_field.name == 'template':
            kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '1', 'cols': '80'})
            # kwargs['widget'] = AceWidget(mode='python', theme='chrome', width='100%', height='500px',
            #                              attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        if db_field.name == 'djangopage':
            # kwargs['widget'] = Textarea(attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
            kwargs['widget'] = AceWidget(mode='python', theme='chrome', width='100%', height='500px',
                                         attrs={'class': 'span12', 'rows': '30', 'cols': '140'})
        return super(DjangoPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

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

admin.site.register(DjangoPage, DjangoPageAdmin)
