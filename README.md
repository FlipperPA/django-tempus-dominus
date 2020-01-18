# Django Tempus Dominus

## DEPRECATION NOTICE: Final Release

**A Note About the Future of This Package**

The parent project to this package, Tempus Dominus, is no longer receiving updates. The maintainer of Tempus Dominus put in a lot of work - thank you! - but doesn't have the cycles to continue maintaining it further. My colleagues and I need a robust date and time picker for our full time jobs, so we'll be looking for a good, accessible Bootstrap 4 solution over the next few months. When we've found the one we are going to use, we'll build another Django shim package similar to this one.

Unless something changes with the future of Tempus Domnius, version `5.1.2.13` will be the final release of Django Tempus Dominus, which includes support for Django 3.0.

Django Tempus Dominus provided Django widgets for the [Tempus Dominus Bootstrap 4 DateTime](https://tempusdominus.github.io/bootstrap-4/ "Tempus Dominus") date and time picker.

## Installation

* From PyPI: `pip install django-tempus-dominus`

Then add `tempus_dominus` to `INSTALLED_APPS` in your Django settings.

## Usage & Django Settings

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
            },
        ),
        initial='2013-01-01',
    )
    """
    In this example, the date portion of `defaultDate` is irrelevant;
    only the time portion is used. The reason for this is that it has
    to be passed in a valid MomentJS format. This will default the time
    to be 14:56:00 (or 2:56pm).
    """
    time_field = forms.TimeField(
        widget=TimePicker(
            options={
                'enabledHours': [9, 10, 11, 12, 13, 14, 15, 16],
                'defaultDate': '1970-01-01T14:56:00'
            },
            attrs={
                'input_toggle': True,
                'input_group': False,
            },
        ),
    )
    datetime_field = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            }
        ),
    )
```

Then in your template, include jQuery, `{{ form.media }}`, and render the form:

```HTML+Django
<html>
  <head>
    {# Include FontAwesome; required for icon display #}
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.css">

    {# Include Bootstrap 4 and jQuery #}
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>

    {# Django Tempus Dominus assets are included in `{{ form.media }}` #}
    {{ form.media }}
  </head>
  
  <body>
    <div class="container">
      <div class="row">
        <div class="col">
          <form method="post" action=".">
            {% csrf_token %}
            {{ form.as_p }}
          </form>
        </div>
      </div>
    </div>
  </body>
</html>
```

## Widget Options

* `options` (dictionary): This dictionary will be passed to Tempus Dominus. [A full list of options is available here](https://tempusdominus.github.io/bootstrap-4/Options/).
* `input_toggle` (boolean, default `True`): Controls whether clicking on the input field toggles the datepicker popup. Typically is set to False when an icon is in use.
* `input_group` (boolean, default `True`): Whether to include a Bootstrap 4 `input-group` around the picker.
* `size` (string): Controls the size of the input group (`small` or `large`). Defaults to the default size.
* `prepend` (string): Name of a Font Awesome icon to prepend to the input field (`fa fa-calendar`).
* `append` (string): Name of a Font Awesome icon to append to the input field (`fa fa-calendar`).
* `icon_toggle` (boolean, default `True`): Controls whether clicking on the icon toggles the datepicker popup. Typically is set to False when an icon is in use.

## Change Log

* 5.1.2.13: Add deprecation notice to README.
* 5.1.2.12: Fix issues with initial values not showing up in TimePicker.
* 5.1.2.11: Fix deprecations introduced in Django 3.0 (`force_text` -> `force_str`).
* 5.1.2.9: Include JS assets from the parent form if `TEMPUS_DOMINUS_INCLUDE_ASSETS` is `False`. Switch to using `setuptools-scm` instead of `MANIFEST.in`.
* 5.1.2.7 / 5.1.2.8: Bug fix: if a field had a hyphen in the `id`, this would cause an error in the JS function. Force hyphens to underscores.
* 5.1.2.6: Include a defer function to play more nicely with different jQuery configurations.
* 5.1.2.5: Typo bug in INCLUDE_ASSETS; switch to Black code formatting.
* 5.1.2.4: Add support for disabling the Bootstrap `input-group` with a new option. Fix an icon.
* 5.1.2.3: Fix a bug which caused a page lag when switching locales.
* 5.1.2.2: Fix a bug with duplicate DOM IDs in template.
* 5.1.2.1: Fix a bug with time formatting to use ISO time format (`T12:34:56`)
* 5.1.2.0: Upgrade Tempus Dominus to 5.1.2. Support for new widget attributes (size, prepend, append, input_toggle, icon_toggle, class). DatePicker now closes after losing focus, and widget attributes are properly passed.
* 5.0.1.5: Fix to ensure options are passed in proper JSON.
* 5.0.1.4: Include template in the MANIFEST.in file.
* 5.0.1.3: Add setting to exclude CDN CSS and JS assets. Add initial test suite.
* 5.0.1.2: Documentation clean up.
* 5.0.1.1: Option to use l10n and i18n to all pickers.
* 5.0.1.0: Upgrade to Tempus Dominus full release version `5.0.1`. Fix bug for populating initial values.
* 0.1.2: UX enhancement: auto-dismiss dialog if the input loses focus.
* 0.1.1: Bug fixes.
* 0.1.0: Initial release.

## Maintainers

* Timothy Allen (https://github.com/FlipperPA)
* Ian Stewart (https://github.com/ianastewart)

This package is largely maintained by the staff of [Wharton Research Data Services](https://wrds.wharton.upenn.edu/). We are thrilled that [The Wharton School](https://www.wharton.upenn.edu/) allows us a certain amount of time to contribute to open-source projects. We add features as they are necessary for our projects, and try to keep up with Issues and Pull Requests as best we can. Due to time constraints (our full time jobs!), Feature Requests without a Pull Request may not be implemented, but we are always open to new ideas and grateful for contributions and our package users.

### Contributors & DjangoCon US Sprinters (Thank You!)

* Stéphane "Twidi" Angel (https://github.com/twidi)
* Jake Bell (https://github.com/theunraveler)
* Bartłomiej Biernacki (https://github.com/pax0r)
* John Carroll (https://github.com/johnnyporkchops)
* Bryan Collazo (https://github.com/bcollazo)
* Katherine Dey (https://github.com/deyspring)
* Tiffany Huang (https://github.com/tiff8433)
* Václav 'ax' Hůla (https://github.com/AxTheB)
* Adam Johnson (https://github.com/adamchainz)
* Manuel Kappler (https://github.com/manuelkappler)
* Kenneth Love (https://github.com/kennethlove)
* Donna St. Louis (https://github.com/dcstlouis)
* Ryan Sullivan (https://github.com/rgs258)
* Kevan Swanberg (https://github.com/kevswanberg)
* Nick Träger (https://github.com/nick-traeger)
* waymou (https://github.com/waymao)
