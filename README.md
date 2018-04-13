# Django Tempus Dominus

Django Tempus Dominus provides Django widgets for the [Tempus Dominus Bootstrap 4 DateTime](https://tempusdominus.github.io/bootstrap-4/ "Tempus Dominus") date and time picker. Why yet another date and time picker for Django? None supported the Tempus Dominus date and time picker, which is actively developed and feature rich. It is a successor to the popular `bootstrap-datetimepicker` JavaScript library.

## Installation

* From PyPI: `pip install django-tempus-dominus`

* From source:

```python
git clone git+https://github.com/FlipperPA/django-tempus-dominus.git
pip install -e django-tempus-dominus
```

## Usage

Three widgets are provided, `DatePicker`, `DateTimePicker`, and `TimePicker`.

```python
    from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
    date_field = forms.DateField(
        required=True,
        widget=DatePicker(options={'asdf': '1234'}),
    )
    time_field = forms.TimeField(
        required=True,
        widget=TimePicker(options={'asdf': '1234'}),
    )
    datetime_field = forms.TimeField(
        required=True,
        widget=DateTimePicker(options={'asdf': '1234'}),
    )
```

## Maintainer

* Timothy Allen (https://github.com/FlipperPA)
