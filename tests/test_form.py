import pytest

from .forms import DateFieldForm, TimeFieldForm, DateTimeFieldForm



@pytest.mark.parametrize("form_class", [
    DateFieldForm,
    TimeFieldForm,
    DateTimeFieldForm,
])
def test_forms_render(form_class):
    """
    Smoke test that forms render
    """
    assert form_class().as_p()
