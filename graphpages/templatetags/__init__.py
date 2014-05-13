#!/usr/bin/env python
# coding=utf-8

""" Some description here

2/23/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '2/23/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

########################################################################################################################

# Load the default template tags.
# This insures that custom template tags are always available to Django's
# template render process.

# fixme: this shouldn't be needed, look into it.  django pages should override

from djangopages.dpage import load_templatetags
load_templatetags()
