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

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, Template
from django.views.generic.list import ListView
from django.views.generic import View

# Supress unresolvedreferences as these are actually needed inside
# the form exec.
# noinspection PyUnresolvedReferences
from django import forms

from graphpages.models import GraphPage

# noinspection PyUnresolvedReferences
from graphpages.utilities import XGraphPage, XGraphRow, XGraphColumn, XGraphCK

# Supress unresolvedreferences as these are actually needed inside
# the exec for the graph query.
# noinspection PyUnresolvedReferences
# from test_data.models import Countries, CIA
#
# hack that may be a partial solution
# from django.db.models.loading import get_models
# for m in get_models():
#     exec "from %s import %s" % (m.__module__, m.__name__)

# todo 3: workout scheme to automagically import models that might be needed for query
# see https://github.com/django-extensions/django-extensions/blob/master/django_extensions/management/shells.py
# see ... /management/commands/shell_plus.py


from django.conf import settings

# todo 3: install and use python-markdown2 from https://github.com/trentm/python-markdown2


class GraphPageView(View):
    """
    View class for graph pages.  Class has methods to process get/post, build and display graphpage form,
    process form response, run graphpage query, and display resulting graphapage graphs.
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request, graph_pk):
        """
        If there is a form, display it.  When the form is posted control will return to the post method.
        There we will build and display the graph.

        If no form, then build and display the graph here.

        :param request:
        :param graph_pk: Primary key for graphpage
        """

        gpg = get_object_or_404(GraphPage, pk=graph_pk)

        if self.page_has_form(gpg):         # process form if present
            return HttpResponse(self.build_display_form_response(request, gpg))
        else:                               # no form, build and display the graph
            return HttpResponse(self.build_graph_graph_response(request, gpg))

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def post(self, request, graph_pk):
        """
        There was a form.  Process it and if valid build and display the graph.

        :param request:
        :param graph_pk: Primary key for graphpage
        """
        # validate the form
        gpg = GraphPage.objects.get(pk=graph_pk)
        form_class_obj, context = self.get_form_object_and_context(gpg)
        form = form_class_obj(request.POST)
        if form.is_valid():
            return HttpResponse(self.build_graph_graph_response(request, gpg, request.POST))

        # form not valid, so redisplay form with errors
        form_page = self.get_form_page_text(gpg)
        t = Template(form_page)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': form})
        return HttpResponse(t.render(c))

    # noinspection PyMethodMayBeStatic
    def page_has_form(self, gpg):
        """
        Return true if page has form.

        :param gpg: Graph page object
        :type gpg: GraphPage
        """
        return gpg.form or gpg.form_ref

    def build_display_form_response(self, request, gpg):
        """
        Display the graphpage form page.

        :param request:
        :param gpg: graphpage object
        """

        # get the form and form_page
        form_class_obj, context = self.get_form_object_and_context(gpg)
        form_page = self.get_form_page_text(gpg)

        # create unbound form object
        graphform = form_class_obj()

        # render response
        t = Template(form_page)
        c = RequestContext(request, {'graph_pk': str(gpg.pk), 'graphform': graphform, 'form_context': context})
        return t.render(c)

    # noinspection PyUnresolvedReferences
    def get_form_object_and_context(self, gpg):
        """
        Get the forms.form object and any context defined with the form.
        Note, a graphpage form may contain arbitrary python code.  This code is execed and available
        as context when the graphpage query is run and the graphpage graphs displayed.

        :param gpg: graphpage object
        :type gpg: GraphPage
        :return:  # fixme
        :rtype:
        """

        # get the form definition
        form_text = self.get_form_text(gpg)

        # create the form object
        exec (form_text, globals(), locals())
        return GraphForm, locals()

    @staticmethod
    def get_form_text(gpg):
        """
        Get the form text.

        :param gpg: graphpage object
        :type gpg: GraphPage
        :return: text of for
        :rtype: unicode
        """
        if gpg.form_ref:
            form = gpg.form_ref.form.strip()
        else:
            form = gpg.form.strip()

        # todo: here could run through template processor

        if len(form) == 0:
            raise ValidationError('Empty form')

        return form

    @staticmethod
    def get_form_page_text(gpg):
        """
        Get the form page.

        :param gpg: graphpage object
        :type gpg: GraphPage
        :return: text of graph page
        :rtype: unicode
        """

        # get the form page definition
        if gpg.form_page_ref:
            # Note: here is where multiple indirections would need to be dealt with for forms.
            # For the moment just 1 level.
            page = gpg.form_page_ref.form.strip()
        else:
            page = gpg.form_page.strip()

        # todo: here could run through template processor

        # Check to make sure we have a form page.  If not fallback to the default form page.
        if len(page) == 0:
            page = '{% include "default_form_page.html" %}'

        return settings.GRAPHPAGE_FORMPAGEHEADER + page + settings.GRAPHPAGE_FORMPAGEFOOTER

    def build_graph_graph_response(self, request, gpg, form_context=None):
        """
        If there is a query, get it and exec.  Otherwise just display the page.

        :param request: The django request object
        :type request: WSGIRequest
        :param gpg: GraphPage to work with
        :type gpg: GraphPage oject
        :param form_context: The request.POST from the proceeding form if any
        :type form_context: QueryDict, If there was a form the request.POST value
        :return: Response object
        :rtype : object
        """

        # build a render context
        if self.page_has_query(gpg):
            context = self.execute_graphpage_query(request, gpg, form_context)
        else:
            context = form_context if form_context else {}
        _context = Context(context)

        # get the template and render
        gp_text = self.get_graph_page_text(gpg)
        template = Template(gp_text)
        response = template.render(_context)
        return response

    @staticmethod
    def page_has_query(gpg):
        """
        Return true if the graphpage has a query.

        :param gpg: GraphPage object
        :type gpg: GraphPage
        :return: True if the graphpage has a query
        :rtype: bool
        """
        return gpg.query or gpg.query_ref

    # noinspection PyUnusedLocal
    def execute_graphpage_query(self, request, gpg, form_context=None):
        """
        Execute a grasph form query.  This creates a context that is used by the graph page
        to actually display the graph.

        :param request: The request object.
        :type request: WSGIRequest
        :param gpg: Graphpage object
        :type gpg: GraphPage object
        :param form_context: Form context if there was a form.
        :type form_context: dict, if there was a form the POST dictionary
        :return: context dictionary with the results of the query
        :rtype: dict
        """

        # todo 2: make exec safe

        # Save the global context before it gets altered.
        global_context = dict(globals())

        # get the query if there is one, otherwise just return an empty list
        query_text = self.get_query_text(gpg)
        if len(query_text) <= 0:
            return {}

        # See if there is a form _context.  If there is, get it into our local context for exec.
        local_context = {}
        if form_context:
            # noinspection PyUnresolvedReferences
            local_context = form_context.dict()

        # Execute the query.
        exec (query_text, global_context, local_context)

        return local_context

    @staticmethod
    def get_query_text(gpg):
        """
        Get the graphpage query text.

        :param gpg: GraphPage object.
        :type gpg: GraphPage
        :return: Query text or ''
        :rtype: str
        """
        # Note:
        # It it ever becomes necessary to support template tags the following code may be useful
        # There may be some template tags in the query so process them.
        # t = Template(query_text)
        # c = Context(fc)
        # query_text = t.render(c)
        #
        # Note:
        # If it becomes necessary to support markdown this is where it shold be processed.
        #

        # get the query text
        if gpg.query_ref:
            # Note: here is where multiple indirections would need to be dealt with for query.
            # For the moment just 1 level.
            page = gpg.query_ref.query
        else:
            page = gpg.query

        # todo: here could run through template processor

        page = page.strip()
        return page

    @staticmethod
    def get_graph_page_text(gpg):
        """
        Get the graphpage for this graph.  If there is no graphpage page, use the default page template.

        :param gpg: Graphpage object
        :type gpg: GraphPage
        :return: graphpage page text for this graphpage
        :rtype: unicode
        """

        # get the graph page text
        if gpg.graph_page_ref:
            page = gpg.graph_page_ref.graph_page
        else:
            page = gpg.graph_page
        page = page.strip()

        # todo: here could run through template processor

        # if there is no graphpage page text, fall back to the default
        if len(page) == 0:
            page = '{% include "default_graph_page.html" %}'

        # build the page text
        conf = settings.GRAPHPAGE_CONFIG
        page = conf['graphpageheader'] + page + conf['graphpagefooter']
        return page

########################################################################################################################
#
# List graphpage DB entries and allow user to select one
#
########################################################################################################################


class GraphPageListView(ListView):
    """
    ListView for graphpages
    """
    model = GraphPage

    def get_queryset(self):
        """
        Force queryset sort order.
        """
        return GraphPage.objects.all().order_by('title')
