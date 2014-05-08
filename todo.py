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
Define tests
Set login required everywhere (current scheme only applies to a few urls, not all and there are issues with class views)
Define default graph page template
Add tag view page
Row doesn't scale properly for phones
Check options on markdown wrt line wraps.
"""

# todo 1: include css and js in the project
# todo 1: write tests
# todo 1: look into fixme_login.html and try to resolve issues

# todo 1: add GraphColumn to classes
# todo 1: modify Graph... classes to accommodate type() to decide how to render objects
# todo 1: create class for forms creation

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

# todo 3: system level test for navigation
# todo 3: finish listview experiment with cia & countries
# todo 3: sort order on admin vs listview page
# todo 3: deploy on heroku
# todo 3: learn about python eggs

