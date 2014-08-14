#!/usr/bin/env python
# coding=utf-8

""" Various bootstrap 3 widgets

Many of these widgets accept a list of arguments.  The default behavior is to apply the widget
to each member of the list.

Where desired it is possible to evaluate and concatenate the list using the X widget.

Final widget template handling is done in the widget's render method.  This is a concious design
choice that allows post instance definition of the template.

8/4/14 - Initial creation

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

from django.template import Template
from django.template import Context
from django.core.context_processors import csrf

from djangopages.dpage import DWidget, _render, unique_name

########################################################################################################################
#
# Various Bootstrap 3 widgets.
#
#
#
# todo: add heading small support
# todo: add lead body copy support
# todo: add small, bold, italics
# todo: add alignment, abbreviations, initialism, addresses, blockquote, etc
# todo: add ordered and unordered lists
# todo: gr through bootstrap CSS and add full support
#
########################################################################################################################


class Button(DWidget):
    """
    DPage button class
    """
    template = '<!-- start of button -->\n' \
               '    <button type="button" {classes} {disabled} {style}>\n' \
               '        {content}\n' \
               '    </button>\n' \
               '<!-- end of button -->\n'

    def __init__(self, content, btn_extras='', disabled=False, classes='', style='', template=None):
        """
        Create a button object.
        """
        super(Button, self).__init__(content, classes, style, template)
        self.btn_extras = btn_extras
        self.disabled = disabled
        return

    def render(self):
        disabled = 'disabled="disabled"' if self.disabled else ''
        extra = ' '.join(['btn', self.btn_extras])
        content, classes, style, template = self.render_setup(extra_classes=extra)
        out = template.format(content=content,
                              disabled=disabled,
                              style=style,
                              classes=classes)
        return out
BTN = functools.partial(Button)


class Glyphicon(DWidget):
    """
    Convenience method to output bootstrap 3 glyphicons
    """
    template = """
    <span {classes} {style}></span>
    """

    def __init__(self, content, classes='', style='', template=None):
        super(Glyphicon, self).__init__(content, classes, style, template)
        return

    def render(self):
        extra = 'glyphicon glyphicon-{}'.format(self.content)
        content, classes, style, template = self.render_setup(extra_classes=extra)
        out = template.format(style=style,
                              classes=classes)
        return out

GL = functools.partial(Glyphicon)


class Link(DWidget):
    """
    Link text support.  Link renders its content and wraps in a link.
    """
    template = '<a href="{href}" {classes} {style}>{content}</a>'

    def __init__(self, href, content, button='', classes='', style='', template=None):
        """
        Create a DPage Link object and initialize it.
        """
        super(Link, self).__init__(content, classes, style, template)
        self.href = href
        self.button = button

    def render(self):
        """
        Render link.
        """
        extra = ''
        if self.button:
            extra = 'btn {}'.format(self.button)
        content, classes, style, template = self.render_setup(extra_classes=extra)
        out = template.format(href=self.href,
                              classes=classes,
                              style=style,
                              content=content)
        return out


class Panel(DWidget):
    """ Bootstrap 3 panel
    | Panel(\*content, \*\*kwargs)

        :param content: content
        :type content: basestring or tuple or DWidget
        :param kwargs: standard kwargs
        :type kwargs: dict

    additional kwargs

        :param heading: Panel heading
        :type para: basestring or tuple or DWidget

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
        heading = kwargs.get('heading', None)
        if heading:
            heading = _render(heading)
        if heading and template == Panel.template:
            template = Panel.heading_template
        out = template.format(content=content, classes=classes, style=style, heading=heading)
        return out


################################################################################
################################################################################
#
# fixme: Put these in alpha order
#
################################################################################
################################################################################

# fixme: resume work here btn-block, diabled, active, active state support


class ButtonModal(Button):
    """
    Button to control modal object.  Modal must exist so that its id is available.
    """
    def __init__(self, button, modal, btn_type='btn-default', btn_size=None, **kwargs):
        """

        """
        self.modal = modal
        self.button = button
        btn_extra = 'data-toggle="modal" data-target="#{modal_id}" '.format(modal_id=modal.id)
        super(ButtonModal, self).__init__(btn_text, btn_type, btn_size, btn_extra=btn_extra, **kwargs)   #fixme rjb
        return

    def render(self):
        out = super(ButtonModal, self).render()
        out += self.modal.render()
        return out


