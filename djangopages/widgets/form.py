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

import functools

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


def _getattr_(obj, item, default):
    if hasattr(obj, item):
        return getattr(obj, item)
    return default


class Form(DWidget):
    """ Extension to forms.Form to support various DWidget features """

    def __init__(self, request, form):
        super(Form, self).__init__()
        self.request = request
        self.form = form
        return

    def generate(self):
        self.resolve_attrs()
        dispatch = {'p': self._as_p,
                    'ul': self._as_ul,
                    'table': self._as_table,
                    'b': self._as_bootstrap,
                    'bootstrap': self._as_bootstrap,
                    'h': self._as_bootstrap_horizontal,
                    'horizontal': self._as_bootstrap_horizontal,
                    }
        rndr = dispatch.get(self.form_type, self._as_bootstrap)
        rtn = rndr()
        return rtn

    # def __getattr__(self, item, default):
    #     try:
    #         return getattr(self, item, default)
    #     except TypeError:
    #         return default

    # noinspection PyAttributeOutsideInit
    def resolve_attrs(self):
        self.button = _getattr_(self, 'button', _getattr_(self.form, 'button', 'Submit'))
        if self.button and not isinstance(self.button, FormButton):
            self.button = FormButton(self.button).render()
        self.method = _getattr_(self, 'method', _getattr_(self.form, 'method', 'Post'))
        self.action_url = _getattr_(self, 'action_url', _getattr_(self.form, 'action_url', self.request.path))
        self.form_type = _getattr_(self, 'form_type', _getattr_(self.form, 'form_type', ''))
        self.layout = _getattr_(self, 'layout', _getattr_(self.form, 'layout', None))
        return

    #
    # Basic Django support ############################################################################################
    #

    def _as_p_ul_table(self, rtn):
        template = '<!-- form -->\n' \
                   '<form role="form" method="{method}" action="{action_url}">\n' \
                   '    {csrf}\n' \
                   '    {form}\n' \
                   '    {button}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        rtn = template.format(method=self.method, action_url=self.action_url,
                              csrf=_csrf_(self.request), form=rtn,
                              button=self.button)
        return rtn

    def _as_p(self):
        rtn = self.form.as_p()
        return self._as_p_ul_table(rtn)

    def _as_ul(self):
        rtn = '<ul>' + self.form.as_ul() + '</ul>'
        return self._as_p_ul_table(rtn)

    def _as_table(self):
        rtn = '<table>' + self.form.as_table() + '</table>'
        return self._as_p_ul_table(rtn)

    #
    # bootstrap default support #######################################################################################
    #

    def b_base(self, form, bound_field, field_name, form_control='form-control', template=None):
        """ Output bootstrap field

        :param form: The form
        :param bound_field: A bound field
        :param field_name: The field's name
        :param form_control: Class to apply to the field's input html or None
        :type form_control: unicode or None
        :return:
        """
        if not template:
            template = '<div class="form-group {group_extra}">\n' \
                       '    {label}\n' \
                       '    {errors}\n' \
                       '    {field}\n' \
                       '    {help}' \
                       '</div>\n'
        fld_id = bound_field.id_for_label
        fld_label = add_classes(bound_field.label_tag(), 'control-label')
        field = str(bound_field)
        if form_control:
            field = add_classes(field, 'form-control')
        if bound_field.errors:
            fld_errors = '    <span style="color:#a94442;>{}</span>'.format(bound_field.errors)
            group_extra = 'has-error'
        else:
            fld_errors = ''
            if self.request.POST:
                group_extra = 'has-success'
            else:
                group_extra = ''
        if bound_field.help_text:
            fld_help = '    <p>{}</p>'.format(bound_field.help_text)
        else:
            fld_help = ''
        rtn = template.format(id=fld_id, group_extra=group_extra,
                              label=fld_label, field=field, errors=fld_errors, help=fld_help)
        return rtn

    # todo 1: custom widget for inline radio (choice radio select) and checkbox(multiple choice checkbox)

    # noinspection PyPep8Naming
    def b_CheckboxInput(self, form, bound_field, field_name):
        template = '<div class="checkbox {group_extra}">\n' \
                   '    {field} {label}\n' \
                   '    {errors}\n' \
                   '    {help}' \
                   '</div>\n'
        return self.b_base(form, bound_field, field_name, form_control=None, template=template)

    # noinspection PyPep8Naming
    def b_TextInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_NumberInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_EmailInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_URLInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_PasswordInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_HiddenInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_DateInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_DateTimeInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_TimeInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_Textarea(self, form, bound_field, field_name):
        # todo 2: add way to specify textarea rows
        return self.b_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def b_Select(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_NullBooleanSelect(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_SelectMultiple(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_RadioSelect(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_CheckboxSelectMultiple(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_FileInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_ClearableFileInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_MultipleHiddenInput(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_SplitDateTimeWidget(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_SplitHiddenDateTimeWidget(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def b_SelectDateWidget(self, form, bound_field, field_name):
        return self.b_base(form, bound_field, field_name, form_control=None)

    def _as_bootstrap(self):
        rtn = ''
        form = self.form
        for name in form.fields:
            field = form[name]
            widget_name = 'b_' + form.fields[name].widget.__class__.__name__
            widget_method = getattr(self, widget_name)
            rtn += widget_method(form, field, name)
            log.debug('>>>> Bootstrap field {}:{}'.format(name, widget_name))
        template = '<!-- form -->\n' \
                   '<form role="form" method="{method}" action="{action_url}">\n' \
                   '    {csrf}\n' \
                   '    {form}\n' \
                   '    {button}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        rtn = template.format(method=self.method, action_url=self.action_url,
                              csrf=_csrf_(self.request), form=rtn,
                              button=self.button)
        return rtn

    def _as_bootstrap_inline(self, form, layout):
        # fixme: implement this
        rtn = ''
        return rtn

    #
    # Horizontal support ##############################################################################################
    #

    def h_base(self, form, bound_field, field_name, form_control='form-control', template=None):
        """ Output bootstrap field

        :param form: The form
        :param bound_field: A bound field
        :param field_name: The field's name
        :param form_control: Class to apply to the field's input html or None
        :type form_control: unicode or None
        :return:
        """
        if not template:
            template = '<div class="form-group {group_extra}">\n' \
                       '    {label}\n' \
                       '    {errors}\n' \
                       '    {field}\n' \
                       '    {help}' \
                       '</div>\n'
        fld_id = bound_field.id_for_label
        fld_label = add_classes(bound_field.label_tag(), 'control-label')
        field = str(bound_field)
        if form_control:
            field = add_classes(field, 'form-control')
        if bound_field.errors:
            fld_errors = '    <span style="color:#a94442;>{}</span>'.format(bound_field.errors)
            group_extra = 'has-error'
        else:
            fld_errors = ''
            if self.request.POST:
                group_extra = 'has-success'
            else:
                group_extra = ''
        if bound_field.help_text:
            fld_help = '    <p>{}</p>'.format(bound_field.help_text)
        else:
            fld_help = ''
        rtn = template.format(id=fld_id, group_extra=group_extra,
                              label=fld_label, field=field, errors=fld_errors, help=fld_help)
        return rtn

    # todo 1: custom widget for inline radio (choice radio select) and checkbox(multiple choice checkbox)

    # noinspection PyPep8Naming
    def h_CheckboxInput(self, form, bound_field, field_name):
        template = '<div class="checkbox {group_extra}">\n' \
                   '    {field} {label}\n' \
                   '    {errors}\n' \
                   '    {help}' \
                   '</div>\n'
        return self.h_base(form, bound_field, field_name, form_control=None, template=template)

    # noinspection PyPep8Naming
    def h_TextInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_NumberInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_EmailInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_URLInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_PasswordInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_HiddenInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_DateInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_DateTimeInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_TimeInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_Textarea(self, form, bound_field, field_name):
        # todo 2: add way to specify textarea rows
        return self.h_base(form, bound_field, field_name)

    # noinspection PyPep8Naming
    def h_Select(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_NullBooleanSelect(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_SelectMultiple(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_RadioSelect(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_CheckboxSelectMultiple(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_FileInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_ClearableFileInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_MultipleHiddenInput(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_SplitDateTimeWidget(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_SplitHiddenDateTimeWidget(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    # noinspection PyPep8Naming
    def h_SelectDateWidget(self, form, bound_field, field_name):
        return self.h_base(form, bound_field, field_name, form_control=None)

    def _as_bootstrap_horizontal(self):
        # fixme: implement this
        rtn = ''
        form = self.form
        for name in form.fields:
            field = form[name]
            widget_name = 'h_' + form.fields[name].widget.__class__.__name__
            widget_method = getattr(self, widget_name)
            rtn += widget_method(form, field, name)
            log.debug('>>>> Bootstrap field {}:{}'.format(name, widget_name))
        template = '<!-- form -->\n' \
                   '<form class="form-horizontal" role="form" method="{method}" action="{action_url}">\n' \
                   '    {csrf}\n' \
                   '    {form}\n' \
                   '    {button}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        rtn = template.format(method=self.method, action_url=self.action_url,
                              csrf=_csrf_(self.request), form=rtn,
                              button=self.button)
        return rtn

    #
    # Bootstrap layout support ########################################################################################
    #

    def _as_bootstrap_layout(self, form, layout):
        layout = self._get_layout()
        # fixme: implement this
        rtn = ''
        return rtn

    def _get_layout(self):
        layout = getattr(self.form, 'layout', None)
        if not layout:
            layout = tuple()
            for name in self.form.fields:
                layout += (FF(name),)
        return layout

    # def __getattr__(self, item, *default):
    #     try:
    #         return self[item]
    #     except KeyError:
    #         if len(default) > 0:
    #             return default[0]
    #         raise AttributeError


class FF(DWidget):
    """

    """
    def __init__(self, field):
        self.form = None
        self.form_type = None
        super(FF, self).__init__(field)

    def generate(self):
        field_name = self.args[0]
        form_type = self.form_type
        form = self.form
        bound_field = form[field_name]
        field_field = form.fields[field_name]
        field_type = field_field.widget.input_type
        log.debug('>>>> Generate for field {} {} {} {}'.format(field_name, form_type, field_type, str(bound_field)))
        return str(bound_field)


class DForm(DWidget):
    """ Django form widget

    .. sourcecode:: python

        DForm(request_obj, django_form, submit_text, action_url)

    :param request: request object
    :type request: WSGIRequest
    :param form: form object
    :type form: forms.Form
    :param button: text for submit button or FormButton object.  Default to Submit.
    :type button: str or unicode or DFormButton.
    :param action_url: submit action url.  Default to request.path (ie. Post to issuing view).
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

        FormButton('Text of button')

    :param text: Button text.
    :type text: str or unicode
    :param button: Button type per bootstrap.  Default 'btn-default',
    :type button: str or unicode
    :param size: Button size per bootstrap.  Default ''
    :type size: str or unicode
    :param classes: Classes to add to output
    :type classes: str or unicode
    :param style: Styles to add to output
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


class B0Form(DWidget):
    """ Bootstrap form """
    def __init__(self, request, form, button='Submit', action_url=None, method='Post'):
        if not isinstance(button, FormButton):
            button = FormButton(button)
        super(B0Form, self).__init__(request, form, button, action_url, method)

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


class BForm(DWidget):
    """ Bootstrap form

    .. sourcecode:: python

        BForm(request, form)
        BForm(request, form, form_type='horizontal')
        BForm(request, FLD(form.field1, ...), FLD(form.field2, ...), form_type='horizontal')

    | Shortcuts:

    :param request: The request
    :type request: WSGIRequest
    :param form: The form. May be a form or a tuple of DWidgets including form fields.
    :type form: form.Form or Form or tuple
    :param kwargs: **The following kwargs are available**
    :param button: text for submit button or FormButton object.  Default to Submit.
    :type button: str or unicode or DFormButton.
    :param action_url: submit action url.  Default to request.path (ie. Post to issuing view).
    :type action_url: str or unicode
    :param method: Submit method.  Default 'Post'.
    :type method: str or unicode
    :param form_type: Form type.  Default ''.
    :type form_type: str or unicode

    The following form types are available:
        * '' - basic bootstrap form.
        * horizontal - bootstrap horizontal form.
        * inline - bootstrap inline form

    """
    # def __init__(self, request, form, button='Submit', action_url=None, method='Post'):
    def __init__(self, request, *form, **kwargs):
        button = kwargs.pop('button', 'Submit')
        if not isinstance(button, FormButton):
            button = FormButton(button)
        action_url = kwargs.pop('action_url', None)
        method = kwargs.pop('method', 'Post')
        form_type = ssw(kwargs.pop('form_type', ''), 'form-')
        for f in form:
            if isinstance(f, (BFG, BCB)):
                f.form_type = form_type
        super(BForm, self).__init__(request, form, button, action_url, method, form_type)

    def generate(self):
        request, form, button, action_url, method, form_type = self.args
        template = '<!-- form -->\n' \
                   '<form role="form" class="{form_type}" method="{method}" action="{action_url}">\n' \
                   '    {csrf}\n' \
                   '    {form}\n' \
                   '    {button}\n' \
                   '</form>\n' \
                   '<!-- /form -->\n'
        if not action_url:
            action_url = request.path
        if isinstance(form, tuple):
            form = '\n'.join(form)
        rtn = template.format(form_type=form_type, method=method, action_url=action_url,
                              csrf=_csrf_(request), form=form,
                              button=button)
        return rtn



# fixme: form-group can have classes has-success, has-warning, has-error, has-feedback,
# fixme: form-group can take a span <span class="glyphicon glyphicon-ok form-control-feedback"></span>, etc.
# fixme: support help text <span class="help-block">A block of help text that breaks onto a new line and may extend beyond one line.</span>
# fixme: ass support for input groups http://getbootstrap.com/components/#input-groups


class BFG(DWidget):
    """ Bootstrap form group field """
    def __init__(self, fld, lbl_width=None, fld_width=None):
        super(BFG, self).__init__(fld, lbl_width, fld_width)

    def generate(self):
        fld, lbl_width, fld_width = self.args
        # noinspection PyUnresolvedReferences
        if self.form_type == '':
            template = '<div class="form-group">\n' \
                       '    {label}\n' \
                       '    {field}\n' \
                       '{fld_help}' \
                       '</div>\n'
            label = fld.label_tag()
            if lbl_width:
                label = add_classes(label, 'col-md-{}'.format(lbl_width))
            field = add_classes(str(fld), 'form-control')
            if fld_width:
                field = '<div class="col-md-{}" >{}</div>'.format(fld_width, field)
            if fld.help_text:
                fld_help = '    <p>{}</p>'.format(fld.help_text)
            else:
                fld_help = ''
            rtn = template.format(label=label, field=field, fld_help=fld_help)
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


# todo 1: add id to Form
