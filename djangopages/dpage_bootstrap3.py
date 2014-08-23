#!/usr/bin/env python
# coding=utf-8

"""
Bootstrap Widgets
=================

.. module:: dpage_bootstrap3
   :synopsis: Provides DjangoPage widgets to create various bootstrap elements

.. moduleauthor:: Richard Bell <rbell01824@gmail.com>

DjangoPages provides a number of widgets to create various bootstrap elements.

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

# noinspection PyProtectedMember
from djangopages.libs import unique_name

########################################################################################################################
#
# Various Bootstrap widgets.
#
#
#
# todo: add remaining bootstrap widgets
# todo: heading small support
# todo: add lead body copy support
# todo: add small, bold, italics
# todo: add alignment, abbreviations, initialism, addresses, blockquote, etc
# todo: add ordered and unordered lists
# todo: gr through bootstrap CSS and add full support
#
########################################################################################################################


# noinspection PyPep8Naming
def Accordion(accordion_panels):
    """ Bootstrap accordion

    .. sourcecode:: python

        Accordion((AccordionPanel('heading 1', 'content 1', expand=True),
                   AccordionPanel('heading 2', 'content 2'))

    :param accordion_panels: accordion panels
    :type accordion_panels: list or tuple
    :return: HTML for bootstrap accordion
    :rtype: unicode
    """
    assert isinstance(accordion_panels, (list, tuple))
    accordion_id = unique_name('aid')
    panels = ''
    for p in accordion_panels:
        panels += p.generate(accordion_id)
    template = '<!-- Accordion start -->' \
               '    <div class="panel-group" id="{accordion_id}">\n' \
               '        {panels}\n' \
               '    </div>\n' \
               '<!--Accordion end -->'
    rtn = template.format(accordion_id=accordion_id,
                          panels=panels)
    return rtn


# noinspection PyPep8Naming
class AccordionPanel(object):
    """ Defines an accordion panel for use in Accordion.  See Accordion.

    .. sourcecode::

        AccordinPanel('Panel title', 'Panel body')

    :param title: Panel title
    :type title: str or unicode
    :param body: Panel body
    :type body: str or unicode
    :param expand: if true, panel is initially expanded, otherwise collapsed
    :type expand: bool
    :param panel_type: type for panel
    :type panel_type: str or unicode

    | Synonyms:
    | AccordionPanelDefault = functools.partial(AccordionPanel, panel_type='panel-default')
    | AccordionPanelPrimary = functools.partial(AccordionPanel, panel_type='panel-primary')
    | AccordionPanelSuccess = functools.partial(AccordionPanel, panel_type='panel-success')
    | AccordionPanelInfo = functools.partial(AccordionPanel, panel_type='panel-info')
    | AccordionPanelWarning = functools.partial(AccordionPanel, panel_type='panel-warning')
    | AccordionPanelDanger = functools.partial(AccordionPanel, panel_type='panel-danger')
    """
    def __init__(self, title='', body='', expand=False, panel_type='panel-default'):
        """
        :param title: Panel title
        :type title: str or unicode
        :param body: Panel body
        :type body: str or unicode
        :param expand: if true, panel is initially expanded, otherwise collapsed
        :type expand: bool
        :param panel_type: type for panel
        :type panel_type: str or unicode
        """
        self.title = title
        self.body = body
        self.expand = expand
        self.panel_type = panel_type
        return

    def generate(self, accordion_id):
        template = '<!-- Accordion panel start -->\n' \
                   '  <div class="panel {panel_type}">\n' \
                   '    <div class="panel-heading">\n' \
                   '      <h4 class="panel-title">\n' \
                   '        <a data-toggle="collapse" data-parent="#{accordion_id}" href="#{panel_id}">\n' \
                   '          {heading}\n' \
                   '        </a>\n' \
                   '      </h4>\n' \
                   '    </div>\n' \
                   '    <div id="{panel_id}" class="panel-collapse collapse {expand}">\n' \
                   '      <div class="panel-body">\n' \
                   '        {content}\n' \
                   '      </div>\n' \
                   '    </div>\n' \
                   '  </div>\n' \
                   '<!-- Accordion panel end -->'
        panel_id = unique_name('apid')
        expand = 'in' if self.expand else ''
        rtn = template.format(accordion_id=accordion_id,
                              panel_id=panel_id,
                              panel_type=self.panel_type,
                              heading=self.title,
                              content=self.body,
                              expand=expand)
        return rtn
AccordionPanelDefault = functools.partial(AccordionPanel, panel_type='panel-default')
AccordionPanelPrimary = functools.partial(AccordionPanel, panel_type='panel-primary')
AccordionPanelSuccess = functools.partial(AccordionPanel, panel_type='panel-success')
AccordionPanelInfo = functools.partial(AccordionPanel, panel_type='panel-info')
AccordionPanelWarning = functools.partial(AccordionPanel, panel_type='panel-warning')
AccordionPanelDanger = functools.partial(AccordionPanel, panel_type='panel-danger')


# noinspection PyPep8Naming
def Button(text, button='btn-default', size='', disabled=False, classes='', style=''):
    """ Bootstrap button

    .. sourcecode:: python

        Button('Button 1', button='btn-success btn-sm')

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
    :return: HTML for bootstrap button
    :rtype: unicode

    | Synonyms:
    | BTN = functools.partial(Button)
    | BTNPrimary = functools.partial(Button, button='btn-primary')
    | BTNSuccess = functools.partial(Button, button='btn-success')
    | BTNInfo = functools.partial(Button, button='btn-info')
    | BTNWarning = functools.partial(Button, button='btn-warning')
    | BTNDanger = functools.partial(Button, button='btn-danger')
    | BTNL = functools.partial(Button, size='btn-lg')
    | BTNLPrimary = functools.partial(Button, button='btn-primary', size='btn-lg')
    | BTNLSuccess = functools.partial(Button, button='btn-success', size='btn-lg')
    | BTNLInfo = functools.partial(Button, button='btn-info', size='btn-lg')
    | BTNLWarning = functools.partial(Button, button='btn-warning', size='btn-lg')
    | BTNLDanger = functools.partial(Button, button='btn-danger', size='btn-lg')
    | BTNS = functools.partial(Button, size='btn-sm')
    | BTNSPrimary = functools.partial(Button, button='btn-primary', size='btn-sm')
    | BTNSSuccess = functools.partial(Button, button='btn-success', size='btn-sm')
    | BTNSInfo = functools.partial(Button, button='btn-info', size='btn-sm')
    | BTNSWarning = functools.partial(Button, button='btn-warning', size='btn-sm')
    | BTNSDanger = functools.partial(Button, button='btn-danger', size='btn-sm')
    | BTNXS = functools.partial(Button, size='btn-xs')
    | BTNXSPrimary = functools.partial(Button, button='btn-primary', size='btn-xs')
    | BTNXSSuccess = functools.partial(Button, button='btn-success', size='btn-xs')
    | BTNXSInfo = functools.partial(Button, button='btn-info', size='btn-xs')
    | BTNXSWarning = functools.partial(Button, button='btn-warning', size='btn-xs')
    | BTNXSDanger = functools.partial(Button, button='btn-danger', size='btn-xs')
    """
    template = '<!-- start of button -->\n' \
               '    <button type="button" {classes} {disabled} {style}>\n' \
               '        {text}\n' \
               '    </button>\n' \
               '<!-- end of button -->\n'
    if isinstance(text, (tuple, list)):
        rtn = ''
        for t in text:
            rtn += Button(t, button, size, disabled, classes, style)
        return rtn
    if disabled:
        disabled = 'disabled="disabled" '
    classes = 'class="btn {button} {size} {classes}" '.format(button=button, size=size, classes=classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(classes=classes, disabled=disabled, style=style, text=text)
    return rtn
BTN = functools.partial(Button)
BTNPrimary = functools.partial(Button, button='btn-primary')
BTNSuccess = functools.partial(Button, button='btn-success')
BTNInfo = functools.partial(Button, button='btn-info')
BTNWarning = functools.partial(Button, button='btn-warning')
BTNDanger = functools.partial(Button, button='btn-danger')
BTNL = functools.partial(Button, size='btn-lg')
BTNLPrimary = functools.partial(Button, button='btn-primary', size='btn-lg')
BTNLSuccess = functools.partial(Button, button='btn-success', size='btn-lg')
BTNLInfo = functools.partial(Button, button='btn-info', size='btn-lg')
BTNLWarning = functools.partial(Button, button='btn-warning', size='btn-lg')
BTNLDanger = functools.partial(Button, button='btn-danger', size='btn-lg')
BTNS = functools.partial(Button, size='btn-sm')
BTNSPrimary = functools.partial(Button, button='btn-primary', size='btn-sm')
BTNSSuccess = functools.partial(Button, button='btn-success', size='btn-sm')
BTNSInfo = functools.partial(Button, button='btn-info', size='btn-sm')
BTNSWarning = functools.partial(Button, button='btn-warning', size='btn-sm')
BTNSDanger = functools.partial(Button, button='btn-danger', size='btn-sm')
BTNXS = functools.partial(Button, size='btn-xs')
BTNXSPrimary = functools.partial(Button, button='btn-primary', size='btn-xs')
BTNXSSuccess = functools.partial(Button, button='btn-success', size='btn-xs')
BTNXSInfo = functools.partial(Button, button='btn-info', size='btn-xs')
BTNXSWarning = functools.partial(Button, button='btn-warning', size='btn-xs')
BTNXSDanger = functools.partial(Button, button='btn-danger', size='btn-xs')


# noinspection PyPep8Naming
def Glyphicon(glyph, classes='', style=''):
    """ Bootstrap glyphicon

    .. sourcecode:: python

        Glyphicon('star')
        Glyphicon('glyphicon-star')

    :param glyph: glyph name in the form 'simple_name' or 'glyphicon-simple_name'
    :type glyph: str or unicode or tuple
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: Glyphicon html
    :rtype: unicode

    | Synonym: GL(...), useful abbreviation
    """

    if isinstance(glyph, (tuple, list)):
        rtn = ''
        for g in glyph:
            rtn += Glyphicon(g, classes, style)
        return rtn
    template = '<span {classes} {style}></span>'
    if not glyph.startswith('glyphicon-'):
        glyph = 'glyphicon-' + glyph
    classes = 'class="glyphicon {glyph} {classes}" '.format(glyph=glyph, classes=classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(classes=classes, style=style)
    return rtn
GL = functools.partial(Glyphicon)


# noinspection PyPep8Naming
def Hn(heading, level=3, classes='', style=''):
    """ HTML heading

    .. sourcecode:: python

        Hn('Header text')
        Hn('Header text' + Small('subtext'), level=2)

    :param heading: heading text
    :type heading: str or unicode
    :param level: heading level
    :type level: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML H html
    :rtype: unicode

    | Synonyms:
    | H1 = functools.partial(Hn, level=1)
    | H2 = functools.partial(Hn, level=2)
    | H3 = functools.partial(Hn, level=3)
    | H4 = functools.partial(Hn, level=4)
    | H5 = functools.partial(Hn, level=5)
    | H6 = functools.partial(Hn, level=6)
    """
    if isinstance(heading, (list, tuple)):
        rtn = ''
        for h in heading:
            rtn += Hn(h, level, classes, style)
        return rtn
    template = '<h{level} {classes} {style}>\n' \
               '    {heading}\n' \
               '</h{level}>'
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    level = str(level)
    rtn = template.format(level=level, classes=classes, style=style, heading=heading)
    return rtn
H1 = functools.partial(Hn, level=1)
H2 = functools.partial(Hn, level=2)
H3 = functools.partial(Hn, level=3)
H4 = functools.partial(Hn, level=4)
H5 = functools.partial(Hn, level=5)
H6 = functools.partial(Hn, level=6)


# noinspection PyPep8Naming
def Header(heading, classes='', style=''):
    """ Bootstrap page-header component

    .. sourcecode:: python

        Header('Header text')
        Header(H3('heading'+Small('subheading'))

    :param heading: heading HTML
    :type heading: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: Header html
    :rtype: unicode
    """
    if isinstance(heading, (tuple, list)):
        rtn = ''
        for h in heading:
            rtn += Header(h, classes, style)
        return rtn

    template = '<!-- header start -->\n' \
               '    <div class="page-header">\n' \
               '        {heading}\n' \
               '    </div>' \
               '<!-- header end -->\n'
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(classes=classes, style=style, heading=heading)
    return rtn


# noinspection PyPep8Naming
def Jumbotron(content, classes='', style=''):
    """ Bbootstrap jumbotron

    .. sourcecode:: python

        Jumbotro('Jumbotron content')
        Jumbotron(MD('#Jumbotron 2') + 'Some text' + BTNSInfo('Button'))

    :param content: content
    :type content: basestring or tuple or DWidget
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: Glyphicon html
    :rtype: unicode
    """
    if isinstance(content, (tuple, list)):
        rtn = ''
        for c in content:
            rtn += Jumbotron(c, classes, style)
        return rtn
    template = '<!-- jumbotron start -->' \
               '<div class="jumbotron">\n' \
               '{content}\n' \
               '</div>\n' \
               '<!-- jumbotron end -->'
    assert isinstance(content, (str, unicode))
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(classes=classes, style=style, content=content)
    return rtn


# noinspection PyPep8Naming
def Label(content, label_type='label-default', classes='', style=''):
    """ Bootstrap label

    .. sourcecode:: python

        Label('default', 'text of default label',
              'primary', 'text of primary label')

    :param content: content, label_type, label_text, ...
    :type content: basestring or tuple or DWidget
    :param label_type: label type in the form 'simple_label' or 'label-simple_label'
    :type label_type: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: label html
    :rtype: unicode
    """

    if isinstance(content, (list, tuple)):
        rtn = ''
        for c in content:
            rtn += Label(c, label_type, classes, style)
        return rtn

    template = '<span {classes} {style}>{content}</span>'
    if not label_type.startswith('label-'):
        label_type = 'label-' + label_type
    classes = 'class="label {label_type} {classes}" '.format(label_type=label_type, classes=classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(content=content, classes=classes, style=style)
    return rtn


# class Link(DWidget):
#     """
#     .. sourcecode:: python
#
#         Link('/dpages/somepage', 'link to somepage',
#              '/dpages/anotherpage', 'link to anotherpage')
#
#     :param content: content
#     :type content: basestring or tuple or DWidget
#     :param kwargs: standard kwargs
#     :type kwargs: dict
#
#     additional kwargs
#
#     :param button: default 'btn-default', button type for the link
#     :type button: str
#     :param disabled: default False, if true button is disabled
#     :type disabled: bool
#     """
#
#     template = '<a href="{href}" {classes} {style} {disabled} {role}>{content}</a>'
#
#     def __init__(self, *content, **kwargs):
#         super(Link, self).__init__(content, kwargs)
#         return
#
#     def generate(self, template, content, classes, style, kwargs):
#         assert isinstance(content, tuple)
#         disabled = kwargs.get('disabled', '')
#         button = kwargs.get('button', 'btn-default')
#         role = ''
#         if button:
#             # make sure have a button type specified
#             for t in ('btn-default', 'btn-primary', 'btn-success', 'btn-info', 'btn-warning',
#                   'btn-danger', 'btn-link'):
#                 if t in button:
#                     break
#             else:
#                 button += ' btn-default'
#             classes = self.add_classes(classes, 'btn {button}'.format(button=button))
#             role = 'role="button"'
#         out = ''
#         for hr, con in zip(content[::2], content[1::2]):
#             out += template.format(href=hr, classes=classes, style=style, disabled=disabled, role=role,
#                                    content=con)
#         return out


# noinspection PyPep8Naming
def PanelFooter(footer='', classes='', style=''):
    """ Bootstrap Panel footer

    .. sourcecode:: python

        PanelFooter('Text for panel footer')

    :param footer: footer
    :type footer: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for panel footer
    :rtype: unicode
    """
    classes = 'class="panel-footer {classes}" '.format(classes=classes)
    if style:
        style = 'style="{}" '.format(style)
    template = '<div {classes} {style} >\n' \
               '    {footer}\n' \
               '</div>\n'
    return template.format(classes=classes, style=style, footer=footer)


# noinspection PyPep8Naming
def PanelHeading(heading='', level=3, classes='', style=''):
    """ Bootstrap Panel heading

    .. sourcecode:: python

        PanelHeading('Text for panel heading')

    :param heading: heading
    :type heading: str or unicode
    :param level: if > 0, heading title level, otherwise no title component
    :type level: int
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: HTML for panel heading
    :rtype: unicode
    """
    classes = 'class="panel-heading {classes}" '.format(classes=classes)
    if style:
        style = 'style="{}" '.format(style)
    if level > 0:
        template = '<div {classes} {style} >\n' \
                   '    <h{level} class="panel-title" >\n' \
                   '        {heading}\n' \
                   '    </h{level}>' \
                   '</div>\n'
        return template.format(classes=classes, style=style, level=level, heading=heading)
    template = '<div {classes} {style} >\n' \
               '    {heading}\n' \
               '</div>\n'
    return template.format(classes=classes, style=style, heading=heading)


# noinspection PyPep8Naming
def Panel(body='', heading='', footer='', panel_type='panel-default'):
    """ Bootstrap panel

    .. sourcecode:: python

        Panel('panel body',
              PanelHeading('panel heading'),
              PanelFooter('panel footer'))

    :param body: body content for panel
    :type body: str or unicode
    :param heading: heading content for panel
    :type heading: str or unicode
    :param footer: footer content for panel
    :type footer: str or unicode
    :param panel_type: type for panel
    :type panel_type: str or unicode
    :return: HTML for panel
    :rtype: unicode

    | Synonyms:
    | PanelDefault = functools.partial(Panel, panel_type='panel-default')
    | PanelPrimary = functools.partial(Panel, panel_type='panel-primary')
    | PanelSuccess = functools.partial(Panel, panel_type='panel-success')
    | PanelInfo = functools.partial(Panel, panel_type='panel-info')
    | PanelWarning = functools.partial(Panel, panel_type='panel-warning')
    | PanelDanger = functools.partial(Panel, panel_type='panel-danger')
    """
    template = '<div class="panel {panel_type}" >\n ' \
               '    {heading}\n' \
               '    <div class="panel-body">\n' \
               '        {body}' \
               '    </div>\n ' \
               '    {footer}\n' \
               '</div>'
    rtn = template.format(panel_type=panel_type,
                          heading=heading,
                          body=body,
                          footer=footer)
    return rtn
PanelDefault = functools.partial(Panel, panel_type='panel-default')
PanelPrimary = functools.partial(Panel, panel_type='panel-primary')
PanelSuccess = functools.partial(Panel, panel_type='panel-success')
PanelInfo = functools.partial(Panel, panel_type='panel-info')
PanelWarning = functools.partial(Panel, panel_type='panel-warning')
PanelDanger = functools.partial(Panel, panel_type='panel-danger')


# class Modal(DWidget):
#     """
#     .. sourcecode:: python
#
#         Modal( heading='', body='', footer='', button='Show', modal_size='', button_type='btn-primary', **kwargs):
#
#     :param heading: heading for modal panel
#     :type heading: basestring or DWidget
#     :param body: body for modal panel
#     :type body: basestring or DWidget
#     :param footer: footer modal panel
#     :type footer: basestring or DWidget
#     :param button: text for modal button
#     :type button: basestring or DWidget
#     :param modal_size: modal size per bootstrap
#     :type modal_size: basestring or DWidget
#     :param button_type: button type
#     :type button_type: basestring or DWidget
#     :param kwargs: standard kwargs
#     :type kwargs: dict
#     """
#     template = """
# <!-- Button trigger modal -->
# <button class="btn {button_type}" data-toggle="modal" data-target="#{modal_id}">
#   {button}
# </button>
# <!-- / Button trigger modal -->
#
# <!-- .modal -->
# <div class="modal fade " id={modal_id} tabindex="-1" role="dialog" aria-labelledby="{modal_label}" aria-hidden="true">
#   <!-- .modal-dialog -->
#   <div class="modal-dialog {modal_size}">
#     <!-- .modal-content -->
#     <div class="modal-content">
#       <!-- .modal-header -->
#       <div class="modal-header">
#         <button type="button" class="close" data-dismiss="modal">
#           <span aria-hidden="true">&times;</span><span class="sr-only">Close</span>
#         </button>
#         <h4 class="modal-title" id={modal_label}>{heading}</h4>
#       </div>
#       <!-- /.modal-header -->
#       <!-- .modal-body -->
#       <div class="modal-body">
#         {body}
#       </div>
#       <!-- /.modal-body -->
#       <!-- .modal-footer -->
#       <div class="modal-footer">
#         {footer}
#       </div>
#       <!-- /.modal-footer -->
#     </div>
#     <!-- /.modal-content -->
#   </div>
#   <!-- /.modal-dialog -->
# </div>
# <!-- /.modal -->
#     """
#
#     def __init__(self, heading='', body='', footer='',
#                  button='Show', modal_size='', button_type='btn-primary', **kwargs):
#         super(Modal, self).__init__((heading, body, footer, button, modal_size, button_type), kwargs)
#         return
#
#     def generate(self, template, content, classes, style, kwargs):
#         assert isinstance(content, tuple)
#         heading, body, footer, button, modal_size, button_type = content[0:7]
#         modal_id = unique_name('id_m_')
#         modal_label = unique_name('lbl_m_')
#         out = template.format(heading=heading, body=body, footer=footer,
#                               modal_id=modal_id, modal_label=modal_label,
#                               modal_size=modal_size,
#                               button=button, button_type=button_type)
#         return out


# noinspection PyPep8Naming
def Small(text, classes='', style=''):
    """
    :param text: text to wrap
    :type text: str or unicode
    :param classes: classes to add to output
    :type classes: str or unicode
    :param style: styles to add to output
    :type style: str or unicode
    :return: small html
    :rtype: unicode
    """
    if isinstance(text, (list, tuple)):
        rtn = ''
        for t in text:
            rtn += Small(t, classes, style)
        return rtn
    template = '<small {classes} {style}>\n' \
               '    {text}\n' \
               '</small>\n'
    if classes:
        classes = 'class="{}" '.format(classes)
    if style:
        style = 'style="{}" '.format(style)
    rtn = template.format(classes=classes, style=style, text=text)
    return rtn

# ################################################################################
# ################################################################################
#
# # fixme: finish table  do this: http://www.pontikis.net/labs/bs_grid/demo/
#
#
# # class Table(object):
# #     """
# #     Table support
# #
# #     table-responsive
# #     table-condensed
# #     table-hover
# #     table-bordered
# #     table-striped
# #     """
# #     def __init__(self, heading, *content, **kwargs):
# #         self.heading = heading
# #         self.content = content
# #         self.tresponsive = kwargs.pop('tbl_class', None)
# #         self.kwargs = kwargs
# #         pass
# #
# #     def render(self):
# #         out = ''
# #         # Build table class
# #         # cls = 'table'
# #
# #         return out
# #
# #
# # class TableRow(object):
# #     """
# #     Table row support
# #
# #       <tr>
# #          <td>January</td>
# #          <td>$100</td>
# #       </tr>
# #     """
# #     def __init__(self, *content, **kwargs):
# #         self.content = content
# #         self.tr_class = kwargs.pop('tr_class', None)
# #         self.kwargs = kwargs
# #         pass
# #
# #     def render(self):
# #         out = ''
# #         for con in self.content:
# #             if isinstance(con, TableCell):
# #                 out += _render(con)
# #             else:
# #                 out += '<td>' + _render(con) + '</td>'
# #         tr_start = '<tr>'
# #         if self.tr_class:
# #             tr_start = '<tr class="{tr_class}" >'.format(self.tr_class)
# #         out = tr_start + out + '</tr>'
# #         return out
# #
# #
# # # noinspection PyPep8Naming
# # def TR(*content, **kwargs):
# #     tr = TableRow(content, kwargs)
# #     return tr
# #
# #
# # class TableCell(object):
# #     """
# #     Table cell support
# #     """
# #     def __init__(self, *content, **kwargs):
# #         """
# #         Initialize a td table element
# #
# #         :param content: content
# #         :type content: object or list
# #         :param kwargs: RFU
# #         :type: dict
# #         """
# #         self.content = content
# #         self.td_class = kwargs.pop('td_class', None)
# #         self.kwargs = kwargs
# #         pass
# #
# #     def render(self):
# #         td_start = '<td>'
# #         if self.td_class:
# #             td_start = '<td class="{td_class}" >'.format(td_class=self.td_class)
# #         out = ''
# #         for con in self.content:
# #             out += td_start + _render(con) + '</td>\n'
# #         return out
# #
# #
# # # noinspection PyPep8Naming
# # def TD(*content, **kwargs):
# #     td = TableCell(content, kwargs)
# #     return td
# #
# #
# # class TableHead(object):
# #     """
# #     Table head support
# #
# #      <thead>
# #       <tr>
# #          <th>Month</th>
# #          <th>Savings</th>
# #       </tr>
# #      </thead>
# #
# #     """
# #     def __init__(self, *content, **kwargs):
# #         """
# #         """
# #         pass
# #
# #     def render(self):
# #         out = ''
# #         return out
# #
# #
# # class TableFoot(object):
# #     """
# #     Table foot support
# #
# #      <tfoot>
# #       <tr>
# #          <td>Sum</td>
# #          <td>$180</td>
# #       </tr>
# #      </tfoot>
# #
# #     """
# #     def __init__(self, *content, **kwargs):
# #         """
# #         """
# #         pass
# #
# #     def render(self):
# #         # todo 1: finish this
# #         out = ''
# #         return out
# #
# #
# # class Table2(object):
# #     """
# #     Provide django-tables2 support
# #     """
# #     def __init__(self, dpage, qs, **kwargs):
# #         """
# #         Initialize a Table object
# #
# #         :param dpage: dpage object
# #         :type dpage: DPage
# #         :param qs: Queryset
# #         :type qs:
# #         :param kwargs: RFU
# #         :type kwargs: dict
# #         """
# #         self.dpage = dpage
# #         self.qs = qs
# #         self.kwargs = kwargs
# #         # todo 2: add other kwargs options here
# #         pass
# #
# #     # noinspection PyUnusedLocal
# #     def render(self, **kwargs):
# #         """
# #         Generate html for table
# #         """
# #         template = '<!-- start of table -->\n' \
# #                    '    {% load django_tables2 %}\n' \
# #                    '    {% render_table insert_the_table %}\n' \
# #                    '<!-- end of table -->\n'
# #         t = Template(template)
# #         c = {'insert_the_table': self.qs, 'request': self.dpage.request}
# #         output = t.render(Context(c))
# #         return output
# #         # output = ''
# #         # name = unique_name('table')
# #         # self.dpage.context[name] = self.qs
# #         # template = '<!-- start of table -->\n' \
# #         #            '    {% render_table x_the_table_object %}\n' \
# #         #            '<!-- end of table -->\n'
# #         # output = template.replace('x_the_table_object', name)
# #         # return output
# #
# # # todo 1: add support for table sorter: http://mottie.github.io/tablesorter/docs/index.html
# # # http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# # # looks good: http://mottie.github.io/tablesorter/docs/example-widget-bootstrap-theme.html
# # # https://github.com/Mottie/tablesorter/wiki
# #
# #
# # class Form(object):
# #     """
# #     Provide form support
# #     """
# #     def __init__(self, dpage, form, submit='Submit', initial=None, action_url=None, **kwargs):
# #         """
# #         Create a form object.
# #
# #         :param dpage: dpage object
# #         :type dpage: DPage
# #         :param form: form object
# #         :type form: forms.Form
# #         :param submit: text for submit button.  If None, no submit button.
# #         :type submit: unicode
# #         :param initial: initial bound values
# #         :type initial: dict or None
# #         :param action_url: submit action url
# #         :type action_url: unicode
# #         :param kwargs: RFU
# #         :type kwargs: dict
# #         """
# #         self.dpage = dpage
# #         self.form = form
# #         self.submit = submit
# #         self.initial = initial
# #         self.action_url = action_url
# #         self.kwargs = kwargs
# #         # todo 2: add other kwargs options here
# #         pass
# #
# #     # noinspection PyUnusedLocal
# #     def render(self, **kwargs):
# #         """
# #         Create and render the form
# #         """
# #         #
# #         #  Alternate form template
# #         #
# #         # <form method="post" class="bootstrap3" action="/graphpages/graphpage/{{ graph_pk }}"> {% csrf_token %}
# #         #     {# Include the hidden fields #}
# #         #     {% for hidden in graphform.hidden_fields %}
# #         #         {{ hidden }}
# #         #     {% endfor %}
# #         #     {# Include the visible fields #}
# #         #     {% for field in graphform.visible_fields %}
# #         #         {% if field.errors %}
# #         #             <div class="row bg-danger">
# #         #                 <div class="col-md-3 text-right"></div>
# #         #                 <div class="col-md-7">{{ field.errors }}</div>
# #         #             </div>
# #         #         {% endif %}
# #         #         <div class="row">
# #         #             <div class="col-md-3 text-right">{{ field.label_tag }}</div>
# #         #             <div class="col-md-7">{{ field }}</div>
# #         #         </div>
# #         #     {% endfor %}
# #         #     <div class="row">
# #         #         <div class='col-md-3 text-right'>
# #         #             <input type="submit" value="Display graph" class="btn btn-primary"/>
# #         #         </div>
# #         #     </div>
# #         # </form>
# #         #
# #         # Technique to submit on channge: widget=forms.Select(attrs={'onChange': 'this.form.submit()'}),
# #         if self.initial:
# #             the_form = self.form(self.initial)
# #         elif len(self.dpage.request.POST) > 0:
# #             the_form = self.form(self.dpage.request.POST)
# #         else:
# #             the_form = self.form()
# #         request = self.dpage.request
# #         form_class_name = self.form.__name__
# #         template_top = '{% load bootstrap3 %}\n' \
# #                        '<!-- start of django bootstrap3 form -->\n' \
# #                        '    <form role="form" action="{action_url}" method="post" class="form">\n' \
# #                        '        <!-- csrf should be here -->{% csrf_token %}<!-- -->\n' \
# #                        '        <!-- our form class name -->' \
# #                        '            <input type="hidden" name="form_class_name" value="{form_class_name}" >\n' \
# #                        '        {% bootstrap_form the_form %}\n'
# #         template_button = '        {% buttons %}\n' \
# #                           '            <button type="submit" class="btn btn-primary">\n' \
# #                           '                {% bootstrap_icon "star" %} {submit_text}\n' \
# #                           '            </button>\n' \
# #                           '        {% endbuttons %}\n'
# #         template_bottom = '    </form>\n' \
# #                           '<!-- end of django bootstrap3 form -->\n'
# #         template = template_top
# #         if self.submit:
# #             template += template_button
# #         template += template_bottom
# #
# #         # Do NOT use format here since the template contains {% ... %}
# #         template = template.replace('{action_url}', self.action_url if self.action_url else '/dpages/')
# #         template = template.replace('{form_class_name}', form_class_name)
# #         if self.submit:
# #             template = template.replace('{submit_text}', self.submit)
# #         t = Template(template)
# #         c = {'the_form': the_form}
# #         c.update(csrf(request))
# #         output = t.render(Context(c))
# #         return output
# #         # return template
# #
# # # todo 1: add support for normal bootstrap forms
# # # todo 1: add id to Form
# #
# ########################################################################################################################
# #
# # Carousel
# #
# ########################################################################################################################
# #
# #
# # class Carousel(object):
# #     """
# #     Carousel
# #     """
# #     def __init__(self, *content, **kwargs):
# #         self.content = content
# #         self.id = kwargs.pop('id', unique_name('carousel_id'))
# #         self.data_interval = kwargs.pop('data-interval', 'false')
# #         self.indicators = kwargs.pop('indicators', None)
# #         self.background_color = kwargs.pop('background-color', '#D8D8D8')
# #         return
# #
# #     def render(self):
# #         # t_ind = '<!-- Start Bottom Carousel Indicators -->\n' \
# #         #         '<ol class="carousel-indicators">\n' \
# #         #         '    <li data-target="#{carousel_id}" data-slide-to="0" class="active"></li>\n' \
# #         #         '    <li data-target="#{carousel_id}" data-slide-to="1"></li>\n' \
# #         #         '    <li data-target="#{carousel_id}" data-slide-to="2"></li>\n' \
# #         #         '</ol>\n<!-- End Bottom Carousel Indicators -->\n'
# #         out = """
# #                   <div class="carousel slide" data-ride="carousel" id="{carousel_id}" data-interval="{data_interval}">
# #
# #                     <!-- Carousel Slides / Quotes -->
# #                     <div class="carousel-inner" style="background-color: {background_color};">
# #
# #                       <!-- Quote 1 -->
# #                       <div class="item active">
# #                           <div class="row">
# #                             <div class="col-sm-9">
# #                               <p>Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <small>Someone famous</small>
# #                               <p>1 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>2 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>3 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>4 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>5 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>6 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                               <p>7 Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur,
# #                                  adipisci velit!</p>
# #                             </div>
# #                           </div>
# #                       </div>
# #                       <!-- Quote 2 -->
# #                       <div class="item">
# #                           <div class="row">
# #                             <div class="col-sm-9">
# #                               <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam auctor nec lacus ut
# #                                  tempor. Mauris.</p>
# #                             </div>
# #                           </div>
# #                       </div>
# #                       <!-- Quote 3 -->
# #                       <div class="item">
# #                           <div class="row">
# #                             <div class="col-sm-9">
# #                               <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut rutrum elit in arcu
# #                                  blandit, eget pretium nisl accumsan. Sed ultricies commodo tortor, eu pretium
# #                                  mauris.</p>
# #                             </div>
# #                           </div>
# #                       </div>
# #                     </div>
# #
# #                     <!-- Carousel Buttons Next/Prev -->
# #                     <a data-slide="prev" href="#{carousel_id}" class="left carousel-control">
# #                         <i class="fa fa-chevron-left"></i>
# #                     </a>
# #                     <a data-slide="next" href="#{carousel_id}" class="right carousel-control">
# #                         <i class="fa fa-chevron-right"></i>
# #                     </a>
# #
# #
# #                   </div>
# #             """
# #         # todo 1: finish this
# #         t_jsf = """
# #                     <!-- Controls buttons -->
# #                     <div style="text-align:center;">
# #                       <input type="button" class="btn start-slide" value="Start">
# #                       <input type="button" class="btn pause-slide" value="Pause">
# #                       <input type="button" class="btn prev-slide" value="Previous Slide">
# #                       <input type="button" class="btn next-slide" value="Next Slide">
# #                       <input type="button" class="btn slide-one" value="Slide 1">
# #                       <input type="button" class="btn slide-two" value="Slide 2">
# #                       <input type="button" class="btn slide-three" value="Slide 3">
# #                     </div>
# #                   <script>
# #                      $(function(){
# #                         // Initializes the carousel
# #                         $(".start-slide").click(function(){
# #                            $("#{carousel_id}").carousel('cycle');
# #                         });
# #                         // Stops the carousel
# #                         $(".pause-slide").click(function(){
# #                            $("#{carousel_id}").carousel('pause');
# #                         });
# #                         // Cycles to the previous item
# #                         $(".prev-slide").click(function(){
# #                            $("#{carousel_id}").carousel('prev');
# #                         });
# #                         // Cycles to the next item
# #                         $(".next-slide").click(function(){
# #                            $("#{carousel_id}").carousel('next');
# #                         });
# #                         // Cycles the carousel to a particular frame
# #                         $(".slide-one").click(function(){
# #                            $("#{carousel_id}").carousel(0);
# #                         });
# #                         $(".slide-two").click(function(){
# #                            $("#{carousel_id}").carousel(1);
# #                         });
# #                         $(".slide-three").click(function(){
# #                            $("#{carousel_id}").carousel(2);
# #                         });
# #                      });
# #                   </script>
# #                 """
# #         out = out.format(carousel_id=self.id,
# #                          data_interval=self.data_interval,
# #                          background_color=self.background_color)
# #         # out += t_jsf.replace('{carousel_id}', self.id)
# #         return out



# todo 1: add dropdowns support http://getbootstrap.com/components/#dropdowns
# todo 1: add button group support http://getbootstrap.com/components/#btn-groups
# todo 1: add Button groups
# todo 1: add Button dropdowns
# todo 1: add Input groups
# todo 1: add Navs
# todo 1: add Navbar
# todo 1: add Breadcrumbs
# todo 1: add Pagination
# todo 1: add Labels
# todo 1: add Badges
# todo 1: add Jumbotron
# todo 1: add Page header
# todo 1: add Thumbnails
# todo 1: add Alerts
# todo 1: add Progress bars
# todo 1: add Media object
# todo 1: add List group
# todo 1: add Panels (need to finish)
# todo 1: add Responsive embed
# todo 1: add Wells
# todo 1: add Modal
# todo 1: add Dropdown
# todo 1: add Scrollspy
# todo 1: add Tab
# todo 1: add Tooltip
# todo 1: add Popover
# todo 1: add Alert
# todo 1: add Button
# todo 1: add Collapse
# todo 1: add Carousel
# todo 1: add Affix
# todo 1: add Grid system
# todo 1: add Typography
# todo 1: add Code
# todo 1: add Tables
# todo 1: add Forms
# todo 1: add Buttons
# todo 1: add Options
# todo 1: add Sizes
# todo 1: add Active state
# todo 1: add Disabled state
# todo 1: add Button tags
# todo 1: add Images