class Modal(object):
    """
    Modal object
    """
    def __init__(self, *content, **kwargs):
        """
        Initialize a Modal.

        :param
        """
        self.content = content
        self.button = kwargs.pop('button', None)
        self.header = kwargs.pop('header', None)
        self.footer = kwargs.pop('footer', None)
        self.id = kwargs.pop('id', unique_name('modal'))                                # id's the modal proper
        self.modal_label = kwargs.pop('modal_label', unique_name('modal_label'))        # labels the modal header
        self.kwargs = kwargs
        return

    def render(self):
        t_btn = '<!-- modal button start -->\n' \
                '<button class="btn btn-primary" data-toggle="modal" data-target="#{id}">\n' \
                '    {btn_text}\n' \
                '</button>\n' \
                '<!-- modal button end -->'
        t_top = '<!-- modal start -->\n' \
                '<div class="modal fade" id="{id}" tabindex="-1" role="dialog" \n' \
                '     aria-labelledby="{modal_label}" aria-hidden="true">\n' \
                '    <div class="modal-dialog">\n' \
                '        <div class="modal-content">\n'
        t_hdr = '            <div class="modal-header">\n' \
                '                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">' \
                '                    &times;' \
                '                </button>\n' \
                '                {modal_header}\n' \
                '            </div>\n'
        t_bdy = '            <div class="modal-body">\n' \
                '                {body}\n' \
                '            </div>\n'
        t_ftr = '            <div class="modal-footer">\n' \
                '                {modal_footer}\n' \
                '           </div>\n'
        t_btm = '        </div>\n' \
                '    </div>\n' \
                '</div>\n' \
                '<!-- modal end -->\n'
        out = ''
        body = _render(self.content)
        if self.button:
            out += t_btn.format(id=self.id, btn_text=self.button)
        out += t_top.format(id=self.id, modal_label=self.modal_label)
        if self.header:
            hdr = _render(self.header)
            out += t_hdr.format(modal_label=self.modal_label, modal_header=hdr)
        out += t_bdy.format(body=body)
        if self.footer:
            ftr = _render(self.footer)
            out += t_ftr.format(modal_footer=ftr)
        out += t_btm
        return out


class ButtonPanel(Button):
    """
    Button to control panel object
    """
    def __init__(self, btn_text, panel, btn_type='btn-default', btn_size=None, **kwargs):
        """
        Create a button panel.

        :param btn_text: Text of the button
        :param panel: Panel to attach.  Must be declared before button.
        :param btn_type: Button type per Button.
        :param btn_size: Button size per Button
        :param kwargs: RFU
        """
        self.panel = panel
        btn_extra = 'data-toggle="collapse" data-target="#{panel_id}" '.format(panel_id=panel.id)
        super(ButtonPanel, self).__init__(btn_text, btn_type, btn_size, btn_extra=btn_extra, **kwargs)
        return

    def render(self):
        out = ''
        out += super(ButtonPanel, self).render()
        return out


class Panel_fixme(object):
    """
    Collapsible button panel
    """
    # todo 2: add panel heading and footer to buttonpanel
    def __init__(self, *content, **kwargs):
        """
        Create a collapsible panel.

        :param content: Content
        :type content: list
        :param kwargs: Keyword arguments. button=None
        :type kwargs: dict
        """
        self.content = content
        self.button = kwargs.pop('button', None)
        self.id = kwargs.pop('id', unique_name('panel'))
        self.kwargs = kwargs
        # todo 2: add header, footer, and panel class attributes here
        pass

    def render(self, **kwargs):
        """
        Render button collapsible panel.
        """
        t_btn = '<!-- panel button start -->\n' \
                '<button class="btn btn-primary" data-toggle="collapse" data-target="#{id}">\n' \
                '    {btn_text}\n' \
                '</button>\n' \
                '<!-- panel button end -->'
        t_bdy = '<!-- panel start -->\n' \
                '    <div id="{id}" class="collapse">\n' \
                '        {content}\n' \
                '    </div>\n' \
                '<!-- panel end -->\n'

        out = ''
        content = _render(self.content, **kwargs)

        if self.button:
            out += t_btn.format(id=self.id, btn_text=self.button)
        out += t_bdy.format(id=self.id, content=content)
        return out


