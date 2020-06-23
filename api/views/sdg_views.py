import functools
from datetime import datetime, date
from .views_utils import *

import requests
from django.db import IntegrityError
from django.db.models import Count
from django.utils.translation import gettext as _
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Action, Period, Cooperative, SustainableDevelopmentGoal, SDGObjective
from api.serializers import ActionSerializer, PeriodSerializer, SustainableDevelopmentGoalSerializer, SDGObjectiveSerializer


class SustainableDevelopmentGoalView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of SustainableDevelopmentGoal for the current cooperative.

    create:
    Creates a SustainableDevelopmentGoal for the current cooperative.

    destroy:
    Removes the selected SustainableDevelopmentGoal.
    """            
    serializer_class = SustainableDevelopmentGoalSerializer

    def get_queryset(self):
        return SustainableDevelopmentGoal.objects.all()


class SDGObjectiveView(viewsets.ModelViewSet):
    """
    list:
    Returns the list of SDG objectives for the current cooperative.

    create:
    Creates a SDG objective for the current cooperative.

    destroy:
    Removes the selected SDG objective.
    """
    serializer_class = SDGObjectiveSerializer

    def get_queryset(self):
        queryset = SDGObjective.objects.filter(cooperative=self.request.user.cooperative_id)
        return queryset

    def create(self, request):
        sdg_objective_serializer = SDGObjectiveSerializer(data=request.data)

        if not sdg_objective_serializer.is_valid():
            return Response(sdg_objective_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        sdg_objective_data = SDGObjective.objects.create(**sdg_objective_serializer.validated_data)

        setattr(sdg_objective_data, 'cooperative_id', request.user.cooperative.id)
        try:
            sdg_objective_data.save()
        except IntegrityError:
            return Response(data={'detail': _("This objective already exists, please modify the existing one.")}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("SDG_OBJ_CREATED", status=status.HTTP_200_OK)


class SDGBalanceView(viewsets.ViewSet):
    """
    list:
    Returns the SDG balance for the selected period {periodId as query param} and cooperative.
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
        [[actions.append({**action, 'objective_name_key': action_ods['name_key'], 'objective': action_ods['id']}) for
          action_ods in action['sustainable_development_goals']] for action in action_serializer.data]
        
        total_invested = sum([float(action['invested_money']) for action in action_serializer.data if len(action['sustainable_development_goals'])])

        return Response({'period': period_data, 'actions': actions, 'all_periods': all_periods_serializer.data,
                         'total_invested': total_invested})


class SDGMonitoringView(viewsets.ViewSet):
    """
    list:
    Returns SDGs objectives for the selected period {periodId as query param} and cooperative.
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
            period_id = period_data['id']

        if not period_data:
            return Response(empty_response)
            
        sdg_objectives_data = SDGObjective.objects.filter(cooperative=cooperative_id, period=period_id)
        sdg_objectives_serializer = SDGObjectiveSerializer(sdg_objectives_data, many=True)
        
        actions = Action.objects.filter(cooperative=cooperative_id, date__gte=period_data['date_from'], date__lte=period_data['date_to'])
        actions_serializer = ActionSerializer(actions, many=True)

        def filterData(sdg):
            return list(filter(lambda x: sdg in list(map(lambda x:x['id'], x['sustainable_development_goals'])), actions_serializer.data))

        monitoring_data = []
        for sdg_objective in sdg_objectives_serializer.data:
            data = filterData(sdg_objective['sustainable_development_goal'])
            invested_hours = sum(map(lambda x: float(x['invested_hours']), data))
            invested_money = sum(map(lambda x: float(x['invested_money']), data))

            monitoring_data.append({**sdg_objective, 
                'invested_hours': invested_hours,
                'invested_money': invested_money,
                'performed_actions': len(data)})

        return Response({'period': period_data, 'monitoring_data': monitoring_data, 'all_periods': all_periods_serializer.data})
