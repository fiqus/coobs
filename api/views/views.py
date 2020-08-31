import functools
from datetime import datetime, date
from .views_utils import *

import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.template.loader import get_template, render_to_string
from django.utils.translation import gettext as _
from rest_framework import viewsets, status, permissions, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.dashboard_charts.charts_data_helpers import get_cards_data, get_progress_data, get_all_principles_data, \
    get_actions_by_partner, get_monthly_hours, get_monthly_investment_by_principle, get_monthly_actions_by_principle,\
    get_all_principles_data_for_current_partner
from api.models import Principle, Action, Period, Cooperative, Partner, MainPrinciple, \
    SustainableDevelopmentGoal
from api.serializers import PrincipleSerializer, ActionSerializer, PeriodSerializer, CooperativeSerializer, \
    PartnerSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer, MainPrincipleSerializer, \
    ActionsByCoopSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import detail_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import remove_query_param, replace_query_param
from datetime import datetime
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.dispatch import receiver
from markdownify import markdownify as md


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class PrincipleView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of principles for the current cooperative.

    create:
    Creates a principle for the current cooperative.

    destroy:
    Removes the selected principle.
    """        
    serializer_class = PrincipleSerializer

    def get_queryset(self):
        return Principle.objects.filter(cooperative=self.request.user.cooperative_id)

class ActionFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name="date", lookup_expr='gte')
    date_to = filters.DateFilter(field_name="date", lookup_expr='lte')
    partner = filters.ModelMultipleChoiceFilter(
        field_name="partners_involved",
        queryset=Partner.objects.all()
    )
    principle = filters.ModelMultipleChoiceFilter(
        field_name="principles",
        queryset=Principle.objects.all()
    )
    sustainable_development_goal = filters.ModelMultipleChoiceFilter(
        field_name="sustainable_development_goals",
        queryset=SustainableDevelopmentGoal.objects.all()
    )

    class Meta:
        model = Action
        fields = ['principle', 'date_from', 'date_to', 'partner', 'sustainable_development_goal']


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page': self.page.number,
            'num_pages': self.page.paginator.num_pages,
            'page_size': self.page.paginator.per_page,
            'results': data
        })

class ActionView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of actions for the current cooperative.

    create:
    Creates an action for the current cooperative.

    destroy:
    Removes the selected action.
    """    
    serializer_class = ActionSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ActionFilter
    pagination_class =  StandardResultsSetPagination
    ordering_fields = ['date', 'name']
    ordering = ['-date']

    def get_queryset(self):
        queryset = Action.objects.filter(cooperative=self.request.user.cooperative_id).order_by('-date')
        return queryset

    def create(self, request):
        action_serializer = ActionSerializer(data=request.data)

        if not action_serializer.is_valid():
            return Response(action_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        partners_involved = action_serializer.validated_data.pop('partners_involved')
        principles = action_serializer.validated_data.pop('principles')
        sustainable_development_goals = action_serializer.validated_data.pop('sustainable_development_goals')
        action_data = Action.objects.create(**action_serializer.validated_data)

        setattr(action_data, 'cooperative_id', request.user.cooperative.id)
        for partner in partners_involved:
            action_data.partners_involved.add(partner['id'])

        for principle in principles:
            action_data.principles.add(principle['id'])

        for goal in sustainable_development_goals:
            action_data.sustainable_development_goals.add(goal['id'])

        action_data.description = md(action_data.description)
        action_data.save()
        return Response("ACTION_CREATED", status=status.HTTP_200_OK)

    def perform_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.request.data['description'] = md(self.request.data['description'])
        serializer = self.get_serializer(instance, data=self.request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        result = serializer.save()
        return Response("ACTION_UPDATED", status=status.HTTP_200_OK)


class PeriodView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of periods for the current cooperative.

    create:
    Creates a period for the current cooperative.

    destroy:
    Removes the selected period.
    """
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
    """
    list:
    Returns the list of cooperatives.

    create:
    Creates a cooperative.

    destroy:
    Removes the selected cooperative.
    """
    schema = None
    permission_classes = (permissions.AllowAny,)
    queryset = Cooperative.objects.all()
    serializer_class = CooperativeSerializer

    @transaction.atomic
    def create(self, request):
        data = request.data
        language = data['language']

        def set_coop_data():
            cooperative_data = Cooperative.objects.create(**coop_serializer.validated_data)
            return cooperative_data

        def set_partner_data():
            partner_data = Partner.objects.create(**partner_serializer.validated_data)
            partner_data.set_password(data['password'])
            setattr(partner_data, 'is_active', False)
            return partner_data

        def send_email_to_admin():
            text_content = f'Verify the coop: {cooperative.business_name} with ID {cooperative.id}. Remember to activate the cooperative and created user. After that send them an email to notify that te cooperative can be used.'
            html_content = f'<div><h3>Verify the coop: {cooperative.business_name} with ID {cooperative.id}</h3><br/><p>Remember to activate the cooperative and created user. <br/>After that send them an email to notify that te cooperative can be used.</p></div>'
            email = EmailMultiAlternatives('A new cooperative wants to join COOBS!', text_content,
                                           getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
                                           [getattr(settings, "EMAIL_TO_ADMIN", "test@console.com")])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        def send_email_to_user():
            public_url = "{}://{}".format(settings.WEB_PROTOCOL, settings.WEB_URL)
            context = {'public_url': public_url, 'email': partner.email}
            text_template = get_template('coop_created_email_template.txt')
            text_content = text_template.render(context)
            html_template = get_template('coop_created_email_template.html')
            html_content = html_template.render(context)
            subject = _('Hello %(partner_name)s, your cooperative is been added to COOBS!') % {"partner_name": partner.first_name}
            email = EmailMultiAlternatives(subject, text_content,
                                           getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
                                           [partner.email])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        def assign_principles_to_coop():
            main_principles = MainPrinciple.objects.all()
            principles = list()
            for main_principle in main_principles:
                description = main_principle.description_es if language=='es' else main_principle.description_en
                principle_data = Principle(cooperative=cooperative, description = description, main_principle=main_principle)
                principles.append(principle_data)
            Principle.objects.bulk_create(principles)

        def assign_coop_to_partner():
            setattr(partner, 'cooperative', cooperative)
            partner.save()
            assign_principles_to_coop()

        recaptchaResult = requests.post(
            settings.RECAPTCHA_VERIFY_URL,
            data={
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': data['reCaptchaToken']
            }
        )

        if not recaptchaResult.json()['success']:
            return Response(data={'detail': _("There has been an error validating recaptcha. Please, contact the site administrator.")},
                            status=status.HTTP_400_BAD_REQUEST)

        coop = {'business_name': data['businessName']}
        coop_serializer = CooperativeSerializer(data=coop)

        partner = {'email': data['email'], 'username': data['email'], 'password': data['password'],
                   'first_name': data['firstName'], 'last_name': data['lastName']}
        partner_serializer = PartnerSerializer(data=partner)

        if not coop_serializer.is_valid(raise_exception=True):
            return Response(coop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not partner_serializer.is_valid(raise_exception=True):
            return Response(partner_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cooperative = set_coop_data()
        partner = set_partner_data()

        try:
            cooperative.save()
            partner.cooperative = cooperative
            partner.save()
            send_email_to_admin()
            send_email_to_user()
        except Exception as errors:
            raise IntegrityError("Partner asked to be created but it FAILED.", errors)
            #FIXME this way it rollbacks the transaction, do we have a way to handle what we send to the client?
            # return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        transaction.on_commit(assign_coop_to_partner)

        created_coop_success_msg = _(
            "The cooperative %(businessName)s has been created for user %(firstName)s %(lastName)s with email %(email)s.") % {
                "businessName": data['businessName'], "firstName": data['firstName'], "lastName": data['lastName'], "email": data['email']}
        account_needs_to_be_activated_msg = _(
            "It needs to be revisited and activated by an administrator, you'll receive an email when your cooperative is active and ready to be used.")

        return Response({'created_coop_success_msg': created_coop_success_msg,
                         'account_needs_to_be_activated_msg': account_needs_to_be_activated_msg},
                        status=status.HTTP_200_OK)


class PartnerView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of partners for the current cooperative.

    create:
    Creates a partner for the current cooperative.

    destroy:
    Removes the selected partner from the current cooperative.
    """

    serializer_class = PartnerSerializer

    def get_queryset(self):
        queryset = Partner.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset

    @transaction.atomic
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
            logo_url = public_url + settings.STATIC_URL + "images/coobs.png"
            context = {'cooperative': CooperativeSerializer(cooperative).data, 'password': password,
                       'public_url': public_url, 'email': partner.email, "logo_url": logo_url}
            text_template = get_template('partner_created_email_template.txt')
            text_content = text_template.render(context)
            html_template = get_template('partner_created_email_template.html')
            html_content = html_template.render(context)
            subject = _('Hello %(partner_name)s, you have been added to COOBS!') % {"partner_name": partner.first_name}
            email = EmailMultiAlternatives(subject, text_content,
                                           getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
                                           [partner.email])
            email.content_subtype = "html"
            email.attach_alternative(html_content, "text/html")
            email.send()

        try:
            partner.save()
            send_email()
        except Exception as errors:
            # return Response(errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #FIXME this way it rollbacks the transaction, do we have a way to handle what we send to the client?
            raise IntegrityError("Partner asked to be created but it FAILED.", errors)

        return Response('Partner asked to be created', status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        partner = self.get_object()

        if partner.id == request.user.id:
            return Response(data={'detail': _("Current logged in user can not delete it self.")},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(partner)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DashboardView(viewsets.ViewSet):
    """
    list:
    Returns a dashboard for the selected period {periodId as query param} and current cooperative. It shows information such as: 
    performed and pending actions, investment budget, graphs summarizing actions (per month, per partner, etc)

    """

    def list(self, request):
        cooperative_id = request.user.cooperative_id
        empty_response = {'period': [], 'actions': [], 'principles': [], 'charts': {
            'cards_data': [],
            'all_principles_data': [],
            'progress_data': {'investmentProgressData': {}, 'periodProgressData': {}, 'actionsProgressData': {}},
            'actions_by_partner': [],
            'monthly_investment_by_date': [],
            'monthly_actions_by_principle': []            
        }, 'all_periods': []}

        all_periods_data = Period.objects.filter(cooperative=cooperative_id)
        all_periods_serializer = PeriodSerializer(all_periods_data, many=True)
        if not all_periods_serializer.data:
            return Response(empty_response)

        period_id = request.query_params.get('periodId', None)
        if period_id is not None:
            period_data = next((period for period in all_periods_serializer.data if period['id'] == int(period_id)),
                               None)
        else:
            period_data = get_current_period(all_periods_serializer.data)

        if not period_data:
            return Response(empty_response)

        date_from = period_data['date_from']
        date_to = period_data['date_to']
        action_data = Action.get_current_actions(cooperative_id, date_from, date_to).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)

        date = datetime.today() if str(datetime.today()) <= date_to and str(datetime.today()) >= date_from else date_to
        done_actions_data = Action.get_current_actions(cooperative_id, date_from, date).order_by('date')

        principle_data = Principle.objects.filter(visible=True)
        principle_serializer = PrincipleSerializer(principle_data, many=True)

        partner_data = Partner.objects.filter(cooperative=cooperative_id, action__date__gte=date_from,
                                              action__date__lte=date_to).annotate(total=Count('username')).order_by()

        actions_by_principles_data = Principle.objects.filter(cooperative=cooperative_id,
                                                              action__date__gte=date_from,
                                                              action__date__lte=date_to).annotate(
            total=Count('id')).order_by()

        principles = {principle['id']: principle['name_key'] for principle in list(principle_serializer.data)}

        charts = {
            'cards_data': get_cards_data(action_data, done_actions_data, period_data),
            'all_principles_data': get_all_principles_data(actions_by_principles_data, principles),
            'progress_data': get_progress_data(action_data, done_actions_data, period_data),
            'actions_by_partner': get_actions_by_partner(partner_data),
            'monthly_hours_by_date': get_monthly_hours(done_actions_data),
            'monthly_investment_by_date': get_monthly_investment_by_principle(done_actions_data,
                                                                              date_from, principles),
            'monthly_actions_by_principle': get_monthly_actions_by_principle(done_actions_data,
                                                                             datetime.strptime(date_from, '%Y-%m-%d'), 
                                                                             principles),
        }

        return Response(
            {'period': period_data, 'actions': action_serializer.data, 'principles': principle_serializer.data,
             'charts': charts, 'all_periods': all_periods_serializer.data})

class BalanceView(viewsets.ViewSet):
    """
    list:
    Returns the cooperative balance for the selected period {periodId as query param} and cooperative.
    """

    def list(self, request):
        cooperative_id = request.user.cooperative_id
        empty_response = {'period': [], 'actions': [], 'all_periods': []}

        all_periods_data = Period.objects.filter(cooperative=cooperative_id)
        all_periods_serializer = PeriodSerializer(all_periods_data, many=True)
        if not all_periods_serializer.data:
            return Response(empty_response)

        period_id = request.query_params.get('periodId', None)
        if period_id is not None:
            period_data = next((period for period in all_periods_serializer.data if period['id'] == int(period_id)),
                               None)
        else:
            period_data = get_current_period(all_periods_serializer.data)

        if not period_data:
            return Response(empty_response)
            
        action_data = Action.get_current_actions(cooperative_id, period_data['date_from'],
                                                 period_data['date_to']).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)

        actions = []
        [[actions.append({**action, 'principle_name_key': action_principle['name_key'], 'principle': action_principle['id']}) for
          action_principle in action['principles']] for action in action_serializer.data]

        total_invested = 0 if len(actions) == 0 else functools.reduce(lambda a, b: a + b,
                                                                      [action.invested_money for action in
                                                                       list(action_data)])
        totalHoursInvested = 0 if len(actions) == 0 else functools.reduce(lambda a, b: a + b,
                                                                      [action.invested_hours for action in
                                                                       list(action_data)])
        return Response({'period': period_data, 'actions': actions, 'all_periods': all_periods_serializer.data,
                         'total_invested': total_invested, 'totalHoursInvested': totalHoursInvested})


class ActionsRankingView(viewsets.ViewSet):
    """
    list:
    Returns a summary of public actions (for current year) performed by all the cooperatives part of COOBS (sorted in a ranking).
    """    
    def list(self, request):
        first_day_of_year = date(datetime.today().year, 1, 1)
        visible_principles = Principle.objects.filter(visible=True)
        visible_principles_ids = visible_principles.values('id')

        actions_by_coop_data = Action.objects.filter(date__gte=first_day_of_year, public=True,
                                                     principles__in=visible_principles_ids).values('cooperative',
                                                                                                   'cooperative__name',
                                                                                                   'cooperative__business_name',
                                                                                                   'principles').annotate(
            actions_count=Count('principles')).order_by('cooperative')
        for action in actions_by_coop_data:
            principle = visible_principles.get(id=action['principles'])
            action['principle_name_key'] = principle.main_principle.name_key
        actions_by_coop_serializer = ActionsByCoopSerializer(actions_by_coop_data, many=True)

        main_principle_data = MainPrinciple.objects.all()
        main_principle_serializer = MainPrincipleSerializer(main_principle_data, many=True)

        return Response({'actions': actions_by_coop_serializer.data, 'principles': main_principle_serializer.data})


class PartnerStatsView(viewsets.ViewSet):
    """
    list:
    Returns a dashboard for the selected period {periodId as query param} and current partner. It shows information such as: 
    performed and pending actions, invested hours, graphs summarizing actions

    """

    def list(self, request):
        user_id = request.user.id
        cooperative_id = request.user.cooperative_id
        empty_response = {'period': [], 'actions': [], 'principles': [], 'charts': {
            'cards_data': [],
            'all_principles_data': [],
            'progress_data': {'investmentProgressData': {}, 'periodProgressData': {}, 'actionsProgressData': {}},
            'actions_by_partner': [],
            'monthly_investment_by_date': [],
            'monthly_actions_by_principle': []            
        }, 'all_periods': []}

        all_periods_data = Period.objects.filter(cooperative=cooperative_id)
        all_periods_serializer = PeriodSerializer(all_periods_data, many=True)
        if not all_periods_serializer.data:
            return Response(empty_response)

        period_id = request.query_params.get('periodId', None)
        if period_id is not None:
            period_data = next((period for period in all_periods_serializer.data if period['id'] == int(period_id)),
                               None)
        else:
            period_data = get_current_period(all_periods_serializer.data)

        if not period_data:
            return Response(empty_response)

        date_from = period_data['date_from']
        date_to = period_data['date_to']
        action_data = Action.get_current_actions(cooperative_id, date_from, date_to, user_id).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)
        date = datetime.today() if str(datetime.today()) <= date_to and str(datetime.today()) >= date_from else date_to
        done_actions_data = Action.get_current_actions(cooperative_id, date_from, date, user_id).order_by('date')

        principle_data = Principle.objects.filter(visible=True, cooperative=cooperative_id)
        principle_serializer = PrincipleSerializer(principle_data, many=True)

        actions_by_principles_data = Action.objects.filter(cooperative=cooperative_id, 
                                    principles__visible=True, date__gte=date_from,   
                                    date__lte=date_to, partners_involved__in=[user_id]).values('principles').annotate(total=Count('principles')).order_by()

        principles = {principle['id']: principle['name_key'] for principle in list(principle_serializer.data)}

        charts = {
            'cards_data': get_cards_data(action_data, done_actions_data, period_data),
            'all_principles_data': get_all_principles_data_for_current_partner(actions_by_principles_data, principles),
            'progress_data': get_progress_data(action_data, done_actions_data, period_data, request.user),
            'monthly_hours_by_date': get_monthly_hours(done_actions_data),
            'monthly_investment_by_date': get_monthly_investment_by_principle(done_actions_data,
                                                                              date_from, principles),
            'monthly_actions_by_principle': get_monthly_actions_by_principle(done_actions_data,
                                                                             datetime.strptime(date_from, '%Y-%m-%d'), 
                                                                             principles)
        }

        return Response(
            {'period': period_data, 'actions': action_serializer.data, 'principles': principle_serializer.data,
             'charts': charts, 'all_periods': all_periods_serializer.data})

class PublicActionView(views.APIView):
    """
    get:
    Returns public actions for this year, all the principles and actions by principles.

    """
    permission_classes = []
    serializer_class = ActionSerializer

    def get(self, request):
        starting_day_of_current_year = datetime.now().date().replace(month=1, day=1)
        ending_day_of_current_year = datetime.now().date().replace(month=12, day=31)
        action_data = Action.get_public_actions(starting_day_of_current_year, ending_day_of_current_year).order_by('date')
        action_serializer = ActionSerializer(action_data, many=True)

        principle_data = Principle.objects.filter(visible=True)
        principle_serializer = PrincipleSerializer(principle_data, many=True)

        actions_by_principles_data = Action.objects.filter(principles__visible=True).values('principles').annotate(total=Count('principles')).order_by()

        return Response({
                'actions': action_serializer.data, 
                'principles': principle_serializer.data,
                'actions_by_principles_data': actions_by_principles_data
            })

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    public_url = "{}://{}".format(settings.WEB_PROTOCOL, settings.WEB_URL)
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'public_url': public_url,
        'reset_password_url': "{}{}?token={}".format(public_url, '/app/#/new-password', reset_password_token.key)
    }
    email_html_message = render_to_string('reset_password_email_template.html', context)
    email_plaintext_message = render_to_string('reset_password_email_template.txt', context)

    msg = EmailMultiAlternatives(
        "Reset your password on COOBS!",
        email_plaintext_message,
        getattr(settings, "EMAIL_FROM_ACCOUNT", "test@console.com"),
        [reset_password_token.user.email]
    )

    msg.attach_alternative(email_html_message, "text/html")
    msg.send()