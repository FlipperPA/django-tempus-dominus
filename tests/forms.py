from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class DateFieldForm(forms.Form):
    """Test form for DatePicker widget."""

    date_field = forms.DateField(widget=DatePicker)


class MinMaxDateFieldForm(forms.Form):
    """Test form for DatePicker widget with minDate and maxDate options."""

    date_field = forms.DateField(
        widget=DatePicker(options={"minDate": "2009-01-20", "maxDate": "2017-01-20"})
    )


class TimeFieldForm(forms.Form):
    """Test form for TimePicker widget."""

    time_field = forms.TimeField(widget=TimePicker)


class DateTimeFieldForm(forms.Form):
    """Test form for DateTimePicker widget."""

    datetime_field = forms.DateTimeField(widget=DateTimePicker)


class DateFieldDisabledForm(forms.Form):
    """Test form for disabled DateField widget."""

    date_field_dis = forms.DateField(widget=TimePicker, disabled=True)


class DateFieldNotRequiredForm(forms.Form):
    """Test form for not required DateField widget."""

    date_field_not_req = forms.DateField(widget=TimePicker, required=False)


class DateFieldPrependLargeForm(forms.Form):
    """Test form with prepended icon."""

    date_field = forms.DateField(
        widget=DatePicker(attrs={"prepend": "fa fa-calendar", "size": "large"})
    )


class TimeFieldAppendSmallForm(forms.Form):
    """Test form with appended icon. """

    time_field = forms.TimeField(
        widget=DatePicker(attrs={"append": "fa fa-clock", "size": "small"})
    )


class DateTimeFieldNoToggleForm(forms.Form):
    """Test form without a toggle"""

    datetime_field = forms.DateTimeField(
        widget=DatePicker(attrs={"icon_toggle": False, "input_toggle": False})
    )
