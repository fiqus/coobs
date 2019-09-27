from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.models import Principle, Action, Cooperative, Period
from api.serializers import PrincipleSerializer, ActionSerializer, CooperativeSerializer, PeriodSerializer


class CooperativeView(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer


class PrincipleView(ReadOnlyModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class PeriodView(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
