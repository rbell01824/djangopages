#!/usr/bin/env python
# coding=utf-8

""" Some description here

5/3/14 - Initial creation

Shamelessly copied from http://www.soyoucode.com/2011/set-variable-django-template

To use:

{% load set_var %}

{% set a = 3 %}
{% set b = some_context_variable %}
{% set c = "some string" %}

Value of a is {{a}}
Value of b is {{b}}
Value of c is {{c}}

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '5/3/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

from django import template

register = template.Library()


class SetVarNode(template.Node):

    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)
