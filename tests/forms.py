from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class DateFieldForm(forms.Form):
    """Test form for DatePicker widget."""
    date_field = forms.DateField(widget=DatePicker())


class TimeFieldForm(forms.Form):
    """Test form for TimePicker widget."""
    time_field = forms.TimeField(widget=TimePicker())

class DateTimeFieldForm(forms.Form):
    """Test form for DateTimePicker widget."""
    datetime_field = forms.DateTimeField(widget=DateTimePicker)
