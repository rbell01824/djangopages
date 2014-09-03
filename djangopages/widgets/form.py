#!/usr/bin/env python
# coding=utf-8

"""
Form Widgets Overview
**************************

.. module:: form
   :synopsis: Provides DjangoPage widgets for forms

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets for forms.

9/1/14 - Initial creation

Widgets
=======
"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '9/1/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

from django.template import Context, Template
from django.core.context_processors import csrf

from djangopages.widgets.widgets import DWidget, DWidgetT
from djangopages.libs import ssw, unique_name


class FormD(DWidget):
    """ Django form widget

    .. sourcecode:: python

        Form(request_obj, django_form, submit_text, action_url)

    :param request: request object
    :type request: WSGIRequest
    :param form: form object
    :type form: forms.Form
    :param button: text for submit button or FormDButton object.  If None, no submit button.
    :type button: str or unicode or FormDButton.
    :param action_url: submit action url
    :type action_url: str or unicode
    :param template: override default widget template
    :type template: str or unicode
    """
    def __init__(self, request, form, button='Submit', action_url=None, label_width=3, method='Post', template=None):
        if not isinstance(button, FormDButton):
            button = FormDButton(button)
        super(FormD, self).__init__(request, form, button, action_url, label_width, method, template)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Django form html """
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),

        request, form, button, action_url, label_width, method, template = self.args
        if not template:
            template = '<!-- form -->\n' \
                       '<form role="form" method="{{ method }}" class="form" action="{{ action_url }}">\n' \
                       '    <!-- csrf -->{% csrf_token %}<!-- / csrf -->\n' \
                       '    {# Include the hidden fields #}\n' \
                       '    {% for hidden in form.hidden_fields %}\n' \
                       '        {{ hidden }}\n' \
                       '    {% endfor %}\n' \
                       '    {# Include the visible fields #}\n' \
                       '    {% for field in form.visible_fields %}\n' \
                       '        {% if field.errors %}' \
                       '        <div class="row bg-danger">\n' \
                       '            <div class="col-md-{{ label_width }}"></div>\n' \
                       '            <div class="col-md-9">{{ field.errors }}</div>\n' \
                       '        {% else %}' \
                       '        <div class="row">\n' \
                       '        {% endif %}' \
                       '            <div class="col-md-{{ label_width }} text-right">{{ field.label_tag }}</div>\n' \
                       '            <div class="col-md-9">{{ field }}</div>\n' \
                       '            {% if field.help_text %}' \
                       '                <div class="col-md-{{ label_width }}"></div>\n' \
                       '                <div class="col-md-9">{{ field.help_text }}</div>\n' \
                       '            {% endif %}' \
                       '        </div>\n' \
                       '    {% endfor %}\n' \
                       '    {# Include submit button #}' \
                       '    {{ button|safe }}\n' \
                       '</form>\n' \
                       '<!-- /form -->\n'
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button,
             'label_width': label_width}
        c.update(csrf(request))
        rtn = t.render(Context(c))
        return rtn


class FormDButton(DWidgetT):
    """ Form django button definition

    .. sourcecode:: python

        FormDButton('Text of button')

    :param text: text
    :type text: str or unicode or tuple
    :param button: default 'btn-default', button type per bootstrap
    :type button: str or unicode
    :param size: default '', button size per bootstrap
    :type size: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    """
    def __init__(self, text='Submit', button='btn-primary', size='', classes='', style=''):
        template = '<div class="row">\n' \
                   '    <div class="col-md-3 text-right">\n' \
                   '        <input type="submit" value="{text}" ' \
                   '            class="btn {button} {size} {classes}" style="{style}" />\n' \
                   '    </div>\n' \
                   '</div>\n'
        button = ssw(button, 'btn-')
        size = ssw(size, 'btn-')
        super(FormDButton, self).__init__(template, {'text': text,
                                                     'button': button, 'size': size,
                                                     'classes': classes, 'style': style})


