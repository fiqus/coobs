from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Func
from django.db.models import Count
from collections import OrderedDict
import datetime 
import requests
import functools 

class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()

class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


#CARDS

def get_cards_data(action_data, done_actions_data, period_data):
    done_actions = len(done_actions_data)
    total_invested = functools.reduce(lambda a, b : a + b, [action.invested_money for action in done_actions_data])
    pending_actions = len(action_data) - len(done_actions_data)
    promotion_fund_percentage = round(total_invested / period_data.actions_budget * 100, 2)
    
    return {'done_actions': done_actions, 'total_invested': total_invested, 'pending_actions': pending_actions, 'promotion_fund_percentage': promotion_fund_percentage}

#ALL PRINCIPLES ACTIONS DATA
def get_all_principles_data(done_actions_data, principles):
    totals = list(done_actions_data.values('principle_id').annotate(total=Count('id')).order_by())
    result =OrderedDict({ principles[item['principle_id']]: item['total'] for item in totals})

    return {'labels': result.keys(), 'series': result.values()}


#MONTHLY ACTIONS BY PRINCIPLE

def get_monthly_actions_by_principle(action_data, date_from, principles):
    date = datetime.date.today()

    actions_by_principle_and_month = list(action_data.annotate(m=Month('date'), y=Year('date')) \
        .values('m', 'y', 'principle_id') \
        .annotate(total=Count('id')) \
        .order_by())
    
    months_labels = list(create_date_range(date_from, date))

    
    actions_by_principles_by_month_list = [{'date': f"{action['m']:02d}" + "-" + str(action['y']), 'count': action['total'], 'principle': principles[action['principle_id']]} for action in actions_by_principle_and_month]
    
    data = {principle: [0]*len(months_labels) for principle in principles.values()}

    for action in actions_by_principles_by_month_list:
        index = months_labels.index(action['date'])
        data[action['principle']][index] = action['count'] 
    result = [{'name': principle, 'data': data[principle]} for principle in data]
    
    return {'result': result, 'labels': months_labels}

def create_date_range(start, end):
    return OrderedDict(((start + datetime.timedelta(_)).strftime(r"%m-%Y"), None) for _ in range((end - start).days)).keys()