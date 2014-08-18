#!/usr/bin/env python
# coding=utf-8

"""
Bootstrap 3 Widgets
===================

.. module:: dpage_bootstrap3
   :synopsis: Provides DjangoPage widgets to create various bootstrap 3 elements

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create various bootstrap 3 elements.

8/4/14 - Initial creation

**Widgets**
"""

from __future__ import unicode_literals
# noinspection PyUnresolvedReferences
import logging

log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '8/4/14'
__copyright__ = "Copyright 2014, Richard Bell"
__credits__ = ['rbell01824']
__license__ = 'All rights reserved'
__version__ = '0.1'
__maintainer__ = 'rbell01824'
__email__ = 'rbell01824@gmail.com'

import functools

# noinspection PyProtectedMember
from djangopages.dpage import DWidget, unique_name

########################################################################################################################
#
# Various Bootstrap 3 widgets.
#
#
#
# todo: add remaining bootstrap 3 widgets
# todo: heading small support
# todo: add lead body copy support
# todo: add small, bold, italics
# todo: add alignment, abbreviations, initialism, addresses, blockquote, etc
# todo: add ordered and unordered lists
# todo: gr through bootstrap CSS and add full support
#
########################################################################################################################


class Accordion(DWidget):
    """
    .. sourcecode:: python

        Accordion('heading 1', 'content 1',
                  'heading 2', 'content 2',
                  ...)

    :param heading: accordion panel heading
    :type heading: basestring or DWidget
    :param content: accordion panel content
    :type content: basestring or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template_top = '<!-- Accordion start -->' \
                   '  <div class="panel-group" id="{accordion_id}">\n' \
                   '    {panels}\n' \
                   '  </div>\n' \
                   '<!--Accordion end -->'
    template = '<!-- Accordion panel start -->\n' \
               '  <div class="panel panel-default">\n' \
               '    <div class="panel-heading">\n' \
               '      <h4 class="panel-title">\n' \
               '        <a data-toggle="collapse" data-parent="#{accordion_id}" href="#{panel_id}">\n' \
               '          {heading}\n' \
               '        </a>\n' \
               '      </h4>\n' \
               '    </div>\n' \
               '    <div id="{panel_id}" class="panel-collapse collapse">\n' \
               '      <div class="panel-body">\n' \
               '        {content}\n' \
               '      </div>\n' \
               '    </div>\n' \
               '  </div>\n' \
               '<!-- Accordion panel end -->'

    def __init__(self, *content, **kwargs):
        super(Accordion, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        accordion_id = unique_name('aid')
        panels = ''
        for hd, con in zip(content[::2], content[1::2]):
            panel_id = unique_name('pid')
            panels += template.format(accordion_id=accordion_id,
                                      panel_id=panel_id,
                                      heading=hd,
                                      content=con)
        out = self.template_top.format(accordion_id=accordion_id,
                                       panels=panels)
        return out


class AccordionM(DWidget):
    """
    .. sourcecode:: python

        AccordionM('heading 1', 'content 1',
                   'heading 2', 'content 2',
                   ...)

    :param heading: accordion panel heading
    :type heading: basestring or DWidget
    :param content: accordion panel content
    :type content: basestring or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict

    .. note:: see http://jsfiddle.net/KyleMit/Wc4xt/

    """
    template_top = '<!-- Accordion start -->' \
                   '  <div class="panel-group" id="{accordion_id}">\n' \
                   '    {panels}\n' \
                   '  </div>\n' \
                   '<!--Accordion end -->'
    template = '<!-- Accordion panel start -->\n' \
               '  <div class="panel panel-default">\n' \
               '    <div class="panel-heading">\n' \
               '      <h4 class="panel-title">\n' \
               '        <a data-toggle="collapse" data-target="#{panel_id}" href="#{panel_id}">\n' \
               '          {heading}\n' \
               '        </a>\n' \
               '      </h4>\n' \
               '    </div>\n' \
               '    <div id="{panel_id}" class="panel-collapse collapse">\n' \
               '      <div class="panel-body">\n' \
               '        {content}\n' \
               '      </div>\n' \
               '    </div>\n' \
               '  </div>\n' \
               '<!-- Accordion panel end -->'

# .panel-heading a:after {
#     font-family: 'Glyphicons Halflings';
#     content: "\e114";
#     float: right;
#     color: grey;
# }
# .panel-heading a.collapsed:after {
#     content: "\e080";
# }

    def __init__(self, *content, **kwargs):
        super(AccordionM, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        accordion_id = unique_name('aid')
        panels = ''
        for hd, con in zip(content[::2], content[1::2]):
            panel_id = unique_name('pid')
            panels += template.format(panel_id=panel_id,
                                      heading=hd,
                                      content=con)
        out = self.template_top.format(accordion_id=accordion_id,
                                       panels=panels)
        return out


class Button(DWidget):
    """
    .. sourcecode:: python

        Button('Button 1', button='btn-success btn-sm')

    | Synonym: BTN(...), useful abbreviation

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict

    additional kwargs

    :param disabled: default False, if true button is disabled
    :type width: bool
    :param button: default 'btn-default', button definition per bootstrap 3
    :type type: str
    """
    template = '<!-- start of button -->\n' \
               '    <button type="button" {classes} {disabled} {style}>\n' \
               '        {content}\n' \
               '    </button>\n' \
               '<!-- end of button -->\n'

    def __init__(self, *content, **kwargs):
        super(Button, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        disabled = kwargs.get('disabled', '')
        button = kwargs.get('button', 'btn-default')
        # make sure have a button type specified
        for t in ('btn-default', 'btn-primary', 'btn-success', 'btn-info', 'btn-warning', 'btn-danger', 'btn-link'):
            if t in button:
                break
        else:
            button += ' btn-default'
        classes = self.add_classes(classes, 'btn {button}'.format(button=button))
        out = ''
        for c in content:
            out += template.format(content=c, classes=classes, style=style, disabled=disabled)
        return out
BTN = functools.partial(Button)


class Glyphicon(DWidget):
    """
    .. sourcecode:: python

        Glyphicon('star')

    | Synonym: GL(...), useful abbreviation

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template = '<span {classes} {style}></span>'

    def __init__(self, *content, **kwargs):
        super(Glyphicon, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        out = ''
        for c in content:
            gl_cls = self.add_classes(classes, 'glyphicon glyphicon-{}'.format(c))
            out += template.format(classes=gl_cls, style=style)
        return out
GL = functools.partial(Glyphicon)


class Jumbotron(DWidget):
    """
    .. sourcecode:: python

        Jumbotro('Jumbotron content')

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template = '<!-- jumbotron start -->' \
               '<div class="jumbotron">\n' \
               '{content}\n' \
               '</div>\n' \
               '<!-- jumbotron end -->'

    def __init__(self, *content, **kwargs):
        super(Jumbotron, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        out = ''
        for con in content:
            out += template.format(classes=classes, style=style, content=con)
        return out


class Label(DWidget):
    """
    .. sourcecode:: python

        Label('default', 'text of default label',
              'primary', 'text of primary label')

    :param content: content, label_type, label_text, ...
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template = '<span {classes} {style}>{content}</span>'

    def __init__(self, *content, **kwargs):
        super(Label, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        out = ''
        for typ, con in zip(content[::2], content[1::2]):
            cls = self.add_classes(classes, 'label label-{}'.format(typ))
            out += template.format(classes=cls, style=style, content=con)
        return out


class Link(DWidget):
    """
    .. sourcecode:: python

        Link('/dpages/somepage', 'link to somepage',
             '/dpages/anotherpage', 'link to anotherpage')

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict

    additional kwargs

    :param button: default 'btn-default', button type for the link
    :type button: str
    :param disabled: default False, if true button is disabled
    :type disabled: bool
    """

    template = '<a href="{href}" {classes} {style} {disabled} {role}>{content}</a>'

    def __init__(self, *content, **kwargs):
        super(Link, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        disabled = kwargs.get('disabled', '')
        button = kwargs.get('button', 'btn-default')
        role = ''
        if button:
            # make sure have a button type specified
            for t in ('btn-default', 'btn-primary', 'btn-success', 'btn-info', 'btn-warning', 'btn-danger', 'btn-link'):
                if t in button:
                    break
            else:
                button += ' btn-default'
            classes = self.add_classes(classes, 'btn {button}'.format(button=button))
            role = 'role="button"'
        out = ''
        for hr, con in zip(content[::2], content[1::2]):
            out += template.format(href=hr, classes=classes, style=style, disabled=disabled, role=role,
                                   content=con)
        return out


class Panel(DWidget):
    """
    .. sourcecode:: python

        Panel( 'heading', 'content',
               'heading2', 'content2', ... )

    :param content: content
    :type content: basestring or tuple or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template = """
    <div class="panel panel-default">
        <div class="panel-body">
            {content}
        </div>
    </div>
    """

    heading_template = """
    <div class="panel panel-default">
        <div class="panel-heading">{heading}</div>
        <div class="panel-body">
            {content}
        </div>
    </div>
    """

    def __init__(self, *content, **kwargs):
        super(Panel, self).__init__(content, kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        out = ''
        for hd, con in zip(content[::2], content[1::2]):
            if hd and template == Panel.template:
                tpl = Panel.heading_template
            else:
                tpl = template
            out += tpl.format(content=con, heading=hd, classes=classes, style=style)
        return out


class Modal(DWidget):
    """
    .. sourcecode:: python

        Modal( heading='', body='', footer='', button='Show', modal_size='', button_type='btn-primary', **kwargs):

    :param heading: heading for modal panel
    :type heading: basestring or DWidget
    :param body: body for modal panel
    :type body: basestring or DWidget
    :param footer: footer modal panel
    :type footer: basestring or DWidget
    :param button: text for modal button
    :type button: basestring or DWidget
    :param modal_size: modal size per bootstrap 3
    :type modal_size: basestring or DWidget
    :param button_type: button type
    :type button_type: basestring or DWidget
    :param kwargs: standard kwargs
    :type kwargs: dict
    """
    template = """
<!-- Button trigger modal -->
<button class="btn {button_type}" data-toggle="modal" data-target="#{modal_id}">
  {button}
</button>
<!-- / Button trigger modal -->

<!-- .modal -->
<div class="modal fade " id={modal_id} tabindex="-1" role="dialog" aria-labelledby="{modal_label}" aria-hidden="true">
  <!-- .modal-dialog -->
  <div class="modal-dialog {modal_size}">
    <!-- .modal-content -->
    <div class="modal-content">
      <!-- .modal-header -->
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">
          <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
        </button>
        <h4 class="modal-title" id={modal_label}>{heading}</h4>
      </div>
      <!-- /.modal-header -->
      <!-- .modal-body -->
      <div class="modal-body">
        {body}
      </div>
      <!-- /.modal-body -->
      <!-- .modal-footer -->
      <div class="modal-footer">
        {footer}
      </div>
      <!-- /.modal-footer -->
    </div>
    <!-- /.modal-content -->
  </div>
  <!-- /.modal-dialog -->
</div>
<!-- /.modal -->
    """

    def __init__(self, heading='', body='', footer='',
                 button='Show', modal_size='', button_type='btn-primary', **kwargs):
        super(Modal, self).__init__((heading, body, footer, button, modal_size, button_type), kwargs)
        return

    def generate(self, template, content, classes, style, kwargs):
        assert isinstance(content, tuple)
        heading, body, footer, button, modal_size, button_type = content[0:7]
        modal_id = unique_name('id_m_')
        modal_label = unique_name('lbl_m_')
        out = template.format(heading=heading, body=body, footer=footer,
                              modal_id=modal_id, modal_label=modal_label,
                              modal_size=modal_size,
                              button=button, button_type=button_type)
        return out

################################################################################
################################################################################

# fixme: finish table  do this: http://www.pontikis.net/labs/bs_grid/demo/


# class Table(object):
#     """
#     Table support
#
#     table-responsive
#     table-condensed
#     table-hover
#     table-bordered
#     table-striped
#     """
#     def __init__(self, heading, *content, **kwargs):
#         self.heading = heading
#         self.content = content
#         self.tresponsive = kwargs.pop('tbl_class', None)
#         self.kwargs = kwargs
#         pass
#
#     def render(self):
#         out = ''
#         # Build table class
#         # cls = 'table'
#
#         return out
#
#
# class TableRow(object):
#     """
#     Table row support
#
#       <tr>
#          <td>January</td>
#          <td>$100</td>
#       </tr>
#     """
#     def __init__(self, *content, **kwargs):
#         self.content = content
#         self.tr_class = kwargs.pop('tr_class', None)
#         self.kwargs = kwargs
#         pass
#
#     def render(self):
#         out = ''
#         for con in self.content:
#             if isinstance(con, TableCell):
#                 out += _render(con)
#             else:
#                 out += '<td>' + _render(con) + '</td>'
#         tr_start = '<tr>'
#         if self.tr_class:
#             tr_start = '<tr class="{tr_class}" >'.format(self.tr_class)
#         out = tr_start + out + '</tr>'
#         return out
#
#
# # noinspection PyPep8Naming
# def TR(*content, **kwargs):
#     tr = TableRow(content, kwargs)
#     return tr
#
#
# class TableCell(object):
#     """
#     Table cell support
#     """
#     def __init__(self, *content, **kwargs):
#         """
#         Initialize a td table element
#
#         :param content: content
#         :type content: object or list
#         :param kwargs: RFU
#         :type: dict
#         """
#         self.content = content
#         self.td_class = kwargs.pop('td_class', None)
#         self.kwargs = kwargs
#         pass
#
#     def render(self):
#         td_start = '<td>'
#         if self.td_class:
#             td_start = '<td class="{td_class}" >'.format(td_class=self.td_class)
#         out = ''
#         for con in self.content:
#             out += td_start + _render(con) + '</td>\n'
#         return out
#
#
# # noinspection PyPep8Naming
# def TD(*content, **kwargs):
#     td = TableCell(content, kwargs)
#     return td
#
#
# class TableHead(object):
#     """
#     Table head support
#
#      <thead>
#       <tr>
#          <th>Month</th>
#          <th>Savings</th>
#       </tr>
#      </thead>
#
#     """
#     def __init__(self, *content, **kwargs):
#         """
#         """
#         pass
#
#     def render(self):
#         out = ''
#         return out
#
#
# class TableFoot(object):
#     """
#     Table foot support
#
#      <tfoot>
#       <tr>
#          <td>Sum</td>
#          <td>$180</td>
#       </tr>
#      </tfoot>
#
#     """
#     def __init__(self, *content, **kwargs):
#         """
#         """
#         pass
#
#     def render(self):
#         # todo 1: finish this
#         out = ''
#         return out
#
#
# class Table2(object):
#     """
#     Provide django-tables2 support
#     """
#     def __init__(self, dpage, qs, **kwargs):
#         """
#         Initialize a Table object
#
#         :param dpage: dpage object
#         :type dpage: DPage
#         :param qs: Queryset
#         :type qs:
#         :param kwargs: RFU
#         :type kwargs: dict
#         """
#         self.dpage = dpage
#         self.qs = qs
#         self.kwargs = kwargs
#         # todo 2: add other kwargs options here
#         pass
#
#     # noinspection PyUnusedLocal
#     def render(self, **kwargs):
#         """
#         Generate html for table
#         """
#         template = '<!-- start of table -->\n' \
#                    '    {% load django_tables2 %}\n' \
#                    '    {% render_table insert_the_table %}\n' \
#                    '<!-- end of table -->\n'
#         t = Template(template)
#         c = {'insert_the_table': self.qs, 'request': self.dpage.request}
#         output = t.render(Context(c))
#         return output
#         # output = ''
#         # name = unique_name('table')
#         # self.dpage.context[name] = self.qs
#         # template = '<!-- start of table -->\n' \
#         #            '    {% render_table x_the_table_object %}\n' \
#         #            '<!-- end of table -->\n'
#         # output = template.replace('x_the_table_object', name)
#         # return output
#
# # todo 1: add support for table sorter: http://mottie.github.io/tablesorter/docs/index.html
# # http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# # looks good: http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# # https://github.com/Mottie/tablesorter/wiki
#
#
# class Form(object):
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
#         #
#         #  Alternate form template
#         #
#         # <form method="post" class="bootstrap3" action="/graphpages/graphpage/{{ graph_pk }}"> {% csrf_token %}
#         #     {# Include the hidden fields #}
#         #     {% for hidden in graphform.hidden_fields %}
#         #         {{ hidden }}
#         #     {% endfor %}
#         #     {# Include the visible fields #}
#         #     {% for field in graphform.visible_fields %}
#         #         {% if field.errors %}
#         #             <div class="row bg-danger">
#         #                 <div class="col-md-3 text-right"></div>
#         #                 <div class="col-md-7">{{ field.errors }}</div>
#         #             </div>
#         #         {% endif %}
#         #         <div class="row">
#         #             <div class="col-md-3 text-right">{{ field.label_tag }}</div>
#         #             <div class="col-md-7">{{ field }}</div>
#         #         </div>
#         #     {% endfor %}
#         #     <div class="row">
#         #         <div class='col-md-3 text-right'>
#         #             <input type="submit" value="Display graph" class="btn btn-primary"/>
#         #         </div>
#         #     </div>
#         # </form>
#         #
#         # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),
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
# # todo 1: add support for normal bootstrap 3 forms
# # todo 1: add id to Form
#
########################################################################################################################
#
# Carousel
#
########################################################################################################################
#
#
# class Carousel(object):
#     """
#     Carousel
#     """
#     def __init__(self, *content, **kwargs):
#         self.content = content
#         self.id = kwargs.pop('id', unique_name('carousel_id'))
#         self.data_interval = kwargs.pop('data-interval', 'false')
#         self.indicators = kwargs.pop('indicators', None)
#         self.background_color = kwargs.pop('background-color', '#D8D8D8')
#         return
#
#     def render(self):
#         # t_ind = '<!-- Start Bottom Carousel Indicators -->\n' \
#         #         '<ol class="carousel-indicators">\n' \
#         #         '    <li data-target="#{carousel_id}" data-slide-to="0" class="active"></li>\n' \
#         #         '    <li data-target="#{carousel_id}" data-slide-to="1"></li>\n' \
#         #         '    <li data-target="#{carousel_id}" data-slide-to="2"></li>\n' \
#         #         '</ol>\n<!-- End Bottom Carousel Indicators -->\n'
#         out = """
#                   <div class="carousel slide" data-ride="carousel" id="{carousel_id}" data-interval="{data_interval}">
#
#                     <!-- Carousel Slides / Quotes -->
#                     <div class="carousel-inner" style="background-color: {background_color};">
#
#                       <!-- Quote 1 -->
#                       <div class="item active">
#                           <div class="row">
#                             <div class="col-sm-9">
#                               <p>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <small>Someone famous</small>
#                               <p>1 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>2 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>3 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>4 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>5 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>6 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                               <p>7 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
#                                  adipisci velit!</p>
#                             </div>
#                           </div>
#                       </div>
#                       <!-- Quote 2 -->
#                       <div class="item">
#                           <div class="row">
#                             <div class="col-sm-9">
#                               <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam auctor nec lacus ut
#                                  tempor. Mauris.</p>
#                             </div>
#                           </div>
#                       </div>
#                       <!-- Quote 3 -->
#                       <div class="item">
#                           <div class="row">
#                             <div class="col-sm-9">
#                               <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut rutrum elit in arcu
#                                  blandit, eget pretium nisl accumsan. Sed ultricies commodo tortor, eu pretium
#                                  mauris.</p>
#                             </div>
#                           </div>
#                       </div>
#                     </div>
#
#                     <!-- Carousel Buttons Next/Prev -->
#                     <a data-slide="prev" href="#{carousel_id}" class="left carousel-control">
#                         <i class="fa fa-chevron-left"></i>
#                     </a>
#                     <a data-slide="next" href="#{carousel_id}" class="right carousel-control">
#                         <i class="fa fa-chevron-right"></i>
#                     </a>
#
#
#                   </div>
#             """
#         # todo 1: finish this
#         t_jsf = """
#                     <!-- Controls buttons -->
#                     <div style="text-align:center;">
#                       <input type="button" class="btn start-slide" value="Start">
#                       <input type="button" class="btn pause-slide" value="Pause">
#                       <input type="button" class="btn prev-slide" value="Previous Slide">
#                       <input type="button" class="btn next-slide" value="Next Slide">
#                       <input type="button" class="btn slide-one" value="Slide 1">
#                       <input type="button" class="btn slide-two" value="Slide 2">
#                       <input type="button" class="btn slide-three" value="Slide 3">
#                     </div>
#                   <script>
#                      $(function(){
#                         // Initializes the carousel
#                         $(".start-slide").click(function(){
#                            $("#{carousel_id}").carousel('cycle');
#                         });
#                         // Stops the carousel
#                         $(".pause-slide").click(function(){
#                            $("#{carousel_id}").carousel('pause');
#                         });
#                         // Cycles to the previous item
#                         $(".prev-slide").click(function(){
#                            $("#{carousel_id}").carousel('prev');
#                         });
#                         // Cycles to the next item
#                         $(".next-slide").click(function(){
#                            $("#{carousel_id}").carousel('next');
#                         });
#                         // Cycles the carousel to a particular frame
#                         $(".slide-one").click(function(){
#                            $("#{carousel_id}").carousel(0);
#                         });
#                         $(".slide-two").click(function(){
#                            $("#{carousel_id}").carousel(1);
#                         });
#                         $(".slide-three").click(function(){
#                            $("#{carousel_id}").carousel(2);
#                         });
#                      });
#                   </script>
#                 """
#         out = out.format(carousel_id=self.id,
#                          data_interval=self.data_interval,
#                          background_color=self.background_color)
#         # out += t_jsf.replace('{carousel_id}', self.id)
#         return out
