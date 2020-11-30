import requests
import json
import unittest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
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
    def test_create_valid_coop_successfull(self, mock_method, create_and_send_email): 
        valid_payload = {"name":"coop", "businessName":"testing coop", "language": "es", "reCaptchaToken": "test",
            'email': 'test_user@email.com', 'username': "test_user", 'password': 'test_pass', 
            'firstName': 'name', 'lastName': 'lastName'}
        
        response = self.client.post(self.list_url, valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_coop = Cooperative.objects.filter(business_name=valid_payload["businessName"])
        created_partner = Partner.objects.filter(email=valid_payload["email"])
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

    def test_create_invalid_coop_unsuccessfull(self):
        invalid_payload = {"businessName":"", "language": "es", "reCaptchaToken": "test",
            'email': 'test_user@email.com', 'username': "test_user", 'password': 'test_pass'}
        response = self.client.post(self.list_url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_user_unsuccessfull(self):
        invalid_payload = {"businessName":"coop business name", "language": "es", "reCaptchaToken": "test",
            'email': 'test_user@email.com', 'username': "test_user", 'password': ''}        
        response = self.client.post(self.list_url, invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PartnerTest(TestCase):
    """ Test module for partners """
    list_url = reverse('Partner-list')

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        self.client.force_authenticate(self.user)
        self.casper = Partner.objects.create(username='Casper', email="casper@mail.com")
        self.muffin = Partner.objects.create(username='Muffy', email="muffy@mail.com")

    #TODO test partner create
    def test_valid_delete_partner(self):
        response = self.client.delete(
            reverse('Partner-detail', kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_partner(self):
        response = self.client.delete(
            reverse('Partner-detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_delete_same_partner_as_logged_in(self):
        response = self.client.delete(
            reverse('Partner-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
