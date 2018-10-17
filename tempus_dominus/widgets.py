from datetime import datetime
from json import dumps as json_dumps

from django.forms.widgets import DateInput, DateTimeInput, TimeInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.formats import get_format
from django.utils.translation import get_language
from django.conf import settings


class CDNMedia:
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
        '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/{moment}.min.js'.format(moment=moment),
        '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.1/js/tempusdominus-bootstrap-4.min.js',
    )


class TempusDominusMixin(object):

    if getattr(settings, 'TEMPUS_DOMINUS_INCLUDE_ASSETS', True):
        Media = CDNMedia

    html_template = """
        <input type="{type}" name="{name}"{value}{attrs} data-toggle="datetimepicker" data-target="#{picker_id}" id="{picker_id}">
        <script type="text/javascript">
            $(function () {{
                $('#{picker_id}').datetimepicker({js_options});
            }});
        </script>
    """

    def __init__(self, attrs={'class': 'form-control datetimepicker-input'}, options=None):
        super().__init__(attrs)
        # If a dictionary of options is passed, combine it with our pre-set js_options.
        if type(options) is dict:
            self.js_options = {**self.js_options, **options}

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

        options = json_dumps(self.js_options)
        if context['widget']['value'] is not None:
            # Append an option to set the datepicker's value using a Javascript moment object
            options = options[:-1] + ', %s}' % self.moment_option(value)

        field_html = self.html_template.format(
            type=context['widget']['type'],
            picker_id=context['widget']['attrs']['id'],
            name=context['widget']['name'],
            value='',
            attrs=attr_html,
            js_options=options,
        )

        return mark_safe(force_text(field_html))

    def moment_option(self, value):
        """
        Returns an option string to set the default date and/or time using a Javascript moment object.
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
                return ''
        option = ''
        if isinstance(self, DatePicker) or isinstance(self, DateTimePicker):
            # NB. moment months are zero indexed!
            option = 'year: {}, month: {}, day: {}'.format(value.year, value.month - 1, value.day)
        if isinstance(self, TimePicker) or isinstance(self, DateTimePicker):
            if option:
                option += ', '
            option += 'hour: {}, minute: {}, second: {}'.format(value.hour, value.minute, value.second)
        return 'defaultDate: moment({%s})' % option


class DatePicker(TempusDominusMixin, DateInput):
    if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
        js_format = 'L'
    else:
        js_format = 'YYYY-MM-DD'

    js_options = {
        'format': js_format,
    }


class DateTimePicker(TempusDominusMixin, DateTimeInput):
    if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
        js_format = 'L LTS'
    else:
        js_format = 'YYYY-MM-DD HH:mm:ss'

    js_options = {
        'format': js_format
    }


class TimePicker(TempusDominusMixin, TimeInput):
    if getattr(settings, 'TEMPUS_DOMINUS_LOCALIZE', False):
        js_format = 'LTS'
    else:
        js_format = 'HH:mm:ss'

    js_options = {
        'format': js_format
    }
