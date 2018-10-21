from datetime import datetime

from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.formats import get_format
from django.utils.translation import get_language
from django.conf import settings
from django.template.loader import render_to_string


def cdn_media():
    css = {
        'all': (
            '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.1/css/tempusdominus-bootstrap-4.min.css',
        ),
    }

    if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
        moment = "moment-with-locales"
    else:
        moment = "moment"

    js = (
        ('//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/'
         '{moment}.min.js'.format(moment=moment)),
        ('//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/'
         '5.0.1/js/tempusdominus-bootstrap-4.min.js'),
    )

    return forms.Media(css=css, js=js)


class TempusDominusMixin:

    def __init__(self, attrs={'class': 'form-control datetimepicker-input'}, options=None):
        super().__init__()

        # If a dictionary of options is passed, combine it with our pre-set js_options.
        self.js_options = {'format': self.get_js_format()}

        if isinstance(options, dict):
            self.js_options = {**self.js_options, **options}

    @property
    def media(self):
        if getattr(settings, 'TEMPUS_DOMINUS_INCLUDE_ASSESTS', True):
            return cdn_media()

    def render(self, name, value, attrs={}, renderer=None):
        context = super().get_context(name, value, attrs)

        attr_html = ''
        for attr_key, attr_value in self.attrs.items():
            attr_html += ' {key}="{value}"'.format(
                key=attr_key,
                value=attr_value,
            )
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False) and 'locale' not in self.js_options:
            self.js_options['locale'] = get_language()

        options = {}
        options.update(self.js_options)
        if context['widget']['value'] is not None:
            # Append an option to set the datepicker's value using a Javascript moment object
            options.update(self.moment_option(value))

        field_html = render_to_string('tempus_dominus/widget.html', {
            'type': context['widget']['type'],
            'picker_id': context['widget']['attrs']['id'],
            'name': context['widget']['name'],
            'attrs': mark_safe(attr_html),
            'js_options': mark_safe(options),
        })

        return mark_safe(force_text(field_html))

    def moment_option(self, value):
        """
        Returns an option dict to set the default date and/or time using a Javascript moment object.
        When a form is first instantiated, value is a date, time or datetime object,
        but after a form has been submitted with an error and re-rendered, value contains a formatted string that
        we need to parse back to a date, time or datetime object.

        """
        if isinstance(value, str):
            if isinstance(self, DatePicker):
                formats = 'DATE_INPUT_FORMATS'
            elif isinstance(self, TimePicker):
                formats = 'TIME_INPUT_FORMATS'
            else:
                formats = 'DATETIME_INPUT_FORMATS'
            for format in get_format(formats):
                try:
                    value = datetime.strptime(value, format)
                    break
                except (ValueError, TypeError):
                    continue
            else:
                return {}

        return {'defaultDate': value.isoformat()}

    def get_js_format(self):
        raise NotImplementedError


class DatePicker(TempusDominusMixin, forms.widgets.DateInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'L'
        else:
            js_format = 'YYYY-MM-DD'
        return js_format


class DateTimePicker(TempusDominusMixin, forms.widgets.DateTimeInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'L LTS'
        else:
            js_format = 'YYYY-MM-DD HH:mm:ss'
        return js_format


class TimePicker(TempusDominusMixin, forms.widgets.TimeInput):
    def get_js_format(self):
        if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
            js_format = 'LTS'
        else:
            js_format = 'HH:mm:ss'
        return js_format
