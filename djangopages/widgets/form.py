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
from django import forms

from djangopages.widgets.widgets import DWidget, DWidgetT
from djangopages.libs import ssw, add_classes

# class ProjectView(View):`
#     @method_decorator(csrf_protect)
#     def get(self, request, *args, **kwargs):
#
# For example, in the Cheetah template language, your form could contain the following:
#
# <div style="display:none">
#     <input type="hidden" name="csrfmiddlewaretoken" value="$csrf_token"/>
# </div>


def _csrf_(request):
    rtn = '<!-- csrf -->\n' \
          '<div style="display:none">' \
          '<input type="hidden" name="csrfmiddlewaretoken" value="{}"/>' \
          '</div>\n' \
          '<!-- / csrf -->'.format(request.COOKIES['csrftoken'])
    return rtn


class Form(forms.Form):
    """ Extension to forms.Form to support various DWidget features """
    def __getattr__(self, item, default=None):
        try:
            return self[item]
        except:
            if default:
                return default
            raise AttributeError


class DForm(DWidget):
    """ Django form widget

    .. sourcecode:: python

        DForm(request_obj, django_form, submit_text, action_url)

    :param request: request object
    :type request: WSGIRequest
    :param form: form object
    :type form: forms.Form
    :param button: text for submit button or DFormButton object.  If None, no submit button.
    :type button: str or unicode or DFormButton.
    :param action_url: submit action url
    :type action_url: str or unicode
    :param template: override default widget template
    :type template: str or unicode
    """
    template = '\n<!-- form -->\n' \
               '<form role="form" method="{method}" class="form" action="{action_url}">\n' \
               '    {csrf_token}\n' \
               '    {form_text}\n' \
               '    {button}\n' \
               '</form>\n' \
               '<!-- /form -->\n'

    def __init__(self, request, form, form_type='', button='Submit', action_url=None, method='Post', template=None):
        if not isinstance(button, FormButton):
            button = FormButton(button)
        super(DForm, self).__init__(request, form, form_type, button, action_url, method, template)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Django form html """
        request, form, form_type, button, action_url, method, template = self.args
        if form_type == 'p':
            form_text = form.as_p()
            pass
        elif form_type == 'ul':
            form_text = '<ul>' + form.as_ul() + '</ul>'
            pass
        else:
            form_text = '<table>' + form.as_table() + '</table>'
            pass
        if not action_url:
            action_url = request.path
        if not template:
            template = self.template
        csrf_token = _csrf_(request)
        rtn = template.format(method=method, action_url=action_url, csrf_token=csrf_token,
                              form_text=form_text, button=button)
        return rtn


class FormButton(DWidgetT):
    """ Form button definition

    .. sourcecode:: python

        DFormButton('Text of button')

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
        template = '\n<!-- form button -->\n' \
                   '<input type="submit" value="{text}" ' \
                   '   class="btn {button} {size} {classes}" style="{style}" />\n' \
                   '<!-- / form button -->\n'
        button = ssw(button, 'btn-')
        size = ssw(size, 'btn-')
        super(FormButton, self).__init__(template, {'text': text,
                                                    'button': button, 'size': size,
                                                    'classes': classes, 'style': style})


