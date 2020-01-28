from rest_framework.test import RequestsClient
from django.test import TestCase


class PrinciplesTests(TestCase):
    def test_principles_are_ok(self):
        client = RequestsClient()
        response = client.get('/principles/')
        self.assertIs(response.status_code, 200)
