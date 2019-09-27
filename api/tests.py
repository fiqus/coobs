from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('/principles/')
assert response.status_code == 200
