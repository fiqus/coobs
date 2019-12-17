from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import Principle, Action, Period, Cooperative, Partner
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer, PartnerCreateSerializer


class PrincipleView(viewsets.ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class PeriodView(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer

class CooperativeView(viewsets.ModelViewSet):
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer
    
    # @action(detail=True, methods=['post'])
    # def ask_to_create_cooperative_account(self, request):        
    #     #mandar mail a coop con link a form para crear coop y usuario con data del form
    #     return Response({'status':'Cooperative to be created'})

    # @action(detail=True, methods=['post'])
    # def create_cooperative_account(self, request):
    #     #TODO what do we have in request.data?
    #     import pdb; pdb.set_trace()
    #     serializer = CooperativeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         #TODO create coop, create user
    #         cooperative = Cooperative(request.data)
    #         cooperative.save()
    #         #TODO send email to coop, send email to fiqus
    #         return Response({'status':'Cooperative created'})
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False)
    def get_partners(self, request):
        import pdb; pdb.set_trace()
        partners = Partner.objects.all(cooperative__id=self)
        return Response(partners, status=status.HTTP_200_OK)

class PartnerView(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerCreateView(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer