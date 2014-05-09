
Miscelaneous Notes
==================

Sample GraphPage Form
---------------------

::

    {% extends "base.html" %}
    {% load graphpage %}
    {% load crispy_forms_tags %}

    {% block content %}
        <div class="container-fluid">
            <div class="row">
                <div class="col-md-6">
                    <h3>This is a form page</h3>
                    <p>It contains one or more forms, like the one below.</p>
                    <p>You can put any explanation text above the form.</p>
                </div>
            </div>

    {% form no_countries %}
    class GraphForm(forms.Form):
        title = forms.CharField(min_length=3, max_length=80, label='Title')
        number_countries = forms.IntegerField(max_value=50, min_value=5,
                                              label='Number of countries')
        helper = FormHelper()
        helper.form_method = 'POST'
        helper.form_action = 'graphpages/graphpage3/{{graph_pk}}'
        helper.add_input(Submit('submit', 'Show graph', css_class='btn-primary'))
    {% endform no_countries %}

            <div class="row">
                <div class="col-md-6">
                   </br>
                   <p>Likewise you can put any instructions or whatever after the form.</p>
                   <p>Forms support django-crispy-forms and bootstrap3!</p>
                </div>
            </div>
        </div>
    {% endblock content %}

Sample GraphPage Page
---------------------
::

    {% extends "base.html" %}
    {% load chartkick %}

    {% query %}
    title1 = 'Top {{number_countries}} countries by land area'
    r = CIA.objects.order_by('-land_area')[:{{number_countries}}]
    data1 = [[o.name, o.land_area] for o in r]

    title2 = 'Top {{number_countries}} countries by population'
    r = CIA.objects.order_by('-population')[:{{number_countries}}]
    data2 = [[o.name, o.population] for o in r]
    {% endquery %}

    {% block content %}
        <div class="container-fluid">
            <div class="jumbotron">
                <h3>Django Graph Pages</h3>
                <p>This template displays two pie charts side by side in a fluid grid.</p>
            </div>
        </div>

        <div class="container-fluid">
            <div class="row">
                <div class="col-md-6">
                    <h3>{{ title1 }}</h3>
                    {% pie_chart data1 with id='chart-1' %}
                    <a class="btn btn-primary" href="javascript:history.back()">Back</a>

                </div>
                <div class="col-md-6">
                    <h3>{{ title2 }}</h3>
                    {% pie_chart data2 with id='chart-2' %}
                    <a class="btn btn-primary" href="javascript:history.back()">Back</a>
                </div>
            </div>
        </div>
    {% endblock content %}


Setting field width in CrispyForms
----------------------------------

I know it should be obvious but I had a hard time sorting this out.  Here's a sample::

    #!/usr/bin/env python
    # coding=utf-8

    """ Some description here

    3/9/14 - Initial creation

    """

    from __future__ import unicode_literals
    import logging

    log = logging.getLogger(__name__)

    __author__ = 'richabel'
    __date__ = '3/9/14'
    __license__ = "All rights reserved"
    __version__ = "0.1"
    __status__ = "dev"


    from django.views.generic import FormView
    from django.forms.extras.widgets import SelectDateWidget
    from django import forms


    ###############################################################################
    #
    # Test crispy forms to make sure it's working
    #
    from crispy_forms.helper import FormHelper
    # noinspection PyUnresolvedReferences
    from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
    from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


    class SimpleForm(forms.Form):
        integer_input = forms.IntegerField(max_value=99, min_value=2,
                                           label='Integer field label(2 to 99)',
                                           initial='30'
        )

        text_input = forms.CharField()

        textarea = forms.CharField(
            widget=forms.Textarea(),
        )

        radio_buttons = forms.ChoiceField(
            choices=(
                ('option_one', "Option one is this and that be sure to include why it's great"),
                ('option_two', "Option two can is something else and selecting it will deselect option one")
            ),
            widget = forms.RadioSelect,
            initial = 'option_two',
        )

        checkboxes = forms.MultipleChoiceField(
            choices=(
                ('option_one', "Option one is this and that be sure to include why it's great"),
                ('option_two', 'Option two can also be checked and included in form results'),
                ('option_three', 'Option three can yes, you guessed it also be checked and included in form results')
            ),
            initial = 'option_one',
            widget = forms.CheckboxSelectMultiple,
            help_text = "<strong>Note:</strong> "
                        "Labels surround all the options for much larger click areas and a more usable form.",
        )

        appended_text = forms.CharField(
            help_text="Here's more help text"
        )

        prepended_text = forms.CharField()

        prepended_text_two = forms.CharField()

        multicolon_select = forms.MultipleChoiceField(
            choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')),
        )

        # Uni-form
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.layout = Layout(
            Field('integer_input', style="width: 20%;"),
            Field('text_input', css_class='input-xlarge'),
            Field('textarea', rows="3", css_class='input-xlarge'),
            'radio_buttons',
            Field('checkboxes', style="background: #FAFAFA; padding: 10px;"),
            AppendedText('appended_text', '.00'),
            PrependedText('prepended_text',
                          '<input type="checkbox" checked="checked" value="" id="" name="">', active=True),
            PrependedText('prepended_text_two', '@'),
            'multicolon_select',
            FormActions(
                Submit('save_changes', 'Save changes', css_class="btn-primary"),
                Submit('cancel', 'Cancel'),
            )
        )


    class CrispyView(FormView):
        template_name = 'crispy.html'
        form_class = SimpleForm

The key is using the helper.layout ans setting style=... as in **integer_input** above.
I tried a number of other approaches but none worked.
