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
from djangopages.libs import ssw


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
    def __init__(self, request, form, button='Submit', action_url=None, method='Post', template=None):
        if not isinstance(button, FormDButton):
            button = FormDButton(button)
        super(FormD, self).__init__(request, form, button, action_url, method, template)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Django form html """
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),

        request, form, button, action_url, method, template = self.args
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
                       '            <div class="col-md-3"></div>\n' \
                       '            <div class="col-md-9">{{ field.errors }}</div>\n' \
                       '        {% else %}' \
                       '        <div class="row">\n' \
                       '        {% endif %}' \
                       '            <div class="col-md-3 text-right">{{ field.label_tag }}</div>\n' \
                       '            <div class="col-md-9">{{ field }}</div>\n' \
                       '            {% if field.help_text %}' \
                       '                <div class="col-md-3 text-right"></div>\n' \
                       '                <div class="col-md-9">{{ field.help_text }}</div>\n' \
                       '            {% endif %}' \
                       '        </div>\n' \
                       '    {% endfor %}\n' \
                       '    {# Include submit button #}' \
                       '    {{ button|safe }}\n' \
                       '</form>\n' \
                       '<!-- /form -->\n'
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button}
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
    def __init__(self, form_groups, button='Submit', form_class=''):
        if not isinstance(button, FormDButton):
            button = FormBButton(button)
        super(FormB, self).__init__(form_groups, button, form_class)

    def generate(self):
        form_groups, button, form_class = self.args
        template = '<!-- bootstrap form -->\n' \
                   '<form role="form" {form_class}>\n' \
                   '{groups}\n' \
                   '{button}\n' \
                   '</form>' \
                   '<!-- / bootstrap form -->'
        form_class = ssw(form_class, 'form-')
        groups = '\n'.join(form_groups)
        rtn = template.format(form_class=form_class, groups=groups, button=button)
        return rtn


class FormGroup(DWidget):
    """ Bootstrap form group """
    def __init__(self, field):
        super(FormGroup, self).__init__(field)

    def generate(self):
        field = self.args
        template = '<div class="form-group">\n' \
                   '</div>'
        pass


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
        template = '<button type="submit" class="btn {button} {classes} {size}" style="{style}">{text}</button>\n'
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