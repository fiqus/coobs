from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from api.models import Principle, Action, Period, Cooperative, Partner, MainPrinciple
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, PartnerSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer, MainPrincipleSerializer, ActionsByCoopSerializer
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.translation import gettext as _
from django.db.models import Count
from api.dashboard_charts.charts_data_helpers import get_cards_data, get_progress_data, get_all_principles_data, get_actions_by_partner, get_monthly_investment_by_principle, get_monthly_actions_by_principle
import requests
from datetime import datetime, date
from django.template.loader import get_template
from django.template import Context



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


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
        principles = action_serializer.validated_data.pop('principles')
        action_data = Action.objects.create(**action_serializer.validated_data)
       
        setattr(action_data, 'cooperative_id', request.user.cooperative.id)
        for partner in partners_involved: 
            action_data.partners_involved.add(partner)
       
        for principle in principles: 
            action_data.principles.add(principle)

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
            text_content = f'Verify the coop: {cooperative.business_name} with ID {cooperative.id}. Remember to activate the cooperative and created user. After that send them an email to notify that te cooperative can be used.'
            html_content = f'<div><h3>Verify the coop: {cooperative.business_name} with ID {cooperative.id}</h3><br/><p>Remember to activate the cooperative and created user. <br/>After that send them an email to notify that te cooperative can be used.</p></div>'
            email = EmailMultiAlternatives('A new cooperative wants to join COOBS!',
                                           text_content, getattr(settings, "DEFAULT_FROM_EMAIL", "test@console.com"),
                                           [getattr(settings, "EMAIL_ADMIN_ACCOUNT", "test@console.com")])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        def assign_principles_to_coop():
            main_principles = MainPrinciple.objects.all()
            principles = list()
            for main_principle in main_principles:
                principle_data = Principle(cooperative=cooperative, main_principle=main_principle)
                principles.append(principle_data)
            Principle.objects.bulk_create(principles)

        def assign_coop_to_partner():
            setattr(partner, 'cooperative', cooperative)
            partner.save()
            assign_principles_to_coop()

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
                partner.cooperative = cooperative
                partner.save()
                send_email()
        except Exception as errors:
            return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        transaction.on_commit(assign_coop_to_partner)
        created_coop_success_msg = _("The cooperative {0} has been created for user {1} {2} with email {3}.".format(data['businessName'], data['firstName'], data['lastName'], data['email']))
        account_needs_to_be_activated_msg = _("It needs to be revisited and activated by an administrator, you'll receive an email when your cooperative is active and ready to be used.")

        return Response({'created_coop_success_msg': created_coop_success_msg,'account_needs_to_be_activated_msg': account_needs_to_be_activated_msg}, status=status.HTTP_200_OK)