class FormB(DWidget):
    """ Bootstrap form """
    def __init__(self, request, form, button='Submit', action_url=None, method='Post', horinl=''):
        if not isinstance(button, FormDButton):
            button = FormBButton(button)
        super(FormB, self).__init__(request, form, button, action_url, method, horinl)

    def generate(self):
        request, form, button, action_url, method, horinl = self.args
        template = '<!-- form -->\n' \
                   '<form role="form" method="{{ method }}" class="{{form_class}}" action="{{ action_url }}">\n' \
                   '    <!-- csrf -->{% csrf_token %}<!-- / csrf -->\n' \
                   '    {# Include the hidden fields #}\n' \
                   '    {% for hidden in form.hidden_fields %}\n' \
                   '        {{ hidden }}\n' \
                   '    {% endfor %}\n' \
                   '    {# Include the visible fields #}\n' \
                   '    {% for field in form.visible_fields %}\n' \
                   '        {% if field.errors %}' \
                   '        <div class="form-group bg-danger">\n' \
                   '            {{ field.errors }}\n' \
                   '        {% else %}' \
                   '        <div class="form-group">\n' \
                   '        {% endif %}' \
                   '            <label for={{ field.id_for_label }} {{ label_class| safe }}>{{ field.label }}</label>\n' \
                   '            <input type="{{ field.field.widget.input_type}}" id={{ field.id_for_label }} ' \
                   '                   name="{{ field.name }}" class="form-control" value="{{ field.value }}" >\n' \
                   '            {% if field.help_text %}' \
                   '                <p class="help-block">{{ field.help_text }}</p>\n' \
                   '            {% endif %}' \
                   '        </div>\n' \
                   '    {% endfor %}\n' \
                   '    {# Include submit button #}' \
                   '    {{ button|safe }}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        #
        # template = '<!-- bootstrap form -->\n' \
        #            '<form role="form" {form_class}>\n' \
        #            '{groups}\n' \
        #            '{button}\n' \
        #            '</form>' \
        #            '<!-- / bootstrap form -->'
        # template_group = '<!-- bootstrap group -->\n' \
        #                  '<div class="form-group">' \
        #                  '    <label for="{fld_id}" >{fld_label}</label>\n' \
        #                  '    <input type="{fld_type}" id="{fld_id}" {fld_other}>\n' \
        #                  '    {fld_help}' \
        #                  '</div>\n' \
        #                  '<!-- / bootstrap group -->\n'
        # groups = ''
        # for fld_name in form.fields:
        #     print fld_name
        #     fld = form.fields[fld_name]
        #     fld_id = unique_name(fld_name)
        #     fld_label = fld.label
        #     fld_type = fld.widget.input_type
        #     fld_other = ''
        #     groups += '\n' + template_group.format(fld_id=fld_id, fld_label=fld_label,
        #                                            fld_type=fld_type, fld_other=fld_other)
        # rtn = template.format(form_class=form_class, groups=groups, button=button)
        form_class = ''
        label_class = ''
        if not horinl:
            pass
        elif horinl == 'inline':
            pass
        elif isinstance(horinl, int):
            form_class = 'form-horizontal'
            label_class = 'class="col-md-{} control-label" '.format(horinl)
        form_class = ssw(form_class, 'form-')
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button,
             'form_class': form_class, 'label_class': label_class}
        c.update(csrf(request))
        rtn = t.render(Context(c))
        return rtn


class FormBButton(DWidgetT):
    """ Form bootstrap button definition

    .. sourcecode:: python

        FormDButton('Text of button')

    :param text: text
    :type text: str or unicode or tuple
    :param button: default 'btn-default', button type per bootstrap
    :type button: str or unicode
    :param size: default '', button size per bootstrap
    :type size: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    """
    def __init__(self, text='Submit', button='btn-primary', size='', classes='', style=''):
        # template = '<button type="submit" class="btn {button} {classes} {size}" style="{style}">{text}</button>\n'
        template = '<div class="row">\n' \
                   '    <div class="col-md-3 text-right">\n' \
                   '        <input type="submit" value="{text}" ' \
                   '            class="btn {button} {size} {classes}" style="{style}" />\n' \
                   '    </div>\n' \
                   '</div>\n'
        button = ssw(button, 'btn-')
        size = ssw(size, 'btn-')
        modal_id = None
        super(FormBButton, self).__init__(template, {'text': text,
                                                     'button': button, 'size': size,
                                                     'classes': classes, 'style': style})

#
# # todo 1: add support for normal bootstrap forms
# # todo 1: add id to Form
#
