import json
from datetime import datetime

from django import forms
from django.utils.formats import get_format
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from tempus_dominus.settings import (
    TEMPUS_DOMINUS_LOCALIZE,
    TEMPUS_DOMINUS_INCLUDE_ASSETS,
    TEMPUS_DOMINUS_DATE_FORMAT,
    TEMPUS_DOMINUS_DATETIME_FORMAT,
    TEMPUS_DOMINUS_TIME_FORMAT,
    TEMPUS_DOMINUS_CSS,
    TEMPUS_DOMINUS_JS,
    TEMPUS_DOMINUS_VERSION,
    TEMPUS_DOMINUS_ICON_PACK,
)
from tempus_dominus.utils import OptionsEncoder


def cdn_media():
    """
    Returns the CDN locations for Tempus Dominus, included by default.
    """
    css = {
        "all": [
            f"//cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@{TEMPUS_DOMINUS_VERSION}"
            "/dist/css/tempus-dominus.min.css",
        ]
    }

    if TEMPUS_DOMINUS_LOCALIZE:
        moment = "moment-with-locales"
    else:
        moment = "moment"

    js = [
        "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/"
        "{moment}.min.js".format(moment=moment),
        "//cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js",
        f"//cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@{TEMPUS_DOMINUS_VERSION}"
        "/dist/js/tempus-dominus.min.js",
    ]

    return forms.Media(css=css, js=js)


class TempusDominusMixin:
    """
    The Tempus Dominus Mixin contains shared functionality for the three types of date
    pickers offered.
    """

    ICON_PACKS = {
        "fa_five": {
            "type": "icons",
            "time": "fas fa-clock",
            "date": "fas fa-calendar",
            "up": "fas fa-arrow-up",
            "down": "fas fa-arrow-down",
            "previous": "fas fa-chevron-left",
            "next": "fas fa-chevron-right",
            "today": "fas fa-calendar-check",
            "clear": "fas fa-trash",
            "close": "fas fa-times",
        },
        "ti_two": {
            "type": "icons",
            "time": "ti ti-clock",
            "date": "ti ti-calendar",
            "up": "ti ti-arrow-up",
            "down": "ti ti-arrow-down",
            "previous": "ti ti-chevron-left",
            "next": "ti ti-chevron-right",
            "today": "ti ti-calendar-check",
            "clear": "ti ti-trash",
            "close": "ti ti-square-x",
        },
        "bi_one": {
            "type": "icons",
            "time": "bi bi-clock",
            "date": "bi bi-calendar-week",
            "up": "bi bi-arrow-up",
            "down": "bi bi-arrow-down",
            "previous": "bi bi-chevron-left",
            "next": "bi bi-chevron-right",
            "today": "bi bi-calendar-check",
            "clear": "bi bi-trash",
            "close": "bi bi-x",
        },
    }
    template_name = "tempus_dominus/widget.html"

    def __init__(self, attrs=None, options=None, format=None):
        super().__init__()

        # Set default options to include a clock item, otherwise datetimepicker
        # shows no icon to switch into time mode
        # cdchen-20231107: Change to 6.x options.
        self.js_options = {
            "localization": {
                # "locale": get_language(),
                "format": self.get_js_format(),
            },
            "display": {
                "icons": self.ICON_PACKS.get(
                    TEMPUS_DOMINUS_ICON_PACK,
                    {
                        "type": "icons",
                        "time": "fa-solid fa-clock",
                        "date": "fa-solid fa-calendar",
                        "up": "fa-solid fa-arrow-up",
                        "down": "fa-solid fa-arrow-down",
                        "previous": "fa-solid fa-chevron-left",
                        "next": "fa-solid fa-chevron-right",
                        "today": "fa-solid fa-calendar-check",
                        "clear": "fa-solid fa-trash",
                        "close": "fa-solid fa-xmark",
                    },
                ),
            },
        }
        display_components = self.get_display_components()
        if display_components:
            self.js_options["display"]["components"] = display_components

        # If a dictionary of options is passed, combine it with our pre-set js_options.
        if isinstance(options, dict):
            self.js_options = {**self.js_options, **options}
        # save any additional attributes that the user defined in self
        self.attrs = attrs or {}
        self.format = format or None

    @property
    def media(self):
        if TEMPUS_DOMINUS_INCLUDE_ASSETS:
            return cdn_media()
        return forms.Media(css=TEMPUS_DOMINUS_CSS, js=TEMPUS_DOMINUS_JS)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        widget = context.get("widget", {})

        # self.attrs = user-defined attributes from __init__
        # attrs = attributes added for rendering.
        # context['attrs'] contains a merge of self.attrs and attrs
        # NB If crispy forms is used, it will already contain
        # 'class': 'datepicker form-control'
        # for DatePicker widget

        all_attrs = widget["attrs"]
        all_attrs["id"] = all_attrs["id"].replace("-", "_")
        cls = all_attrs.get("class", "")
        if "form-control" not in cls:
            cls = "form-control " + cls

        # Add the attribute that makes datepicker popup close when focus is lost
        cls += " datetimepicker-input"
        all_attrs["class"] = cls

        # defaults for our widget attributes
        input_toggle = True
        icon_toggle = True
        input_group = True
        append = ""
        prepend = ""
        size = ""

        attr_html = ""
        for attr_key, attr_value in all_attrs.items():
            if attr_key == "prepend":
                prepend = attr_value
            elif attr_key == "append":
                append = attr_value
            elif attr_key == "input_toggle":
                input_toggle = attr_value
            elif attr_key == "input_group":
                input_group = attr_value
            elif attr_key == "icon_toggle":
                icon_toggle = attr_value
            elif attr_key == "size":
                size = attr_value
            elif attr_key == "icon_toggle":
                icon_toggle = attr_value
            else:
                attr_html += ' {key}="{value}"'.format(key=attr_key, value=attr_value)

        options = {}
        options.update(self.js_options)

        if TEMPUS_DOMINUS_LOCALIZE and "locale" not in self.js_options:
            options["locale"] = get_language()

        if widget["value"] is not None:
            # Append an option to set the datepicker's value using a Javascript
            # moment object
            options.update(self.moment_option(value))

        widget.update(
            {
                "picker_id": widget["attrs"]["id"].replace("-", "_"),
                "html_attrs": mark_safe(attr_html),
                "x_value": value,
                "js_options": mark_safe(json.dumps(options, cls=OptionsEncoder)),
                "prepend": prepend,
                "append": append,
                "icon_toggle": icon_toggle,
                "input_toggle": input_toggle,
                "input_group": input_group,
                "size": size,
            }
        )
        return context

    def moment_option(self, value):
        """
        Returns an option dict to set the default date and/or time using a Javascript
        moment object. When a form is first instantiated, value is a date, time or
        datetime object, but after a form has been submitted with an error and
        re-rendered, value contains a formatted string that we need to parse back to a
        date, time or datetime object.
        """
        if isinstance(value, str):
            if isinstance(self, DatePicker):
                formats = (
                    [self.format] if self.format else get_format("DATE_INPUT_FORMATS")
                )
            elif isinstance(self, TimePicker):
                formats = (
                    [self.format] if self.format else get_format("TIME_INPUT_FORMATS")
                )
            else:
                formats = (
                    [self.format]
                    if self.format
                    else get_format("DATETIME_INPUT_FORMATS")
                )
            for fmt in formats:
                try:
                    value = datetime.strptime(value, fmt)
                    if isinstance(self, TimePicker):
                        # strptime returns a date; get the time from it.
                        value = value.time()
                    break
                except (ValueError, TypeError):
                    continue
            else:
                return {}

        # Append an option to set the datepicker's value using iso formatted string
        iso_date = value.isoformat()

        # iso format for time requires a prepended T
        if isinstance(self, TimePicker):
            iso_date = "T" + iso_date

        # cdchen-20231107: Change to 6.x options
        return {"defaultDate": iso_date}

    def get_display_components(self):
        raise NotImplementedError()

    def get_js_format(self):
        raise NotImplementedError


