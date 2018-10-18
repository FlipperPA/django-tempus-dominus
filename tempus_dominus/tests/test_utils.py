from django.conf import settings
from django.test import TestCase

from cybersource_hosted_checkout.utils import create_sha256_signature, sign_fields_to_context


class UtilTests(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sha256_signature(self):
        key = settings.CYBERSOURCE_SECRET_KEY
        message = 'key1=value1,key2=value2,key3=value3'

        response = create_sha256_signature(key, message)

        self.assertEqual(response, 'A8ew8SEYdgbyeiiQBWFYHsW1pcAAZFroS331gMDzBaI=')

    def test_sign_fields(self):
        context = {
            'contextkey1': 'contextvalue1',
        }

        fields = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3',
        }

        response = sign_fields_to_context(fields, context)

        self.assertEqual(
            response['contextkey1'],
            'contextvalue1',
        )
        self.assertEqual(
            response['fields']['key1'],
            'value1',
        )
        self.assertEqual(
            response['fields']['signed_field_names'],
            'key1,key2,key3,signed_date_time,unsigned_field_names,signed_field_names',
        )
        self.assertEqual(
            response['url'],
            'https://testsecureacceptance.cybersource.com/pay',
        )
