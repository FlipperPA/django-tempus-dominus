from django.test import override_settings
from django.conf import settings

settings.configure({
    'TEMPUS_DOMINUS_LOCALIZE': False,
})

from .forms import DateFieldForm, TimeFieldForm, DateTimeFieldForm


@override_settings(
    USE_L10N=False,
    USE_I18N=False,
    DATE_INPUT_FORMATS=[
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
        '%b %d %Y',
        '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
        '%d %b %Y',
        '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
        '%B %d %Y',
        '%B %d, %Y',  # 'October 25 2006', 'October 25, 2006'
        '%d %B %Y',
        '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
    ],
    FORM_RENDERER='django.forms.renderers.DjangoTemplates')
def test_date_field_form():
    """
    Test to see ...
    """
    form = DateFieldForm()
    import pdb
    pdb.set_trace()
    # from IPython import embed
    # embed()
