#!/usr/bin/env python
# coding=utf-8

""" Some description here

3/15/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/15/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

import re

from taggit_suggest.models import TagKeyword, TagRegex
from taggit.models import Tag


def _suggest_keywords(content):
    """
    Suggest by keywords
    :type content: unicode, content to check
    :rtype: set of tag id's for keywords that match content
    """
    suggested_keywords = set()
    keywords = TagKeyword.objects.all()
    # noinspection PyStatementEffect
    content_lower = content.lower()

    for k in keywords:
        # Use the stem if available, otherwise use the whole keyword
        # if k has uppercase match with case, otherwise match everything lowercase
        if k.stem:
            # noinspection PyStatementEffect
            kstr = k.stem
        else:
            # noinspection PyStatementEffect
            kstr = k.keyword
        if kstr.lower() == kstr:
            if kstr in content_lower:
                suggested_keywords.add(k.tag_id)
        else:
            if kstr in content:
                suggested_keywords.add(k.tag_id)
    return suggested_keywords


def _suggest_regexes(content):
    """
    Suggest by regular expressions
    :type content: unicode, content to check
    :rtype: set of tag id's for regexs that match content
    """
    # Grab all regular expressions and compile them
    suggested_regexes = set()
    regex_keywords = TagRegex.objects.all()

    # Look for our regular expressions in the content
    for r in regex_keywords:
        if re.search(r.regex, content):
            suggested_regexes.add(r.tag_id)

    return suggested_regexes


def suggest_tags(content):
    """
    Suggest tags based on text content
    :type content: unicode, content to check
    :rtype: queryset of tag ids that match keywords or regexes
    """
    suggested_keywords = _suggest_keywords(content)
    suggested_regexes = _suggest_regexes(content)
    suggested_tag_ids = suggested_keywords | suggested_regexes

    return Tag.objects.filter(id__in=suggested_tag_ids)
