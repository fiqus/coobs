from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from random import seed, randint
from django.db import DatabaseError, transaction
from django.core.mail import EmailMultiAlternatives
from api.models import Principle, Action, Period, Cooperative, Partner
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests

seed(1)
class PrincipleView(viewsets.ModelViewSet):
    queryset = Principle.objects.all()
    serializer_class = PrincipleSerializer


class ActionView(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        queryset = Action.objects.filter(cooperative=self.request.user.cooperative.id)
        return queryset

class PeriodView(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer

    def get_queryset(self):
        queryset = Period.objects.filter(cooperative=self.request.user.cooperative.id)
        return queryset

    def create(self, request):
        period_serializer = PeriodSerializer(data=request.data)

        if not period_serializer.is_valid():
            return Response(period_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        period_data = Period()
        setattr(period_data, 'name', request.data['name'])
        setattr(period_data, 'date_from', request.data['date_from'])
        setattr(period_data, 'date_to', request.data['date_to'])
        setattr(period_data, 'actions_budget', request.data['actions_budget'])
        setattr(period_data, 'cooperative_id', request.user.cooperative.id)

        period_data.save()
        return Response("PERIOD_CREATED", status=status.HTTP_200_OK)

class CooperativeView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer

    def create(self, request):
        data = request.data
        def set_coop_data():
            cooperative_data = Cooperative()
            setattr(cooperative_data, 'business_name', data['businessName'])
            setattr(cooperative_data, 'is_active', False)
            return cooperative_data

        def set_partner_data():
            partner_data = Partner()
            setattr(partner_data, 'first_name', data['firstName'])
            setattr(partner_data, 'last_name', data['lastName'])
            setattr(partner_data, 'email', data['email'])
            setattr(partner_data, 'username', data['email'])
            partner_data.set_password(data['password'])
            setattr(partner_data, 'is_active', False)
            return partner_data

        def send_email():
            text_content = f'Verify the coop: {cooperative.business_name} with ID {cooperative.id}'
            html_content = f'<div><h1>Verify the coop: {cooperative.business_name} with ID {cooperative.id}</h1></div>'
            email = EmailMultiAlternatives('A new cooperative wants to join COOBS!', text_content, 'info@fiqus.coop', [settings.EMAIL_ADMIN_ACCOUNT])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        recaptchaResult = requests.post(
            settings.RECAPTCHA_VERIFY_URL,
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': data['reCaptchaToken']
            }
        )

        if not recaptchaResult.json()['success']:
            return Response(coop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        coop = {'business_name': data['businessName']}
        coop_serializer = CooperativeSerializer(data=coop)

        partner = {'email': data['email'], 'username':data['email'], 'password':data['password'], 'first_name': data['firstName'], 'last_name': data['lastName']}
        partner_serializer = PartnerSerializer(data=partner)

        if not coop_serializer.is_valid():
            return Response(coop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not partner_serializer.is_valid():
            return Response(partner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cooperative = set_coop_data()
        partner = set_partner_data()

        try:
            with transaction.atomic():
                cooperative.save()
                partner.save()
                send_email()
        except Exception as errors:
            return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        def assign_coop_to_partner():
            setattr(partner, 'cooperative', cooperative)
            partner.save()

        transaction.on_commit(assign_coop_to_partner)
        return Response(f'{data["businessName"]} Cooperative asked to be created', status=status.HTTP_200_OK)
    

class PartnerView(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer

    def get_queryset(self):
        queryset = Partner.objects.filter(cooperative=self.request.user.cooperative.id)
        return queryset
