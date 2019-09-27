from rest_framework.viewsets import ModelViewSet
from api.models import Principle, Action, Period
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer


class PrincipleView(ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class PeriodView(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