class DBForm(DWidget):
    """ Django form widget

    .. sourcecode:: python

        Form(request_obj, django_form, submit_text, action_url)

    :param request: request object
    :type request: WSGIRequest
    :param form: form object
    :type form: forms.Form
    :param button: text for submit button or DFormButton object.  If None, no submit button.
    :type button: str or unicode or DFormButton.
    :param action_url: submit action url
    :type action_url: str or unicode
    :param template: override default widget template
    :type template: str or unicode
    """
    def __init__(self, request, form, button='Submit', action_url=None, method='Post', width=(3, 6), template=None):
        if not isinstance(button, FormButton):
            button = FormButton(button)
        super(DBForm, self).__init__(request, form, button, action_url, method, width, template)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Django form html """
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),

        request, form, button, action_url, method, width, template = self.args
        if not template:
            template = '<!-- form -->\n' \
                       '<form role="form" method="{{ method }}" class="form" action="{{ action_url }}">\n' \
                       '    <!-- csrf -->{% csrf_token %}<!-- / csrf -->\n' \
                       '    {# Include the hidden fields #}\n' \
                       '    {% for hidden in form.hidden_fields %}\n' \
                       '        {{ hidden }}\n' \
                       '    {% endfor %}\n' \
                       '    {# Include non-field errors #}\n' \
                       '         {{ form.non_field_errors }}\n' \
                       '    {# Include the visible fields #}\n' \
                       '    {% for field in form.visible_fields %}\n' \
                       '        {% if field.errors %}' \
                       '        <div class="row bg-danger">\n' \
                       '            <div class="col-md-{{ l_width }}"></div>\n' \
                       '            <div class="col-md-{{ i_width }}">{{ field.errors }}</div>\n' \
                       '        </div>\n' \
                       '        <div class="row bg-danger">\n' \
                       '        {% else %}' \
                       '        <div class="row">\n' \
                       '        {% endif %}' \
                       '            <div class="col-md-{{ l_width }} text-right">{{ field.label_tag }}</div>\n' \
                       '            <div class="col-md-{{ i_width }}">{{ field }}</div>\n' \
                       '        </div>\n' \
                       '        {% if field.help_text %}' \
                       '        <div class="row">\n' \
                       '            <div class="col-md-{{ l_width }}"></div>\n' \
                       '            <div class="col-md-{{ i_width }}">{{ field.help_text }}</div>\n' \
                       '        </div>\n' \
                       '        {% endif %}' \
                       '    {% endfor %}\n' \
                       '    {# Include submit button #}' \
                       '    <div class="row">\n' \
                       '        <div class="col-md-{{ l_width }} text-right">\n' \
                       '            {{ button|safe }}\n' \
                       '        </div>\n' \
                       '    </div>\n' \
                       '</form>\n' \
                       '<!-- /form -->\n'
        l_width, i_width = width
        if not action_url:
            action_url = request.path
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button,
             'l_width': l_width, 'i_width': i_width}
        c.update(csrf(request))
        rtn = t.render(Context(c))
        return rtn

# fixme: make BForm a basic bootstrap form widget and create BIForm (inline) and BHForm (horizontal)


class BForm(DWidget):
    """ Bootstrap form """
    def __init__(self, request, form, button='Submit', action_url=None, method='Post'):
        if not isinstance(button, FormButton):
            button = FormButton(button)
        super(BForm, self).__init__(request, form, button, action_url, method)

    def generate(self):
        request, form, button, action_url, method = self.args
        template = '<!-- form -->\n' \
                   '<form role="form" method="{{ method }}" action="{{ action_url }}">\n' \
                   '    <!-- csrf -->{% csrf_token %}<!-- / csrf -->\n' \
                   '    {# Include the hidden fields #}\n' \
                   '    {% for hidden in form.hidden_fields %}\n' \
                   '        {{ hidden }}\n' \
                   '    {% endfor %}\n' \
                   '    {# Include non-field errors #}\n' \
                   '         {{ form.non_field_errors }}\n' \
                   '    {# Include the visible fields #}\n' \
                   '    {% for field in form.visible_fields %}\n' \
                   '        {% if field.errors %}' \
                   '        <div class="form-group bg-danger">\n' \
                   '            {{ field.errors }}\n' \
                   '        {% else %}' \
                   '        <div class="form-group">\n' \
                   '        {% endif %}' \
                   '            <label for={{ field.id_for_label }}>{{ field.label }}</label>\n' \
                   '            {% if field.data %}' \
                   '            <input type="{{ field.field.widget.input_type}}" id={{ field.id_for_label }} ' \
                   '             name="{{field.name}}" class="form-control" value="{{field.data}}" >\n' \
                   '            {% else %}' \
                   '            <input type="{{ field.field.widget.input_type}}" id={{ field.id_for_label }} ' \
                   '             name="{{field.name}}" class="form-control" placeholder="{{field.field.initial}}" >\n' \
                   '            {% endif %}' \
                   '            {% if field.help_text %}' \
                   '                <p class="help-block">{{ field.help_text }}</p>\n' \
                   '            {% endif %}' \
                   '        </div>\n' \
                   '    {% endfor %}\n' \
                   '    {# Include submit button #}' \
                   '    {{ button|safe }}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        if not action_url:
            action_url = request.path
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button}
        c.update(csrf(request))
        rtn = t.render(Context(c))
        return rtn


class BCB(DWidget):
    """ Bootstrap check box field """
    def __init__(self, fld, lbl_width=None, fld_width=None):
        super(BCB, self).__init__(fld, lbl_width, fld_width)

    def generate(self):
        fld, lbl_width, fld_width = self.args
        if not lbl_width and not fld_width:
            template = '<div class="checkbox">\n' \
                       '    <label>\n' \
                       '    {field} {label}\n' \
                       '    </label>' \
                       '{fld_help}' \
                       '</div>\n'
            if fld.help_text:
                fld_help = '    <p>{}</p>'.format(fld.help_text)
            else:
                fld_help = ''
            rtn = template.format(label=fld.label, field=fld, fld_help=fld_help)
            return rtn
        elif lbl_width and fld_width:
            template = '<div class="form-group">\n' \
                       '    {label}\n' \
                       '    <div class="col-md-{fld_width}>\n' \
                       '        {field}>\n' \
                       '    </div>' \
                       '{fld_help}' \
                       '</div>\n'
            label = fld.label_tag()
            label_classes = 'class="col-md-{} control-label" '.format(lbl_width)
            label = label.replace('<label', '<label ' + label_classes, 1)
            fld.css_classes('form-control')
            if fld.help_text:
                fld_help = '    <p>{}</p>'.format(fld.help_text)
            else:
                fld_help = ''
            rtn = template.format(label=label, fld_width=fld_width, field=fld, fld_help=fld_help)
            return rtn
        raise AttributeError


class BFG(DWidget):
    """ Bootstrap form group field """
    def __init__(self, fld, lbl_width=None, fld_width=None):
        super(BFG, self).__init__(fld, lbl_width, fld_width)

    def generate(self):
        fld, lbl_width, fld_width = self.args
        if not lbl_width and not fld_width:
            # template = '<div class="form-group">\n' \
            #            '    <label for="{fld_label_id}">{fld_label}</label>\n' \
            #            '    <input type="{fld_type}" class="form-control" id="{fld_id}" ' \
            #            'placeholder="{fld_placeholder}">\n' \
            #            '{fld_help}' \
            #            '</div>\n'
            template = '<div class="form-group">\n' \
                       '    {label}\n' \
                       '    {field}\n' \
                       '{fld_help}' \
                       '</div>\n'
            field = add_classes(str(fld), 'form-control')
            if fld.help_text:
                fld_help = '    <p>{}</p>'.format(fld.help_text)
            else:
                fld_help = ''
            rtn = template.format(label=fld.label_tag(), field=field, fld_help=fld_help)
            return rtn
        elif lbl_width and fld_width:
            template = '<div class="form-group">\n' \
                       '    {label}\n' \
                       '    <div class="col-md-{fld_width}>\n' \
                       '        {field}>\n' \
                       '    </div>' \
                       '{fld_help}' \
                       '</div>\n'
            label = fld.label_tag()
            label_classes = 'class="col-md-{} control-label" '.format(lbl_width)
            label = label.replace('<label', '<label ' + label_classes, 1)
            fld.css_classes('form-control')
            if fld.help_text:
                fld_help = '    <p>{}</p>'.format(fld.help_text)
            else:
                fld_help = ''
            rtn = template.format(label=label, fld_width=fld_width, field=fld, fld_help=fld_help)
            return rtn
        raise AttributeError


class BF(DWidget):
    """ Bootstrap form """
    # def __init__(self, request, form, button='Submit', action_url=None, method='Post'):
    def __init__(self, request, *form):
        super(BF, self).__init__(request, form)

    def generate(self):
        request, form = self.args
        template = '<!-- form -->\n' \
                   '<form role="form" method="Post" action="{action_url}">\n' \
                   '    {csrf}\n' \
                   '    {form}' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        action_url = request.path
        if isinstance(form, tuple):
            form = '\n'.join(form)
        rtn = template.format(action_url=action_url, csrf=_csrf_(request), form=form)
        return rtn


# todo 1: add id to Form
