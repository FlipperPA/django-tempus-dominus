import pytest

from .forms import DateFieldForm, TimeFieldForm, DateTimeFieldForm, MinMaxDateFieldForm


@pytest.mark.parametrize("form_class", [
    DateFieldForm,
    TimeFieldForm,
    DateTimeFieldForm,
    MinMaxDateFieldForm,
])
def test_forms_render(form_class):
    """
    Smoke test that forms render
    """
    assert form_class().as_p()


def test_render_moment_localized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    form = DateFieldForm()
    assert form.as_p()
