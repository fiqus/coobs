from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse
from django.test import TestCase
from api.models import Cooperative
from api.serializers import CooperativeSerializer
from unittest.mock import patch
import requests
from api.tests.utils import MockResponse

COOPERATIVES_URL = reverse('cooperative-list')

class CooperativeTest(TestCase):
    """ Test module for cooperative API """

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

    def test_create_coop_successful(self):
        payload = {"name":"coop", "businessName":"testing coop", "language": "es", "reCaptchaToken": "test",
            'email': 'test_user@email.com', 'username': "test_user", 'password': 'test_pass', 
            'firstName': 'name', 'lastName': 'lastName'}
        with patch.object(requests, "post", return_value=MockResponse({"success": True}, 200)) as mock_method:
            self.client.post(self.list_url, payload)
            created_coop = Cooperative.objects.filter(business_name=payload["businessName"])
            exists = created_coop.exists()
            # TODO check for user created, assign_principles_to_coop, send_email_to_user, assign_coop_to_partner
            self.assertTrue(exists)
            mock_method.assert_called_once()



# principle_1 = MainPrinciple.objects.create(name="principle_1", name_key="principle_1", description_key="principle_1_eng").save()
# principle_2 = MainPrinciple.objects.create(name="principle_2", name_key="principle_2", description_key="principle_2_eng").save()
# principle_3 = MainPrinciple.objects.create(name="principle_3", name_key="principle_3", description_key="principle_3_eng").save()

# class GetAllPrinciplesTest(TestCase):
    # """ Test module for GET All principles API """
# 
    # def setUp(self):
        # Principle.objects.create(cooperative=cooperative, main_principle=principle_1)
        # Principle.objects.create(cooperative=cooperative, main_principle=principle_2)
        # Principle.objects.create(cooperative=cooperative, main_principle=principle_3)
        # 
# 
    # def test_get_all_principles(self):
        # response = client.get(reverse('list'))
        # principles = Principle.objects.all()
        # serializer = PrincipleSerializer(principles, many=True)
        # self.assertEqual(response.data, serializer.data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_principles_are_ok(self):
        # client = RequestsClient()
        # response = client.get('/principles/')
        # self.assertIs(response.status_code, 200)