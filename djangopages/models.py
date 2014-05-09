#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/7/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/7/14'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"

########################################################################################################################

from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

from taggit.managers import TaggableManager


class DjangoPage(TitleSlugDescriptionModel, TimeStampedModel):
    """
    Class defines a DjangoPage records.

    Base models provide the following fields:
        Title
        Slug
        Description
        Created
        Modified
    """
    tags = TaggableManager(blank=True)
    template = models.TextField(blank=True)
    # The Django/python to get the form data
    djangopage = models.TextField(blank=True)

    class Meta:
        verbose_name = "DjangoPage"
        verbose_name_plural = "DjangoPage"

    def __unicode__(self):
        return u'{}'.format(self.title)
    pass

