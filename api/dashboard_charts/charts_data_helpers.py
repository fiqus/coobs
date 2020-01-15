from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Func
from django.db.models import Count, Sum
from collections import OrderedDict
import datetime 
import requests
import functools
import time

def t(dt):
  return time.mktime(dt.timetuple())

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

#PROGRESS

def get_progress_data(action_data, done_actions_data, period_data):
    date = datetime.date.today()
    period_progress_data = {
        "date_from": period_data.date_from, 
        "date_to": period_data.date_to,
        "period_progress": round((t(date) - t(period_data.date_from)) / (t(period_data.date_to)- t(period_data.date_from)) * 100, 2)
    }
    actions_progress_data = {
        "actions_done": len(done_actions_data), 
        "total_actions": len(action_data), 
        "actions_progress": round(len(done_actions_data)/len(action_data) * 100, 2)
    }
    invested = round(functools.reduce(lambda a, b : a + b, [action.invested_money for action in done_actions_data]), 2)
    investment_progress_data = {
        "invested": invested, 
        "budget": period_data.actions_budget, 
        "investment_progress": round(invested / period_data.actions_budget * 100, 2)
    }
    
    return {'period_progress_data': period_progress_data, 'actions_progress_data': actions_progress_data, "investment_progress_data": investment_progress_data}

#ALL PRINCIPLES ACTIONS DATA
def get_all_principles_data(done_actions_data, principles):
    totals = list(done_actions_data.values('principle_id').annotate(total=Count('id')).order_by())
    result =OrderedDict({ principles[item['principle_id']]: item['total'] for item in totals})

    return {'labels': result.keys(), 'series': result.values()}

#ACTIONS BY PARTNER
def get_actions_by_partner(partner_data):
    partners = OrderedDict({'%s %s' % (partner.first_name, partner.last_name): partner.total for partner in list(partner_data)})
    
    return {'labels': partners.keys(), 'result': [{'name': 'Acciones Realizadas', 'data': partners.values()}]}



#MONTHLY INVESTMENT BY PRINCIPLE

def get_monthly_investment_by_principle(action_data, date_from, principles):
    date = datetime.date.today()

    actions_amount_by_principle_and_month = list(action_data.annotate(m=Month('date'), y=Year('date')) \
        .values('m', 'y', 'principle_id') \
        .annotate(total=Sum('invested_money')) \
        .order_by())
    
    months_labels = list(create_date_range(date_from, date))

    
    actions_amount_by_principle_and_month = [{'date': f"{action['m']:02d}" + "-" + str(action['y']), 'sum': action['total'], 'principle': principles[action['principle_id']]} for action in actions_amount_by_principle_and_month]
    
    data = {principle: [0]*len(months_labels) for principle in principles.values()}

    for action in actions_amount_by_principle_and_month:
        index = months_labels.index(action['date'])
        data[action['principle']][index] = action['sum'] 
    result = [{'name': principle, 'data': data[principle]} for principle in data]
    
    return {'labels': months_labels, 'result': result}


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
    
    return {'labels': months_labels, 'result': result}

def create_date_range(start, end):
    return OrderedDict(((start + datetime.timedelta(_)).strftime(r"%m-%Y"), None) for _ in range((end - start).days)).keys()