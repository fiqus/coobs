from rest_framework.viewsets import ModelViewSet
from api.models import Principle, Action, Period, Cooperative, Partner
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer


class PrincipleView(ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class PeriodView(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

class CooperativeView(ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer

class PartnerView(ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