class Accordion(object):
    """
    Accordion support
    """
    def __init__(self, *content, **kwargs):
        """
        Create accordion object.

        :param content: Accordion content.  Must AccordionPanel or list of AccordionRow.
        :type content: list or AccordionPanel
        :param kwargs: RFU
        :type kwargs: dict
        """
        # todo 2: check that content is AccordionPanel or list of AccordionPanel
        # todo 2: add other accordion options in kwargs
        self.content = content
        self.id = kwargs.pop('id', unique_name('accordion_id'))
        self.kwargs = kwargs
        return

    def render(self, **kwargs):
        """
        Render accordion.
        """
        template = '<!-- Start of accordion -->\n' \
                   '<div class="panel-group" id="{accordion_id}">\n' \
                   '    {content}\n' \
                   '</div>\n' \
                   '<!-- End of accordion -->\n'
        content = _render(self.content, accordion_id=self.id, **kwargs)
        return template.format(accordion_id=self.id, content=content)


class AccordionPanel(object):
    """
    Panel within an Accordion
    """
    def __init__(self, *content, **kwargs):
        """
        Define accordion panel.
        :param kwargs: title='', default=False
        :type kwargs: dict
        """
        self.content = content
        self.accordion_id = kwargs.pop('accordion_id', None)
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        self.id = kwargs.pop('id', unique_name('panel_id'))
        # todo 2: add other accordion panel options here
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        # Accordion panels can not get their accordion parent id until the parent
        # is created, possibly after the panel is created.  So we may need to fetch
        # the accordion_id here.
        if not self.accordion_id:
            kwargs.pop('accordion_id')

        template = '<!-- start of panel -->\n' \
                   '    <div class="panel panel-default">\n' \
                   '        <div class="panel-heading">\n' \
                   '            <h4 class="panel-title">\n' \
                   '                <a data-toggle="collapse" data-parent="#{accordion_id}" ' \
                   '                    href="#{panel_id}">\n' \
                   '                    {panel_title}\n' \
                   '                </a>\n' \
                   '            </h4>\n' \
                   '        </div>\n' \
                   '        <div id="{panel_id}" class="panel-collapse collapse {panel_collapsed}">\n' \
                   '            <div class="panel-body">\n' \
                   '                {panel_content}\n ' \
                   '            </div>\n' \
                   '        </div>\n' \
                   '    </div>\n' \
                   '<!-- end of panel -->\n'
        content = _render(self.content, **kwargs)
        out = template.format(accordion_id=self.accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=self.id,
                              panel_title=self.title,
                              panel_content=content)
        return out


class AccordionMultiPanel(object):
    """
    Panel within an Accordion
    """
    def __init__(self, *content, **kwargs):
        """
        Define accordion panel.
        :param kwargs: title='', default=False
        :type kwargs: dict
        """
        self.content = content
        self.accordion_id = kwargs.pop('accordion_id', None)
        self.title = kwargs.pop('title', '')
        self.panel_collapsed = kwargs.pop('collapsed', True)
        self.id = kwargs.pop('id', unique_name('panel_id'))
        # todo 2: add other options here
        return

    def render(self, **kwargs):
        """
        Render the accordion panel.
        :param kwargs: accordion_id=accordion_id, Accordion id
        :type: dict
        :return: Rendered HTML
        :rtype: html
        """
        # Accordion panels can not get their accordion parent id until the parent
        # is created, possibly after the panel is created.  So we may need to fetch
        # the accordion_id here.
        if not self.accordion_id:
            kwargs.pop('accordion_id')

        template = '<!-- start of panel -->\n' \
                   '    <div class="panel panel-default">\n' \
                   '        <div class="panel-heading">\n' \
                   '            <h4 class="panel-title">\n' \
                   '                <a data-toggle="collapse" data-target="#{panel_id}" ' \
                   '                    href="#{panel_id}">\n' \
                   '                    {panel_title}\n' \
                   '                </a>\n' \
                   '            </h4>\n' \
                   '        </div>\n' \
                   '        <div id="{panel_id}" class="panel-collapse collapse {panel_collapsed}">\n' \
                   '            <div class="panel-body">\n' \
                   '                {panel_content}\n ' \
                   '            </div>\n' \
                   '        </div>\n' \
                   '    </div>\n' \
                   '<!-- end of panel -->\n'
        content = _render(self.content, **kwargs)
        out = template.format(accordion_id=self.accordion_id,
                              panel_collapsed='' if self.panel_collapsed else 'in',
                              panel_id=self.id,
                              panel_title=self.title,
                              panel_content=content)
        return out


