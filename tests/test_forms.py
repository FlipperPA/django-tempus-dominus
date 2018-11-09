import importlib

import pytest

from . import forms
from tempus_dominus import widgets



@pytest.mark.parametrize("form_class", [
    forms.DateFieldForm,
    forms.TimeFieldForm,
    forms.DateTimeFieldForm,
])
def test_forms_render(form_class):
    """
    Smoke test that forms render
    """
    assert form_class().as_p()


def test_render_moment_unlocalized(settings):
    form = forms.DateTimeFieldForm()
    widget = form.fields['datetime_field'].widget
    assert isinstance(
        widget,
        widgets.DateTimePicker
    )
    #assert widget.js_options == {'format': 'YYYY-MM-DD HH:mm:ss'}
    assert 'YYYY-MM-DD HH:mm:ss' in widget.js_options['format']

def test_datetime_form_localization(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    importlib.reload(forms)
    form = forms.DateTimeFieldForm()
    widget = form.fields['datetime_field'].widget
    assert isinstance(
        widget,
        widgets.DateTimePicker
    )
    #assert widget.js_options == {'format': 'L LTS'}
    assert 'L LTS' in widget.js_options['format']

def test_form_media():
    """Check that the widget media makes it up to the form"""
    form = forms.DateTimeFieldForm()
    cdn_media = widgets.cdn_media()

    # I'm not a fan of testing private methods but there's no
    # other way to access the css and js members that I could
    # find. Please fix if you find one.
    assert set(form.media._css['all']) == set(cdn_media._css['all'])
    assert set(form.media._js) == set(cdn_media._js)


def test_class_attr_contents():
    output = forms.DateFieldForm().as_p()
    assert 'datetimepicker-input' in output


def test_disabled_in_output():
    output = forms.DateFieldDisabledForm().as_p()
    assert 'disabled' in output


def test_required_not_in_output():
    output = forms.DateFieldNotRequiredForm().as_p()
    assert 'required' not in output


def test_prepend():
    output = forms.DateFieldPrependForm().as_p()
    assert 'prepend' in output
    assert 'fa fa-calendar' in output


def test_append():
    output = forms.TimeFieldAppendForm().as_p()
    assert 'append' in output
    assert 'fa fa-clock' in output


def test_no_toggle():
    output = forms.DateTimeFieldNoToggleForm().as_p()
    assert 'datatoggle' not in output


def test_field_with_value():
    date_value = '2018-11-9'
    form = forms.DateFieldForm()
    form.fields['date_field'].value = date_value
    output = form.as_p()
    assert date_value in output

