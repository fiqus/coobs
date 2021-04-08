import requests
import json
import unittest
import random
from datetime import datetime, date, timedelta
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from api.models import Cooperative, Partner, MainPrinciple, Principle, Action
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
        cls.coop1 = Cooperative.objects.create(business_name='cooperative 1', name="coop 1")
        cls.coop2 = Cooperative.objects.create(business_name='cooperative 2', name="coop 2")
        #FIXME por qué NO puedo mover el resto de setUp acá?

    def setUp(self):
        self.client = APIClient()
        self.user_coop1 = get_user_model().objects.create_user("test_user_coop1@mail.com", "password1")
        self.user_coop2 = get_user_model().objects.create_user("test_user_coop2@mail.com", "password2")
        self.user_coop1.cooperative = self.coop1
        self.user_coop2.cooperative = self.coop2
        self.client.force_authenticate(self.user_coop1)
        self.casper = Partner.objects.create(username='Casper', email="casper@mail.com", cooperative=self.coop1)
        self.muffin = Partner.objects.create(username='Muffy', email="muffy@mail.com", cooperative=self.coop2)
    
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
        self.assertEqual(created_partner.cooperative.id, self.coop1.id)
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
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': self.casper.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_invalid_delete_partner_unsuccessfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_same_partner_as_logged_in_unsuccessfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': self.user_coop1.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_partner_from_other_coop_unsuccessfull(self):
        response = self.client.delete(reverse(self.detail_view, kwargs={'pk': self.muffin.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ActionTest(TestCase):
    """ Test module for actions """

    list_url = reverse('Action-list')
    public_actions_url = reverse('public_actions')

    @classmethod
    def create_main_principles(cls):
        main_principles = []
        for i in [0, 1 , 2]:
            main_principles.append(MainPrinciple.objects.create(name=f"main pple {i}", description=f"main principle {i}"))
        return main_principles

    @classmethod
    def setUpTestData(cls):
        cls.coop = Cooperative.objects.create(name="coop", business_name="testing coop", is_active=True)
        cls.main_principles = cls.create_main_principles()
        cls.principles = []
        for main_pple in cls.main_principles:
            cls.principles.append(Principle.objects.create(cooperative=cls.coop, main_principle=main_pple, description=f"principle {main_pple.id}", custom_description=f"principle {main_pple.id}"))
        #FIXME por qué NO puedo mover el resto de setUp acá?

    def create_action(self, name, description=None, public=True, date=datetime.today(), coop=None):
        return Action.objects.create(
            cooperative=coop if coop != None else self.coop,
            name=name,
            description=description,
            public=public,
            date=date
        )

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test_user@mail.com", "password")
        self.user.cooperative = self.coop
        self.client.force_authenticate(self.user)

    def test_retrieve_actions_list(self):
        self.create_action(name="action 1")
        self.create_action(name="action 2")
        response = self.client.get(self.list_url)
        actions = Action.objects.all()
        serializer = ActionSerializer(actions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(len(serializer.data), 2)

    def test_retrieve_actions_list_with_filter_contents(self):
        self.create_action(name="find my name", description="find my description")
        self.create_action(name="don't find me", description="don't find me")
        response = self.client.get(f"{self.list_url}?contents=my%20name")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        response = self.client.get(f"{self.list_url}?contents=my%20description")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        response = self.client.get(f"{self.list_url}?contents=my")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        response = self.client.get(f"{self.list_url}?contents=me")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_public_actions_list(self):
        for idx in range(1, 101):
            date = datetime.today().date() - timedelta(days=idx)
            self.create_action(name="Action {}!".format(idx), public=idx % 2 == 0, date=date)

        response = self.client.get(self.public_actions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["actions"]), 20)
        self.assertEqual(response.data["actions"][0]["name"], "Action 2!")
        self.assertEqual(response.data["actions"][19]["name"], "Action 40!")

        response = self.client.get(f"{self.public_actions_url}?more=wrong!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["actions"]), 20)
        self.assertEqual(response.data["actions"][0]["name"], "Action 2!")
        self.assertEqual(response.data["actions"][19]["name"], "Action 40!")

        response = self.client.get(f"{self.public_actions_url}?more=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["actions"]), 20)
        self.assertEqual(response.data["actions"][0]["name"], "Action 42!")
        self.assertEqual(response.data["actions"][19]["name"], "Action 80!")

        response = self.client.get(f"{self.public_actions_url}?more=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["actions"]), 10)
        self.assertEqual(response.data["actions"][0]["name"], "Action 82!")
        self.assertEqual(response.data["actions"][9]["name"], "Action 100!")

    def test_retrieve_action(self):
        action = self.create_action(name="test action")
        response = self.client.get(reverse('Action-detail', kwargs={"pk": action.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test action")
    
    def test_invalid_create_action_unsuccessfull(self):
        action_to_create = {'name': 'invalid action', 'cooperative': self.coop.id, 'partners_involved': [], 'principles': [], 'sustainable_development_goals': []}
        response = self.client.post(self.list_url, 
                                    data=json.dumps(action_to_create), 
                                    content_type="application/json")        
        created_action = Action.objects.filter(name=action_to_create["name"])
        self.assertFalse(created_action.exists())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_valid_create_action_successfull(self):
        action_to_create = {'name': 'valid action',
                            'cooperative': self.coop.id, 'partners_involved': [], 
                            'principles': [{'id': self.principles[0].id, 'custom_description': 'custom description'}],
                            'sustainable_development_goals': []}
        response = self.client.post(self.list_url, 
                                    data=json.dumps(action_to_create), 
                                    content_type="application/json")
        created_action = Action.objects.filter(name=action_to_create["name"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(created_action.exists())
        created_action = created_action[0]
        self.assertEqual(created_action.cooperative.id, self.coop.id)
        self.assertEqual(created_action.principles.all()[0].id, self.principles[0].id)

    #TODO def test_update_action(self):
        # response = self.client.put(reverse('actions-detail', kwars={"pk": 1}), { lo que cambió})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(json.loads(response.content), {"id": 1, "name": "actionName"})
    
    #TODO testear todo con un usuario que no es parte de la cooperativa que quiere modificar