# fixme: finish table  do this: http://www.pontikis.net/labs/bs_grid/demo/
class Table(object):
    """
    Table support

    table-responsive
    table-condensed
    table-hover
    table-bordered
    table-striped
    """
    def __init__(self, heading, *content, **kwargs):
        self.heading = heading
        self.content = content
        self.tresponsive = kwargs.pop('tbl_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        out = ''
        # Build table class
        # cls = 'table'

        return out


class TableRow(object):
    """
    Table row support

      <tr>
         <td>January</td>
         <td>$100</td>
      </tr>
    """
    def __init__(self, *content, **kwargs):
        self.content = content
        self.tr_class = kwargs.pop('tr_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        out = ''
        for con in self.content:
            if isinstance(con, TableCell):
                out += _render(con)
            else:
                out += '<td>' + _render(con) + '</td>'
        tr_start = '<tr>'
        if self.tr_class:
            tr_start = '<tr class="{tr_class}" >'.format(self.tr_class)
        out = tr_start + out + '</tr>'
        return out


# noinspection PyPep8Naming
def TR(*content, **kwargs):
    tr = TableRow(content, kwargs)
    return tr


class TableCell(object):
    """
    Table cell support
    """
    def __init__(self, *content, **kwargs):
        """
        Initialize a td table element

        :param content: content
        :type content: object or list
        :param kwargs: RFU
        :type: dict
        """
        self.content = content
        self.td_class = kwargs.pop('td_class', None)
        self.kwargs = kwargs
        pass

    def render(self):
        td_start = '<td>'
        if self.td_class:
            td_start = '<td class="{td_class}" >'.format(td_class=self.td_class)
        out = ''
        for con in self.content:
            out += td_start + _render(con) + '</td>\n'
        return out


# noinspection PyPep8Naming
def TD(*content, **kwargs):
    td = TableCell(content, kwargs)
    return td


class TableHead(object):
    """
    Table head support

     <thead>
      <tr>
         <th>Month</th>
         <th>Savings</th>
      </tr>
     </thead>

    """
    def __init__(self, *content, **kwargs):
        """
        """
        pass

    def render(self):
        out = ''
        return out


class TableFoot(object):
    """
    Table foot support

     <tfoot>
      <tr>
         <td>Sum</td>
         <td>$180</td>
      </tr>
     </tfoot>

    """
    def __init__(self, *content, **kwargs):
        """
        """
        pass

    def render(self):
        # todo 1: finish this
        out = ''
        return out


class Table2(object):
    """
    Provide django-tables2 support
    """
    def __init__(self, dpage, qs, **kwargs):
        """
        Initialize a Table object

        :param dpage: dpage object
        :type dpage: DPage
        :param qs: Queryset
        :type qs:
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.dpage = dpage
        self.qs = qs
        self.kwargs = kwargs
        # todo 2: add other kwargs options here
        pass

    # noinspection PyUnusedLocal
    def render(self, **kwargs):
        """
        Generate html for table
        """
        template = '<!-- start of table -->\n' \
                   '    {% load django_tables2 %}\n' \
                   '    {% render_table insert_the_table %}\n' \
                   '<!-- end of table -->\n'
        t = Template(template)
        c = {'insert_the_table': self.qs, 'request': self.dpage.request}
        output = t.render(Context(c))
        return output
        # output = ''
        # name = unique_name('table')
        # self.dpage.context[name] = self.qs
        # template = '<!-- start of table -->\n' \
        #            '    {% render_table x_the_table_object %}\n' \
        #            '<!-- end of table -->\n'
        # output = template.replace('x_the_table_object', name)
        # return output

# todo 1: add support for table sorter: http://mottie.github.io/tablesorter/docs/index.html
# http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# looks good: http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# https://github.com/Mottie/tablesorter/wiki


class Form(object):
    """
    Provide form support
    """
    def __init__(self, dpage, form, submit='Submit', initial=None, action_url=None, **kwargs):
        """
        Create a form object.

        :param dpage: dpage object
        :type dpage: DPage
        :param form: form object
        :type form: forms.Form
        :param submit: text for submit button.  If None, no submit button.
        :type submit: unicode
        :param initial: initial bound values
        :type initial: dict or None
        :param action_url: submit action url
        :type action_url: unicode
        :param kwargs: RFU
        :type kwargs: dict
        """
        self.dpage = dpage
        self.form = form
        self.submit = submit
        self.initial = initial
        self.action_url = action_url
        self.kwargs = kwargs
        # todo 2: add other kwargs options here
        pass

    # noinspection PyUnusedLocal
    def render(self, **kwargs):
        """
        Create and render the form
        """
        #
        #  Alternate form template
        #
        # <form method="post" class="bootstrap3" action="/graphpages/graphpage/{{ graph_pk }}"> {% csrf_token %}
        #     {# Include the hidden fields #}
        #     {% for hidden in graphform.hidden_fields %}
        #         {{ hidden }}
        #     {% endfor %}
        #     {# Include the visible fields #}
        #     {% for field in graphform.visible_fields %}
        #         {% if field.errors %}
        #             <div class="row bg-danger">
        #                 <div class="col-md-3 text-right"></div>
        #                 <div class="col-md-7">{{ field.errors }}</div>
        #             </div>
        #         {% endif %}
        #         <div class="row">
        #             <div class="col-md-3 text-right">{{ field.label_tag }}</div>
        #             <div class="col-md-7">{{ field }}</div>
        #         </div>
        #     {% endfor %}
        #     <div class="row">
        #         <div class='col-md-3 text-right'>
        #             <input type="submit" value="Display graph" class="btn btn-primary"/>
        #         </div>
        #     </div>
        # </form>
        #
        # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),
        if self.initial:
            the_form = self.form(self.initial)
        elif len(self.dpage.request.POST) > 0:
            the_form = self.form(self.dpage.request.POST)
        else:
            the_form = self.form()
        request = self.dpage.request
        form_class_name = self.form.__name__
        template_top = '{% load bootstrap3 %}\n' \
                       '<!-- start of django bootstrap3 form -->\n' \
                       '    <form role="form" action="{action_url}" method="post" class="form">\n' \
                       '        <!-- csrf should be here -->{% csrf_token %}<!-- -->\n' \
                       '        <!-- our form class name -->' \
                       '            <input type="hidden" name="form_class_name" value="{form_class_name}" >\n' \
                       '        {% bootstrap_form the_form %}\n'
        template_button = '        {% buttons %}\n' \
                          '            <button type="submit" class="btn btn-primary">\n' \
                          '                {% bootstrap_icon "star" %} {submit_text}\n' \
                          '            </button>\n' \
                          '        {% endbuttons %}\n'
        template_bottom = '    </form>\n' \
                          '<!-- end of django bootstrap3 form -->\n'
        template = template_top
        if self.submit:
            template += template_button
        template += template_bottom

        # Do NOT use format here since the template contains {% ... %}
        template = template.replace('{action_url}', self.action_url if self.action_url else '/dpages/')
        template = template.replace('{form_class_name}', form_class_name)
        if self.submit:
            template = template.replace('{submit_text}', self.submit)
        t = Template(template)
        c = {'the_form': the_form}
        c.update(csrf(request))
        output = t.render(Context(c))
        return output
        # return template

# todo 1: add support for normal bootstrap 3 forms
# todo 1: add id to Form

########################################################################################################################
#
# Carousel
#
########################################################################################################################


class Carousel(object):
    """
    Carousel
    """
    def __init__(self, *content, **kwargs):
        self.content = content
        self.id = kwargs.pop('id', unique_name('carousel_id'))
        self.data_interval = kwargs.pop('data-interval', 'false')
        self.indicators = kwargs.pop('indicators', None)
        self.background_color = kwargs.pop('background-color', '#D8D8D8')
        return

    def render(self):
        # t_ind = '<!-- Start Bottom Carousel Indicators -->\n' \
        #         '<ol class="carousel-indicators">\n' \
        #         '    <li data-target="#{carousel_id}" data-slide-to="0" class="active"></li>\n' \
        #         '    <li data-target="#{carousel_id}" data-slide-to="1"></li>\n' \
        #         '    <li data-target="#{carousel_id}" data-slide-to="2"></li>\n' \
        #         '</ol>\n<!-- End Bottom Carousel Indicators -->\n'
        out = """
                  <div class="carousel slide" data-ride="carousel" id="{carousel_id}" data-interval="{data_interval}">

                    <!-- Carousel Slides / Quotes -->
                    <div class="carousel-inner" style="background-color: {background_color};">

                      <!-- Quote 1 -->
                      <div class="item active">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <small>Someone famous</small>
                              <p>1 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>2 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>3 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>4 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>5 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>6 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                              <p>7 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
                                 adipisci velit!</p>
                            </div>
                          </div>
                      </div>
                      <!-- Quote 2 -->
                      <div class="item">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam auctor nec lacus ut
                                 tempor. Mauris.</p>
                            </div>
                          </div>
                      </div>
                      <!-- Quote 3 -->
                      <div class="item">
                          <div class="row">
                            <div class="col-sm-9">
                              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut rutrum elit in arcu
                                 blandit, eget pretium nisl accumsan. Sed ultricies commodo tortor, eu pretium
                                 mauris.</p>
                            </div>
                          </div>
                      </div>
                    </div>

                    <!-- Carousel Buttons Next/Prev -->
                    <a data-slide="prev" href="#{carousel_id}" class="left carousel-control">
                        <i class="fa fa-chevron-left"></i>
                    </a>
                    <a data-slide="next" href="#{carousel_id}" class="right carousel-control">
                        <i class="fa fa-chevron-right"></i>
                    </a>


                  </div>
            """
        # todo 1: finish this
        t_jsf = """
                    <!-- Controls buttons -->
                    <div style="text-align:center;">
                      <input type="button" class="btn start-slide" value="Start">
                      <input type="button" class="btn pause-slide" value="Pause">
                      <input type="button" class="btn prev-slide" value="Previous Slide">
                      <input type="button" class="btn next-slide" value="Next Slide">
                      <input type="button" class="btn slide-one" value="Slide 1">
                      <input type="button" class="btn slide-two" value="Slide 2">
                      <input type="button" class="btn slide-three" value="Slide 3">
                    </div>
                  <script>
                     $(function(){
                        // Initializes the carousel
                        $(".start-slide").click(function(){
                           $("#{carousel_id}").carousel('cycle');
                        });
                        // Stops the carousel
                        $(".pause-slide").click(function(){
                           $("#{carousel_id}").carousel('pause');
                        });
                        // Cycles to the previous item
                        $(".prev-slide").click(function(){
                           $("#{carousel_id}").carousel('prev');
                        });
                        // Cycles to the next item
                        $(".next-slide").click(function(){
                           $("#{carousel_id}").carousel('next');
                        });
                        // Cycles the carousel to a particular frame
                        $(".slide-one").click(function(){
                           $("#{carousel_id}").carousel(0);
                        });
                        $(".slide-two").click(function(){
                           $("#{carousel_id}").carousel(1);
                        });
                        $(".slide-three").click(function(){
                           $("#{carousel_id}").carousel(2);
                        });
                     });
                  </script>
                """
        out = out.format(carousel_id=self.id,
                         data_interval=self.data_interval,
                         background_color=self.background_color)
        # out += t_jsf.replace('{carousel_id}', self.id)
        return out
