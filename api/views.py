from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.models import Principle, Event, Cooperative
from api.serializers import PrincipleSerializer, EventSerializer, CooperativeSerializer


class CooperativeView(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer


class PrincipleView(ReadOnlyModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class EventView(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
