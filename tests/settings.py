from django.conf import settings

SECRET_KEY = "tests"
TEMPUS_DOMINUS_LOCALIZE = False

TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}
]

INSTALLED_APPS = settings.INSTALLED_APPS + ["tempus_dominus"]