class DatePicker(TempusDominusMixin, forms.widgets.DateInput):
    """
    Widget for Tempus Dominus DatePicker.
    """

    def get_display_components(self):
        return {
            "decades": False,
            "year": True,
            "month": True,
            "date": True,
            "hours": False,
            "minutes": False,
            "seconds": False,
        }

    def get_js_format(self):
        if TEMPUS_DOMINUS_LOCALIZE:
            js_format = "L"
        else:
            js_format = TEMPUS_DOMINUS_DATE_FORMAT
        return js_format


class DateTimePicker(TempusDominusMixin, forms.widgets.DateTimeInput):
    """
    Widget for Tempus Dominus DateTimePicker.
    """

    def get_display_components(self):
        return {}

    def get_js_format(self):
        if TEMPUS_DOMINUS_LOCALIZE:
            js_format = "L LTS"
        else:
            js_format = TEMPUS_DOMINUS_DATETIME_FORMAT
        return js_format


class TimePicker(TempusDominusMixin, forms.widgets.TimeInput):
    """
    Widget for Tempus Dominus TimePicker.
    """

    def get_display_components(self):
        return {
            "decades": False,
            "year": False,
            "month": False,
            "date": False,
            "hours": True,
            "minutes": True,
            "seconds": True,
        }

    def get_js_format(self):
        if TEMPUS_DOMINUS_LOCALIZE:
            js_format = "LTS"
        else:
            js_format = TEMPUS_DOMINUS_TIME_FORMAT
        return js_format
