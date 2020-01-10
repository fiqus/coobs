from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from random import seed, randint
from django.db import DatabaseError, transaction
from django.core.mail import EmailMultiAlternatives
from api.models import Principle, Action, Period, Cooperative, Partner, MainPrinciple
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer, MyTokenObtainPairSerializer, DashboardSerializer
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext as _

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

seed(1)
class PrincipleView(viewsets.ModelViewSet):
    serializer_class = PrincipleSerializer

    def get_queryset(self):
        return Principle.objects.filter(cooperative=self.request.user.cooperative_id)

class ActionView(viewsets.ModelViewSet):
    serializer_class = ActionSerializer

    def get_queryset(self):
        queryset = Action.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset 

    def create(self, request):
        action_serializer = ActionSerializer(data=request.data)

        if not action_serializer.is_valid():
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        partners_involved = action_serializer.validated_data.pop('partners_involved')
        action_data = Action.objects.create(**action_serializer.validated_data)
       
        setattr(action_data, 'cooperative_id', request.user.cooperative.id)
        for partner in partners_involved: 
            action_data.partners_involved.add(partner)

        action_data.save()
        return Response("ACTION_CREATED", status=status.HTTP_200_OK)

class PeriodView(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer

    def get_queryset(self):
        queryset = Period.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset

    def create(self, request):
        request.data['cooperative_id'] = self.request.user.cooperative_id
        period_serializer = PeriodSerializer(data=request.data)

        if not period_serializer.is_valid():
            return Response(period_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        period_data = Period.objects.create(**period_serializer.validated_data)
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
            cooperative_data = Cooperative.objects.create(**coop_serializer.validated_data)
            return cooperative_data

        def set_partner_data():
            partner_data = Partner.objects.create(**partner_serializer.validated_data)
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
            raise ValidationError({"recaptcha": "ERROR_RECAPTCHA"})

        coop = {'business_name': data['businessName']}
        coop_serializer = CooperativeSerializer(data=coop)

        partner = {'email': data['email'], 'username':data['email'], 'password':data['password'], 'first_name': data['firstName'], 'last_name': data['lastName']}
        partner_serializer = PartnerSerializer(data=partner)

        if not coop_serializer.is_valid(raise_exception=True):
            return Response(coop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not partner_serializer.is_valid(raise_exception=True):
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

        def assign_principles_to_coop():
            main_principles = MainPrinciple.objects.all()
            principles = list()
            for main_principle in main_principles:
                principle_data = Principle()
                setattr(principle_data, 'description', "")
                setattr(principle_data, 'visible', True)
                setattr(principle_data, 'cooperative', cooperative)
                setattr(principle_data, 'main_principle', main_principle)
                principles.append(principle_data)
            Principle.objects.bulk_create(principles)

        def assign_coop_to_partner():
            setattr(partner, 'cooperative', cooperative)
            partner.save()
            assign_principles_to_coop()

        transaction.on_commit(assign_coop_to_partner)
        return Response(f'{data["businessName"]} Cooperative asked to be created', status=status.HTTP_200_OK)

class PartnerView(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer

    def get_queryset(self):
        queryset = Partner.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset

    def create(self, request):
        data = request.data
        cooperative = request.user.cooperative_id
        def set_partner_data():
            data['username'] = data['email']
            partner_serializer = PartnerSerializer(data=data)
            if not partner_serializer.is_valid():
                return Response(partner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            partner_data = Partner.objects.create(**partner_serializer.validated_data)
            setattr(partner_data, 'cooperative_id', cooperative)
            partner_data.set_password(data['password'])
            return partner_data

        partner = set_partner_data()

        try:
            with transaction.atomic():
                partner.save()
        except Exception as errors:
            return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Partner asked to be created', status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        partner = self.get_object()

        if partner.id == request.user.id:
            return Response(data={'detail': _("Current logged in user can not delete it self.")}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(partner)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DashboardView(viewsets.ViewSet):
    def list(self, request):
        cooperative_id = request.user.cooperative_id
        period_data = Period.get_current(cooperative_id)        
        if not period_data:
            return Response("NO_PERIOD", status=status.HTTP_400_BAD_REQUEST)        
        period_serializer = PeriodSerializer(period_data)

        action_data = Action.get_current_actions(cooperative_id, period_data.date_from, period_data.date_to)
        action_serializer = ActionSerializer(action_data, many=True)

        principle_data = Principle.objects.filter(visible=True)
        principle_serializer = PrincipleSerializer(principle_data, many=True)

        return Response({'period': period_serializer.data, 'actions': action_serializer.data, 'principles': principle_serializer.data})