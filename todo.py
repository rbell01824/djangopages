#!/usr/bin/env python
# coding=utf-8

""" Some description here

2/19/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '2/19/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

# work list
"""
Make code cleanup pass
add form support
how to deal with a page with a form
add ajax support
how to deal with a page wrt ajax
is it possible to dynamically create/update/delete python objects at runtime so that objects defined in DBs do not require a Db reference?
review graphpages and extract useful functionality/todos.  this is base for userpages!!
get all existing test apps working
add Nose to system for testing
make test routines for all existing functions
add link button
add bootstrap tables
add syntactic suggar for Forms
django pandas
django rest pandas
Move layout objects to their own module
Move content objects to their own module
Add kwargs and attributes to layout & content objects
Restructure RC and content objects properly
Define tests
Set login required everywhere (current scheme only applies to a few urls, not all and there are issues with class views)
Define default graph page template
Add tag view page
Row doesn't scale properly for phones
Check options on markdown wrt line wraps.
"""

# todo 1: review all DWidget(s) to see where DWidgetX should be used.
# todo 1: new application modeled after chartkick setup for distribution
# todo 1: include css and js in the project
# todo 1: write tests
# todo 1: look into fixme_login.html and try to resolve issues
# todo 1: add popup window feature to all graph pages and for graph objects
# todo 1: modify Graph... classes to accommodate type() to decide how to render objects
# todo 1: create class for forms creation

# todo 2: rewrite demo based on DjangoPages and DWidget(s)
# todo 2: add html template option to content objects universally
# todo 2: get local versions of jquery and ALL the bootstrap cruft
# todo 2: look into macros for graph page, see https://github.com/twidi/django-templates-macros
# todo 2: look into hosting services - python anywhere https://www.pythonanywhere.com/
# todo 2: look into https://github.com/jezdez/django-dbtemplates
# todo 2: look into django-taggit-templattags
# todo 2: put jquery.min.js into static
# todo 2: put highcharts.js into static
# todo 2: put chartkick.js into static
# todo 2: format graph page list field widths
# todo 2: start user documentation
# todo 2: About page
# todo 2: Contact page
# todo 2: tests for models, see http://effectivedjango.com/tutorial/models.html

# todo 3: add support for direct highchart interface
# todo 3: add support for ajax interface for highcharts
# todo 3: system level test for navigation
# todo 3: finish listview experiment with cia & countries
# todo 3: sort order on admin vs listview page
# todo 3: deploy on heroku
# todo 3: learn about python eggs
# todo 3: remove chartkick demo from system since no longer needed

