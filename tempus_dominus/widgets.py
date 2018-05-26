from json import dumps as json_dumps

from django.forms.widgets import DateInput, DateTimeInput, TimeInput
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


class TempusDominusMixin(object):
    class Media:
        css = {
            'all': (
                '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha18/css/tempusdominus-bootstrap-4.min.css',
            ),
        }
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.0/moment.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha18/js/tempusdominus-bootstrap-4.min.js',
        )

    html_template = """
        <input type="{type}" name="{name}"{value}{attrs} data-toggle="datetimepicker" class="datetimepicker-input form-control" data-target="#{picker_id}" id="{picker_id}">
        <script type="text/javascript">
            $(function () {{
                $('#{picker_id}').datetimepicker({js_options});
            }});
        </script>
    """

    def __init__(self, attrs=None, options=None):
        super().__init__(attrs)
        # If a dictionary of options is passed, combine it with our pre-set js_options.
        if type(options) is dict:
            self.js_options = {**self.js_options, **options}

    def render(self, name, value, attrs=None, options=None):
        context = super().get_context(name, value, attrs)

        attr_html = ''
        for attr_key, attr_value in self.attrs.items():
            attr_html += ' {key}="{value}"'.format(
                key=attr_key,
                value=attr_value,
            )

        value_html = ''
        if context['widget']['value'] is not None:
            value_html = ' value="{}"'.format(context['widget']['value'])
            self.js_options['date'] = context['widget']['value']

        field_html = self.html_template.format(
            type=context['widget']['type'],
            picker_id=context['widget']['attrs']['id'],
            name=context['widget']['name'],
            value=value_html,
            attrs=attr_html,
            js_options=json_dumps(self.js_options),
        )

        return mark_safe(force_text(field_html))


class DatePicker(TempusDominusMixin, DateInput):
    js_options = {
        'format': 'YYYY-MM-DD',
        'autoclose': True,
    }


class DateTimePicker(TempusDominusMixin, DateTimeInput):
    js_options = {
        'format': 'YYYY-MM-DD HH:mm:ss',
    }


class TimePicker(TempusDominusMixin, TimeInput):
    js_options = {
        'format': 'HH:mm:ss',
    }
