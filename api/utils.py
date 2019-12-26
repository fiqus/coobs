from api.serializers import PartnerSerializer

# Custom auth response handler to retrieve user information
def jwt_response_payload_handler(token, user=None, request=None):
  return {
    'token': token,
    'user': PartnerSerializer(user, context={'request': request}).data
  }