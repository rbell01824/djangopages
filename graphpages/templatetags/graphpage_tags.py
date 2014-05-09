#!/usr/bin/env python
# coding=utf-8

""" Custom template tags to support graphpages

3/23/14 - Initial creation

"""

from __future__ import unicode_literals
import logging

log = logging.getLogger(__name__)

__author__ = 'richabel'
__date__ = '3/23/14'
__license__ = "All rights reserved"
__version__ = "0.1"
__status__ = "dev"

import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _
from django.template.base import Context, Node
from django import template
from django.template import Template, Variable, TemplateSyntaxError

# These are needed inside the exec for the form tag and crispy
# noinspection PyUnresolvedReferences
from django import forms

import re


register = template.Library()

########################################################################################################################
#
# Markdown support
#
#  todo 3: look into using markdown2
#
########################################################################################################################


@register.filter(name='graphpage_markdown', is_safe=True)
@stringfilter
def graphpage_markdown(value):
    """
    Process markdown.
    :type value: unicode, the value to process
    :rtype: unicode, html result from markdown processing
    """
    extensions = []
    # extensions = ["nl2br", ]                    # enable new line to break extension

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       safe_mode=True,
                                       enable_attributes=False))

########################################################################################################################
#
# Expr support
#
# see: https://djangosnippets.org/snippets/9/
#
# This tag can be used to calculate a python expression, and save it into a
# template variable which you can reuse later or directly output to template.
# So if the default django tag can not be suit for your need, you can use it.
#
# How to use it
#
# {% expr "1" as var1 %}
# {% expr [0, 1, 2] as var2 %}
# {% expr _('Menu') as var3 %}
# {% expr var1 + "abc" as var4 %}
# ...
# {{ var1 }}
# for 0.2 version
#
# {% expr 3 %}
# {% expr "".join(["a", "b", "c"]) %}
# Will directly output the result to template
#
# Syntax
#
# {% expr python_expression as variable_name %}
# python_expression can be valid python expression, and you can even
# use _() to translate a string. Expr tag also can used context variables.
#
########################################################################################################################

# todo 2: clean up this code


class ExprNode(template.Node):
    """
    Expr template tag node.
    """
    def __init__(self, expr_string, var_name):
        self.expr_string = expr_string
        self.var_name = var_name

    def render(self, context):
        """
        Render method for expr tag.

        :param context:
        :return:
        :rtype:
        :raise:
        """
        try:
            clist = list(context)
            clist.reverse()
            # noinspection PyDictCreation
            d = {}
            d['_'] = _
            for c in clist:
                for item in c:
                    if isinstance(item, dict):
                        d.update(item)
            if self.var_name:
                # context[self.var_name] = eval(self.expr_string, d)
                # context.dicts[0][self.varname] = eval(self.expr_string, d)
                # todo 2: this is a hack to run in the global context, fixme fixme fixme
                # context.dicts[0][self.varname] = eval(self.expr_string)
                context[self.var_name] = eval(self.expr_string)
                return ''
            else:
                return str(eval(self.expr_string, d))
        except:
            raise
        pass

r_expr = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)


# noinspection PyUnusedLocal
def do_expr(parser, token):
    """
    Compiler for expr template tag.

    :param parser:
    :param token:
    :return: :rtype: :raise template.TemplateSyntaxError:
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
    m = r_expr.search(arg)
    if m:
        expr_string, var_name = m.groups()
    else:
        if not arg:
            raise template.TemplateSyntaxError, "%r tag at least require one argument" % tag_name

        expr_string, var_name = arg, None
    return ExprNode(expr_string, var_name)
do_expr = register.tag('expr', do_expr)

########################################################################################################################
#
# Renders context variable.
#
# See: https://djangosnippets.org/snippets/1373/
# This is a template tag that works like {% include %}, but instead of loading a template
# from a file, it uses some text from the current context, and renders that as though it
# were itself a template. This means, amongst other things, that you can use template tags
# and filters in database fields.
#
# For example, instead of:
#
# {{ context_variable }}
#
# you could use:
#
# {% render_as_template context_variable %}
#
# Then you can use template tags (such as {% url showprofile user.id %}) in flat pages,
# stored in the database.
#
# The template is rendered with the current context.
#
# Warning - only allow trusted users to edit content that gets rendered with this tag.
#
########################################################################################################################


class RenderAsTemplateNode(template.Node):
    """
    Renders variable
    """
    def __init__(self, item_to_be_rendered):
        """
        :param item_to_be_rendered: the item to be rendered, ex. {% piechart %}
        :type item_to_be_rendered: unicode
        """
        self.item_to_be_rendered = Variable(item_to_be_rendered)

    def render(self, context):
        """
        Render variable in context.
        :param context: Current template context.
        :type context: dict
        :return: Rendered variable
        :rtype: unicode
        """
        try:
            actual_item = self.item_to_be_rendered.resolve(context)
            return Template(actual_item).render(context)
        except template.VariableDoesNotExist:
            return ''


def render_as_template(parser, token):
    """

    :param parser:
    :param token:
    :return: :rtype: :raise TemplateSyntaxError:
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'%s' takes only one argument"
                                  " (a variable representing a template to render)" % bits[0])
    return RenderAsTemplateNode(bits[1])

render_as_template = register.tag(render_as_template)

