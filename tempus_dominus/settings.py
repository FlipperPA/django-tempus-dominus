from django.conf import settings

TEMPUS_DOMINUS_VERSION = getattr(settings, "TEMPUS_DOMINUS_VERSION", "6.7.16")

TEMPUS_DOMINUS_INCLUDE_ASSETS = getattr(settings, "TEMPUS_DOMINUS_INCLUDE_ASSETS", True)

TEMPUS_DOMINUS_LOCALIZE = getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False)

TEMPUS_DOMINUS_DATE_FORMAT = getattr(
    settings, "TEMPUS_DOMINUS_DATE_FORMAT", "yyyy-MM-dd"
)

TEMPUS_DOMINUS_DATETIME_FORMAT = getattr(
    settings, "TEMPUS_DOMINUS_DATETIME_FORMAT", "yyyy-MM-dd HH:mm:ss"
)

TEMPUS_DOMINUS_TIME_FORMAT = getattr(settings, "TEMPUS_DOMINUS_TIME_FORMAT", "HH:mm:ss")

TEMPUS_DOMINUS_CSS = getattr(
    settings,
    "TEMPUS_DOMINUS_CSS",
    {
        "all": [
            f"//cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@{TEMPUS_DOMINUS_VERSION}"
            "/dist/css/tempus-dominus.min.css",
        ]
    },
)

TEMPUS_DOMINUS_JS = getattr(
    settings,
    "TEMPUS_DOMINUS_JS",
    [
        "//cdnjs.cloudflare.com/ajax/libs/moment.js/2.22.2/{moment}.min.js".format(
            moment="moment-with-locales" if TEMPUS_DOMINUS_LOCALIZE else "moment"
        ),
        "//cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js",
        f"//cdn.jsdelivr.net/npm/@eonasdan/tempus-dominus@{TEMPUS_DOMINUS_VERSION}"
        "/dist/js/tempus-dominus.min.js",
    ],
)

TEMPUS_DOMINUS_ICON_PACK = getattr(settings, "TEMPUS_DOMINUS_ICON_PACK", "fa_five")
