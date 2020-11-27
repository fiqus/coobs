import requests
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from django.test import TestCase
from api.models import Cooperative, Partner, Principle
from api.serializers import CooperativeSerializer
from api.views import CooperativeView, views_utils
from unittest.mock import patch
from api.tests.utils import MockResponse

class CooperativeTest(TestCase):
    """ Test module for cooperative """

    list_url = reverse('cooperative-list')

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        self.client.force_authenticate(self.user)

    def test_retrieve_coop(self):
        Cooperative.objects.create(name="coop", business_name="testing coop", is_active=True)
        response = self.client.get(self.list_url)
        cooperatives = Cooperative.objects.all()
        serializer = CooperativeSerializer(cooperatives, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch("api.views.views_utils.create_and_send_email")
    @patch("requests.post", return_value=MockResponse({"success": True}, 200))
    def test_create_coop_successful(self, mock_method, create_and_send_email): 
        payload = {"name":"coop", "businessName":"testing coop", "language": "es", "reCaptchaToken": "test",
            'email': 'test_user@email.com', 'username': "test_user", 'password': 'test_pass', 
            'firstName': 'name', 'lastName': 'lastName'}
        
        self.client.post(self.list_url, payload)
        created_coop = Cooperative.objects.filter(business_name=payload["businessName"])
        created_partner = Partner.objects.filter(email=payload["email"])
        created_principles = Principle.objects.filter(cooperative__id=created_coop[0].id)

        self.assertTrue(created_coop.exists())
        created_coop = created_coop[0]
        self.assertFalse(created_coop.is_active)

        self.assertTrue(created_partner.exists())
        created_partner = created_partner[0]
        self.assertFalse(created_partner.is_active)
        self.assertEqual(created_partner.cooperative.id, created_coop.id)
        #FIXME not working
        # self.assertEqual(create_and_send_email.call_count, 2)
        mock_method.assert_called_once()

# class ActionTest(TestCase):
    # """ Test module for actions """
# 
    # list_url = reverse('actions-list')
# 
    # def setUp(self):
        # self.client = APIClient()
        # self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        # self.client.force_authenticate(self.user)
# 
    # def test_retrieve_actions_list(self):
        # Cooperative.objects.create(name="coop", business_name="testing coop", is_active=True)
        # response = self.client.get(self.list_url)
        # cooperatives = Cooperative.objects.all()
        # serializer = CooperativeSerializer(cooperatives, many=True)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)
# 
    # def test_retrieve_action(self):
        # response = self.client.get(reverse('actions-detail', kwars={"pk": 1}))
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data["name"], "actionName")
# 
    ##TODO we should test everything but with an user that is not part of this cooperative
    # def test_update_action(self):
        # response = self.client.put(reverse('actions-detail', kwars={"pk": 1}), { lo que cambió})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), {"id": 1, "name": "actionName"})
