from rest_framework.viewsets import ModelViewSet
from api.models import Principle, Action, Cooperative
from api.serializers import PrincipleSerializer, ActionSerializer, CooperativeSerializer


class CooperativeView(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer


class PrincipleView(ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
