# Django Tempus Dominus

Django Tempus Dominus provides Django widgets for the [Tempus Dominus Bootstrap 4 DateTime](https://tempusdominus.github.io/bootstrap-4/ "Tempus Dominus") date and time picker. Why yet another date and time picker for Django? None supported the Tempus Dominus date and time picker, which is actively developed and feature rich. It is a successor to the popular `bootstrap-datetimepicker` JavaScript library.

## Installation

* From PyPI: `pip install django-tempus-dominus`

* From source:

```python
git clone git+https://github.com/FlipperPA/django-tempus-dominus.git
pip install -e django-tempus-dominus
```

## Usage & Settings

The following settings are available:

* `TEMPUS_DOMINUS_LOCALIZE` (default: `False`): if `True`, widgets will be translated to the selected browser language and use the localized date and time formats.
* `TEMPUS_DOMINUS_INCLUDE_ASSETS` (default: `True`): if `True`, loads Tempus Dominus and `moment` JS and CSS from Cloudflare's CDN, otherwise loading the JS and CSS are up to you.

Three widgets are provided:

* `DatePicker`
    * Defaults to `YYYY-MM-DD`
    * Defaults to `L` if `TEMPUS_DOMINUS_LOCALIZE` is `True`
* `DateTimePicker`
    * Defaults to `YYYY-MM-DD HH:mm:ss`
    * Defaults to `L LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`
* `TimePicker`
    * Defaults to `HH:mm:ss`
    * Defaults to `LTS` if `TEMPUS_DOMINUS_LOCALIZE` is `True`

In your Django form, you can use the widgets like this:

```python
import datetime

from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

class MyForm(forms.Form):
    date_field = forms.DateField(widget=DatePicker())
    date_field_required_with_min_max_date = forms.DateField(
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
                'minDate': (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),  # Tomorrow
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

## Change Log

* 5.0.1.2: Documentation clean up.
* 5.0.1.1: Option to l10n and i18n to all pickers (thank you, @AxTheB).
* 5.0.1.0: Upgrade to Tempus Dominus full release version `5.0.1`. Fix bug for populating initial values (thank you, @ianastewart).
* 0.1.2: UX enhancement: auto-dismiss dialog if the input loses focus.
* 0.1.1: Bug fixes.
* 0.1.0: Initial release.

## Maintainer

* Timothy Allen (https://github.com/FlipperPA)

### Contributors (Thank You!)

* Ian Stewart (https://github.com/ianastewart)
* Jake Bell (https://github.com/theunraveler)
* Václav 'ax' Hůla (https://github.com/AxTheB)
* waymou (https://github.com/waymao)
