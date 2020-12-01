import requests
import json
import unittest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from api.models import Cooperative, Partner, Principle, Action
from api.serializers import CooperativeSerializer, ActionSerializer
from api.views import CooperativeView, PartnerView, views_utils
from unittest.mock import patch
from api.tests.utils import MockResponse

class CooperativeTest(TestCase):
    """ Test module for cooperative """

    list_url = reverse('cooperative-list')

    @classmethod
    def setUpTestData(cls):
        Cooperative.objects.create(name="coop", business_name="testing coop", is_active=True)
        Cooperative.objects.create(name="coop_2", business_name="testing coop 2", is_active=True)
        Cooperative.objects.create(name="coop_3", business_name="testing coop 3", is_active=True)
        cls.client = APIClient()
        cls.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        cls.client.force_authenticate(cls.user)

    def test_retrieve_coops(self):
        response = self.client.get(self.list_url)
        cooperatives = Cooperative.objects.all()
        serializer = CooperativeSerializer(cooperatives, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch("api.views.views_utils.create_and_send_email")
    @patch("requests.post", return_value=MockResponse({"success": True}, 200))
    def test_create_valid_coop_successfull(self, mock_method, create_and_send_email): 
        valid_payload = {"name":"new coop", "businessName":"new testing coop", "language": "es", "reCaptchaToken": "test",
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
    detail_view = 'Partner-detail'

    @classmethod
    def setUpTestData(cls):
        cls.coop = Cooperative.objects.create(business_name='cooperative', name="coop")
        #FIXME por qué NO puedo mover el resto de setUp acá?

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        self.user.cooperative = self.coop
        self.client.force_authenticate(self.user)
        self.casper = Partner.objects.create(username='Casper', email="casper@mail.com")
        self.muffin = Partner.objects.create(username='Muffy', email="muffy@mail.com")

    def test_valid_create_partner_successfull(self):
        user_to_create = {'email': 'user@email.com', 'username': "user", 'password': 'test_pass2020', 'confirm_password': 'test_pass2020'}
        response = self.client.post(self.list_url, 
                                    data=json.dumps(user_to_create), 
                                    content_type="application/json")
        created_partner = Partner.objects.filter(email=user_to_create["email"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(created_partner.exists())
        created_partner = created_partner[0]
        self.assertTrue(created_partner.is_active)
        self.assertEqual(created_partner.cooperative.id, self.coop.id)
        #TODO chequear que le mandó un mail al usuario creado

    def test_invalid_create_partner_unsuccessfull(self):
        user_to_create = {'email': 'user@email.com', 'username': "user", 'password': 'test_pass', 'confirm_password': 'test_pas'}
        response = self.client.post(self.list_url, 
                                    data=json.dumps(user_to_create), 
                                    content_type="application/json")
        created_partner = Partner.objects.filter(email=user_to_create["email"])
        self.assertFalse(created_partner.exists())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_partner_successfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_partner_unsuccessfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_same_partner_as_logged_in_unsuccessfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    #TODO testear que un user no puede borrar users de otra coope, funcionalidad NO desarrollada
    # https://github.com/fiqus/coobs/issues/282


class ActionTest(TestCase):
    """ Test module for actions """

    list_url = reverse('Action-list')

    @classmethod
    def setUpTestData(cls):
        cls.coop = Cooperative.objects.create(name="coop", business_name="testing coop", is_active=True)
        #FIXME por qué NO puedo mover el resto de setUp acá?

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        self.user.cooperative = self.coop
        self.client.force_authenticate(self.user)
        self.action = Action.objects.create(name="test action", cooperative=self.coop)

    def test_retrieve_actions_list(self):
        response = self.client.get(self.list_url)
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(serializer.data))

    def test_retrieve_action(self):
        response = self.client.get(reverse('Action-detail', kwargs={"pk": self.action.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test action")

    #TODO testear crear una accion
    #TODO testear todo con un usuario que no es parte de la cooperativa que quiere modificar
    # def test_update_action(self):
        # response = self.client.put(reverse('actions-detail', kwars={"pk": 1}), { lo que cambió})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), {"id": 1, "name": "actionName"})