class PartnerView(viewsets.ModelViewSet):
    serializer_class = PartnerSerializer

    def get_queryset(self):
        queryset = Partner.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset

    def create(self, request):
        data = request.data
        password = data['password']
        cooperative = request.user.cooperative

        def set_partner_data():
            data['username'] = data['email']
            partner_serializer = PartnerSerializer(data=data)
            partner_serializer.is_valid(raise_exception=True)

            password_data = {'new_password': data['password'], 'confirm_password': data['confirm_password']}
            change_pass_serializer = ChangePasswordSerializer(data=password_data)
            change_pass_serializer.is_valid(raise_exception=True)

            partner_data = Partner.objects.create(**partner_serializer.validated_data)
            setattr(partner_data, 'cooperative_id', cooperative.id)

            partner_data.set_password(data['password'])

            return partner_data

        partner = set_partner_data()

        def send_email():
            public_url = "{}://{}".format(settings.WEB_PROTOCOL, settings.WEB_URL)
            context = {'cooperative': CooperativeSerializer(cooperative).data, 'password': password, 'public_url': public_url}
            text_template = get_template('partner_created_email_template.txt')
            text_content = text_template.render(context)
            html_template = get_template('partner_created_email_template.html')
            html_content = html_template.render(context)            
            subject = _('Hello {0}, you have been added to COOBS!'.format(partner.first_name))
            email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_ADMIN_ACCOUNT, [partner.email])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        try: 
            with transaction.atomic():
                partner.save()
                send_email()
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
    def get_current_period(self, all_periods):
        today = datetime.today()
        # Note that if there are two periods that overlap, it returns the last one.
        current_periods = [period for period in all_periods if datetime.strptime(period['date_from'], '%Y-%m-%d') < today < datetime.strptime(period['date_to'], '%Y-%m-%d')]
        current_period = current_periods[len(current_periods)-1]
        if (current_period):
            return current_period
        return None
        
    def list(self, request):        
        cooperative_id = request.user.cooperative_id

        all_periods_data = Period.objects.filter(cooperative=cooperative_id)
        all_periods_serializer = PeriodSerializer(all_periods_data, many=True)
        if not all_periods_serializer.data:
            return Response("NO_PERIOD", status=status.HTTP_400_BAD_REQUEST)
        
        period_id = request.query_params.get('periodId', None)
        if period_id is not None:
            period_data = next((period for period in all_periods_serializer.data if period['id']==int(period_id)), None)
        else:
            period_data = self.get_current_period(all_periods_serializer.data)        

        if not period_data:
            return Response("NO_PERIOD", status=status.HTTP_400_BAD_REQUEST)

        action_data = Action.get_current_actions(cooperative_id, period_data['date_from'], period_data['date_to']).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)
        
        date = datetime.today()
        done_actions_data = Action.get_current_actions(cooperative_id, period_data['date_from'], date).order_by('date')

        principle_data = Principle.objects.filter(visible=True)
        principle_serializer = PrincipleSerializer(principle_data, many=True)

        partner_data = Partner.objects.filter(cooperative=cooperative_id, action__date__gte=period_data['date_from'], action__date__lte=date).annotate(total=Count('username')).order_by()

        actions_by_principles_data = Principle.objects.filter(cooperative=cooperative_id, action__date__gte=period_data['date_from'], action__date__lte=date).annotate(total=Count('id')).order_by()

        principles = {principle['id']: principle['name_key'] for principle in list(principle_serializer.data)}
        
        charts = {
            'cards_data': get_cards_data(action_data, done_actions_data, period_data),
            'all_principles_data': get_all_principles_data(actions_by_principles_data, principles),
            'progress_data': get_progress_data(action_data, done_actions_data, period_data),
            'actions_by_partner': get_actions_by_partner(partner_data),
            'monthly_investment_by_date': get_monthly_investment_by_principle(done_actions_data, period_data['date_from'], principles),
            'monthly_actions_by_principle': get_monthly_actions_by_principle(done_actions_data, datetime.strptime(period_data['date_from'], '%Y-%m-%d'), principles),
            }

        return Response({'period': period_data, 'actions': action_serializer.data, 'principles': principle_serializer.data, 'charts': charts, 'all_periods':all_periods_serializer.data})
class BalanceView(viewsets.ViewSet):
    def get_current_period(self, all_periods):
        today = datetime.today()
        # Note that if there are two periods that overlap, it returns the last one.
        current_periods = [period for period in all_periods if datetime.strptime(period['date_from'], '%Y-%m-%d') < today < datetime.strptime(period['date_to'], '%Y-%m-%d')]
        current_period = current_periods[len(current_periods)-1]
        if (current_period):
            return current_period
        return None

    def list(self, request):
        cooperative_id = request.user.cooperative_id
        
        all_periods_data = Period.objects.filter(cooperative=cooperative_id)
        all_periods_serializer = PeriodSerializer(all_periods_data, many=True)
        if not all_periods_serializer.data:
            return Response("NO_PERIOD", status=status.HTTP_400_BAD_REQUEST)
        
        period_id = request.query_params.get('periodId', None)
        if period_id is not None:
            period_data = next((period for period in all_periods_serializer.data if period['id']==int(period_id)), None)
        else:
            period_data = self.get_current_period(all_periods_serializer.data)

        if not period_data:
            return Response("NO_PERIOD", status=status.HTTP_400_BAD_REQUEST)

        action_data = Action.get_current_actions(cooperative_id, period_data['date_from'], period_data['date_to']).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)
        
        return Response({'period': period_data, 'actions': action_serializer.data, 'all_periods':all_periods_serializer.data})

class MedalTableView(viewsets.ViewSet):
    def list(self, request):
        first_day_of_year = date(datetime.today().year, 1, 1)
        actions_by_coop_data = Action.objects.filter(date__gte=first_day_of_year, public=True, principle__visible=True).values('cooperative', 'cooperative__name', 'principle__main_principle__name_key', 'principle__main_principle__name').annotate(actions_count=Count('principle')).order_by('cooperative')
        actions_by_coop_serializer = ActionsByCoopSerializer(actions_by_coop_data, many=True)
        
        main_principle_data = MainPrinciple.objects.all()
        main_principle_serializer = MainPrincipleSerializer(main_principle_data, many=True)

        return Response({'actions': actions_by_coop_serializer.data, 'principles': main_principle_serializer.data})
