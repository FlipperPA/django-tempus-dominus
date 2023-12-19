from django import urls
from django.conf import settings
from django.views.generic import FormView

from .forms import MinMaxDateFieldForm, TimeFieldForm, DateTimeFieldForm

SECRET_KEY = "tests"
DEBUG = True
ALLOWED_HOSTS = ["*"]

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [__file__.replace("settings.py", "templates")],
    "APP_DIRS": True
}]

INSTALLED_APPS = settings.INSTALLED_APPS + ["tempus_dominus"]

ROOT_URLCONF = __name__


class DateFieldTestView(FormView):
    template_name = "test.html"
    form_class = MinMaxDateFieldForm
    success_url = ""


class TimeFieldTestView(FormView):
    template_name = "test.html"
    form_class = TimeFieldForm
    success_url = ""


class DateTimeFieldTestView(FormView):
    template_name = "test.html"
    form_class = DateTimeFieldForm
    success_url = ""


urlpatterns = [
    urls.path("", DateFieldTestView.as_view()),
    urls.path("t/", TimeFieldTestView.as_view()),
    urls.path("dt/", DateTimeFieldTestView.as_view()),
]
