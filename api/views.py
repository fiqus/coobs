from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from random import seed, randint
from django.core.mail import EmailMultiAlternatives
from api.models import Principle, Action, Period, Cooperative, Partner
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer, PartnerCreateSerializer

seed(1)
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
    permission_classes = (permissions.AllowAny,)
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer

    def create(self, request):
        data = request.data        
        def set_coop_data():
            cooperative_data = Cooperative()
            setattr(cooperative_data, 'business_name', data['business_name'])
            setattr(cooperative_data, 'is_active', False)
            return cooperative_data

        def set_partner_data():
            partner_data = Partner()
            setattr(partner_data, 'first_name', data['firstName'])
            setattr(partner_data, 'last_name', data['lastName'])
            setattr(partner_data, 'email', data['email'])
            setattr(partner_data, 'username', data['email'])
            setattr(partner_data, 'cooperative', cooperative)
            setattr(partner_data, 'password', data['password'])
            setattr(partner_data, 'is_active', False)
            return partner_data
        
        def send_email():
            text_content = f'Verify the coop: {cooperative.business_name} with ID {cooperative.id}'
            html_content = f'<div><h1>Verify the coop: {cooperative.business_name} with ID {cooperative.id}</h1></div>'
            email = EmailMultiAlternatives('A new cooperative wants to join COOBS!', text_content, 'info@fiqus.coop', ['info@fiqus.coop'])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        coop = {'business_name': data['businessName']}
        coop_serializer = CooperativeSerializer(data=coop)

        partner = {'email': data['email'], 'username':data['email'], 'password':data['password'], 'first_name': data['firstName'], 'last_name': data['lastName']}
        partner_serializer = PartnerSerializer(data=partner)

        if not coop_serializer.is_valid():
            return Response(coop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not partner_serializer.is_valid():
            return Response(partner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cooperative = set_coop_data()
        cooperative.save()
        partner = set_partner_data()
        partner.save()
        send_email()
        return Response(f'{data["business_name"]} Cooperative asked to be created', status=status.HTTP_200_OK)
    
    @action(detail=False)
    def get_partners(self, request):
        import pdb; pdb.set_trace()
        partners = Partner.objects.all().filter(cooperative__id=self.queryset[0].id)
        serializer = PartnerSerializer(partners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PartnerView(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class PartnerCreateView(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerCreateSerializer