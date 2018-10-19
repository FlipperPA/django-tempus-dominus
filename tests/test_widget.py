import pytest

from tempus_dominus import widgets


def test_datepicker_format_localized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    widget = widgets.DatePicker()
    assert widget.get_js_format() == 'L'


def test_datepicker_format_nonlocalized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = False
    widget = widgets.DatePicker()
    assert widget.get_js_format() == 'YYYY-MM-DD'


def test_timepicker_format_localized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    widget = widgets.TimePicker()
    assert widget.get_js_format() == 'LTS'


def test_timepicker_format_nonlocalized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = False
    widget = widgets.TimePicker()
    assert widget.get_js_format() == 'HH:mm:ss'


def test_datetimepicker_format_localized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = True
    widget = widgets.DateTimePicker()
    assert widget.get_js_format() == 'L LTS'


def test_datetimepicker_format_nonlocalized(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = False
    widget = widgets.DateTimePicker()
    assert widget.get_js_format() == 'YYYY-MM-DD HH:mm:ss'


def test_get_js_format_error():
    with pytest.raises(NotImplementedError):
        widgets.TempusDominusMixin().get_js_format()


def test_widget_render(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = False
    widget = widgets.DatePicker()
    output = widget.render('inputname', '2018-01-01', attrs={'id': 'myid'})
    input_element = '<input type="text" name="inputname" data-toggle="datetimepicker" data-target="#myid" id="myid">'
    jquery_call = "$('#myid').datetimepicker({'format': 'YYYY-MM-DD', 'defaultDate': '2018-01-01T00:00:00'});"
    assert input_element in output
    assert jquery_call in output


def test_uparsable_date_doesnt_include_default_value(settings):
    settings.TEMPUS_DOMINUS_LOCALIZE = False
    widget = widgets.DateTimePicker()
    output = widget.render('inputname', 'invalid-date', attrs={'id': 'myid'})
    assert 'defaultDate' not in output
