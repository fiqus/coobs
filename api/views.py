from rest_framework.viewsets import ModelViewSet
from api.models import Principle
from api.serializers import PrincipleSerializer


class PrincipleView(ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer
