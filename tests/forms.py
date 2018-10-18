from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class DateFieldForm(forms.Form):
    """Test form for DatePicker widget."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_field'] = forms.DateField(widget=DatePicker())


class TimeFieldForm(forms.Form):
    """Test form for TimePicker widget."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_field'] = forms.TimeField(widget=TimePicker())



class DateTimeFieldForm(forms.Form):
    """Test form for DateTimePicker widget."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['datetime_field'] = forms.DateTimeField(widget=DateTimePicker())
