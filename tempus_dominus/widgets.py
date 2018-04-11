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
                'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha14/css/tempusdominus-bootstrap-4.min.css',
            ),
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/tempusdominus-bootstrap-4/5.0.0-alpha14/js/tempusdominus-bootstrap-4.min.js',
        )


class DatePicker(DateInput, TempusDominusMixin):
    pass


class DateTimePicker(DateTimeInput, TempusDominusMixin):
    html_template = """
        <div class="form-group">
            <div class="input-group date" id="{picker_id}" data-target-input="nearest">
                <input type="text" class="form-control datetimepicker-input" data-target="#{picker_id}"/>
                <div class="input-group-append" data-target="#{picker_id}" data-toggle="datetimepicker">
                    <div class="input-group-text"><i class="{icon_attrs}"></i></div>
                </div>
            </div>
        </div>
    """

    """

                    <div{div_attrs}>
            <input{input_attrs}>
            <span class="input-group-addon">
                <span{icon_attrs}></span>
            </span>
        </div>
    """

    js_template = """
        <script type="text/javascript">
            $(function () {
                $('#{picker_id}').datetimepicker({options});
            });
        </script>
    """

    '''
        <script>
            (function(window) {
                var callback = function() {
                    $(function(){$("#%(picker_id)s:has(input:not([readonly],[disabled]))").datepicker(%(options)s);});
                };
                if(window.addEventListener)
                    window.addEventListener("load", callback, false);
                else if (window.attachEvent)
                    window.attachEvent("onload", callback);
                else window.onload = callback;
            })(window);
        </script>'''

    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, icon_attrs=None):
        if not icon_attrs:
            icon_attrs = {'class': 'fa fa-calendar'}
        if not div_attrs:
            div_attrs = {'class': 'input-group date'}
        if format is None and options and options.get('format'):
            format = self.conv_datetime_format_js2py(options.get('format'))
        super().__init__(attrs, format)
        if 'class' not in self.attrs:
            self.attrs['class'] = 'form-control'
        self.div_attrs = div_attrs and div_attrs.copy() or {}
        self.icon_attrs = icon_attrs and icon_attrs.copy() or {}
        self.picker_id = self.div_attrs.get('id') or None
        if options is False:  # datepicker will not be initalized when options is False
            self.options = False
        else:
            self.options = options and options.copy() or {}
            if format and not self.options.get('format') and not self.attrs.get('date-format'):
                self.options['format'] = self.conv_datetime_format_py2js(format)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        extra_attrs = dict()
        extra_attrs['type'] = self.input_type
        extra_attrs['name'] = name
        input_attrs = self.build_attrs(attrs, extra_attrs)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            input_attrs['value'] = force_text(self._format_value(value))
        input_attrs = {key: conditional_escape(val) for key, val in input_attrs.items()}
        if not self.picker_id:
            self.picker_id = (input_attrs.get('id', '') + '_pickers').replace(' ', '_')
        self.div_attrs['id'] = self.picker_id
        picker_id = conditional_escape(self.picker_id)
        div_attrs = {key: conditional_escape(val) for key, val in self.div_attrs.items()}
        icon_attrs = {key: conditional_escape(val) for key, val in self.icon_attrs.items()}
        html = self.html_template % dict(div_attrs=flatatt(div_attrs),
                                         input_attrs=flatatt(input_attrs),
                                         icon_attrs=flatatt(icon_attrs))
        if self.options:
            js = self.js_template % dict(picker_id=picker_id, options=json_dumps(self.options or {}))
        else:
            js = ''
        return mark_safe(force_text(html + js))


class TimePicker(TimeInput, TempusDominusMixin):
    pass
