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

Three widgets are provided:

* `DatePicker`, which defaults to `YYYY-MM-DD`
* `DateTimePicker`, which defaults to `YYYY-MM-DD HH:mm:ss`
* `TimePicker`, which defaults to `HH:mm:ss`

In your Django form, you can use the widgets like this:

```python
import datetime

from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class MyForm(forms.Form):
    date_field = forms.DateField(
        required=True,
        widget=DatePicker(
            options={
                'minDate': '2009-01-20',
                'maxDate': '2017-01-20',
            }
        ),
    )
    time_field = forms.TimeField(
        widget=TimePicker(
            options={
                'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
            }
        ),
    )
    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # Tomorrow
                'useCurrent': True,
                'collapse': False,
            }
        ),
    )
```

The `options` dictionary will be passed to Tempus Dominus. [A full list of options is available here](https://tempusdominus.github.io/bootstrap-4/Options/).

Then in your template, include jQuery, `{{ form.media }}`, and render the form:

```HTML+Django
<html>
    <head>
        <script crossorigin="anonymous" integrity="sha384-xBuQ/xzmlsLoJpyjoggmTEz8OWUFM0/RC5BsqQBDX2v5cMvDHcMakNTNrHIW2I5f" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
        {{ form.media }}
    </head>
<body>
    <form method="post" action=".">
        {% csrf_token %}
        {{ form.as_p }}
    </form>
</body>
</html>
```

## Maintainer

* Timothy Allen (https://github.com/FlipperPA)
