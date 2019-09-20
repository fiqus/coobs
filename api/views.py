from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.models import Principle, Action, Cooperative
from api.serializers import PrincipleSerializer, ActionSerializer, CooperativeSerializer


class CooperativeView(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer


class PrincipleView(ReadOnlyModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
