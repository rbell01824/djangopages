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


class Form(DWidget):
    """ Django form widget

    .. sourcecode:: python

        Small('some text')

    :param request: request object
    :type request: WSGIRequest
    :param form: form object
    :type form: forms.Form
    :param button: text for submit button or FormButton object.  If None, no submit button.
    :type button: str or unicode or FormButton.
    :param action_url: submit action url
    :type action_url: str or unicode
    :param template: override default widget template
    :type template: str or unicode
    """
    def __init__(self, request, form, button='Submit', action_url=None, method='Post', template=None):
        super(Form, self).__init__(request, form, button, action_url, method, template)
        return

    # noinspection PyMethodOverriding
    def generate(self):
        """ Django form html """
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),

        request, form, button, action_url, method, template = self.args
        if not template:
            template = '<!-- form -->\n' \
                       '<form role="form" method="{{ method }}" class="form" action="{{ action_url }}">\n' \
                       '     <!-- csrf -->{% csrf_token %}<!-- / csrf -->\n' \
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
                       '        </div>\n' \
                       '    {% endfor %}\n' \
                       '     <div class="row">\n' \
                       '         <div class="col-md-3 text-right">\n' \
                       '             <input type="submit" value="{{ button }}" class="btn btn-primary"/>\n' \
                       '         </div>\n' \
                       '     </div>\n' \
                       '</form>\n' \
                       '<!-- /form -->\n'
        # if not isinstance(button, FormButton):
        #     button = FormButton(button)
        t = Template(template)
        c = {'form': form, 'method': method, 'action_url': action_url, 'button': button}
        c.update(csrf(request))
        rtn = t.render(Context(c))
        return rtn

# todo 2: create djpages.format method that deals sensibly with errors
#         try:
#             rtn = template.format(form=form, method=method, action_url=action_url, button=button )
#         except:
#             rtn = None
#             exception = sys.exc_info()[0]
#             error_args = sys.exc_info()[1]
#             print exception, error_args
#             pass


class FormButton(DWidgetT):
    """ Form button definition

    .. sourcecode:: python

        FormButton('Text of button')

    :param text: text
    :type text: str or unicode or tuple
    :param button: default 'btn-default', button type per bootstrap
    :type button: str or unicode
    :param size: default '', button size per bootstrap
    :type size: str or unicode
    :param disabled: default False, if true button is disabled
    :type disabled: bool
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    """
    def __init__(self, text='Submit', button='btn-default', size='',
                 disabled=False, classes='', style=''):
        template = '<div class="row">' \
                   '    <div class="col-md-3 text-right">\n' \
                   '        <button type="submit" class="btn {button} {size} {classes}" style="{style}" {disabled}>\n' \
                   '            {text}\n' \
                   '        </button>\n' \
                   '    </div>\n' \
                   '</div>\n'
        button = ssw(button, 'btn-')
        size = ssw(size, 'btn-')
        disabled = 'disabled="disabled"' if disabled else ''
        modal_id = None
        super(FormButton, self).__init__(template, {'modal_id': modal_id, 'text': text,
                                                    'button': button, 'size': size, 'disabled': disabled,
                                                    'classes': classes, 'style': style})


# class Form(DWidget):
#     """
#     Provide form support
#     """
#     def __init__(self, dpage, form, submit='Submit', initial=None, action_url=None, **kwargs):
#         """
#         Create a form object.
#
#         :param dpage: dpage object
#         :type dpage: DPage
#         :param form: form object
#         :type form: forms.Form
#         :param submit: text for submit button.  If None, no submit button.
#         :type submit: unicode
#         :param initial: initial bound values
#         :type initial: dict or None
#         :param action_url: submit action url
#         :type action_url: unicode
#         :param kwargs: RFU
#         :type kwargs: dict
#         """
#         self.dpage = dpage
#         self.form = form
#         self.submit = submit
#         self.initial = initial
#         self.action_url = action_url
#         self.kwargs = kwargs
#         # todo 2: add other kwargs options here
#         pass
#
#     # noinspection PyUnusedLocal
#     def render(self, **kwargs):
#         """
#         Create and render the form
#         """
#         if self.initial:
#             the_form = self.form(self.initial)
#         elif len(self.dpage.request.POST) > 0:
#             the_form = self.form(self.dpage.request.POST)
#         else:
#             the_form = self.form()
#         request = self.dpage.request
#         form_class_name = self.form.__name__
#         template_top = '{% load bootstrap3 %}\n' \
#                        '<!-- start of django bootstrap3 form -->\n' \
#                        '    <form role="form" action="{action_url}" method="post" class="form">\n' \
#                        '        <!-- csrf should be here -->{% csrf_token %}<!-- -->\n' \
#                        '        <!-- our form class name -->' \
#                        '            <input type="hidden" name="form_class_name" value="{form_class_name}" >\n' \
#                        '        {% bootstrap_form the_form %}\n'
#         template_button = '        {% buttons %}\n' \
#                           '            <button type="submit" class="btn btn-primary">\n' \
#                           '                {% bootstrap_icon "star" %} {submit_text}\n' \
#                           '            </button>\n' \
#                           '        {% endbuttons %}\n'
#         template_bottom = '    </form>\n' \
#                           '<!-- end of django bootstrap3 form -->\n'
#         template = template_top
#         if self.submit:
#             template += template_button
#         template += template_bottom
#
#         # Do NOT use format here since the template contains {% ... %}
#         template = template.replace('{action_url}', self.action_url if self.action_url else '/dpages/')
#         template = template.replace('{form_class_name}', form_class_name)
#         if self.submit:
#             template = template.replace('{submit_text}', self.submit)
#         t = Template(template)
#         c = {'the_form': the_form}
#         c.update(csrf(request))
#         output = t.render(Context(c))
#         return output
#         # return template
#
# # todo 1: add support for normal bootstrap forms
# # todo 1: add id to Form
#
