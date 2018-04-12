from json import dumps as json_dumps

from django.forms.utils import flatatt
from django.forms.widgets import DateInput, DateTimeInput, TimeInput
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.utils.encoding import force_text


class TempusDominusMixin(object):
    class Media:
        css = {
            'all': (
                '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha14/css/tempusdominus-bootstrap-4.min.css',
            ),
        }
        js = (
            '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.0/moment.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha14/js/tempusdominus-bootstrap-4.min.js',
        )

    html_template = """
        <input type="{type}" name="{name}"{value}{attrs} data-toggle="datetimepicker" data-target="#{picker_id}" id="{picker_id}">
        <script type="text/javascript">
            $(function () {{
                $('#{picker_id}').datetimepicker({options});
            }});
        </script>
    """

    def render(self, name, value, attrs=None):
        self.attrs['class'] = 'form-control datetimepicker-input'

        from pprint import pprint
        print('SELF')
        pprint(dir(self))

        context = super().get_context(name, value, attrs)

        attr_html = ''
        for attr_key, attr_value in self.attrs.items():
            if attr_key == "class":
                print("CLASS", attr_value)
            attr_html += ' {key}="{value}"'.format(
                key=attr_key,
                value=attr_value,
            )

        value_html = ''
        if context['widget']['value'] is not None:
            value_html = ' value="{}"'.format(context['widget']['value'])
            self.options['date'] = context['widget']['value']

        field_html = self.html_template.format(
            type=context['widget']['type'],
            picker_id=context['widget']['attrs']['id'],
            name=context['widget']['name'],
            value=value_html,
            attrs=attr_html,
            options=json_dumps(self.options),
        )

        print(field_html)
        return mark_safe(field_html)


class DatePicker(TempusDominusMixin, DateInput):
    options = {
        'format': 'YYYY-MM-DD',
    }


class DateTimePicker(TempusDominusMixin, DateTimeInput):
    options = {
        'format': 'YYYY-MM-DD HH:mm:ss',
    }


class TimePicker(TimeInput, TempusDominusMixin):
    pass
