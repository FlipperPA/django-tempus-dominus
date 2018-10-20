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
    assert widget.js_options == {'format': 'YYYY-MM-DD HH:mm:ss'}


def test_datetime_form_localization(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    importlib.reload(forms)
    form = forms.DateTimeFieldForm()
    widget = form.fields['datetime_field'].widget
    assert isinstance(
        widget,
        widgets.DateTimePicker
    )
    assert widget.js_options == {'format': 'L LTS'}


def test_form_media():
    """Check that the widget media makes it up to the form"""
    form = forms.DateTimeFieldForm()
    cdn_media = widgets.cdn_media()

    # I'm not a fan of testing private methods but there's no
    # other way to access the css and js members that I could
    # find. Please fix if you find one.
    assert set(form.media._css['all']) == set(cdn_media._css['all'])
    assert set(form.media._js) == set(cdn_media._js)
