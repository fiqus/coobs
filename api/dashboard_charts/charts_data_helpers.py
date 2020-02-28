from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Func
from django.db.models import Count, Sum
from collections import OrderedDict
from itertools import accumulate
from datetime import datetime, timedelta
import requests
import functools
import time


def t(dt):
    return time.mktime(dt.timetuple())


class Day(Func):
    function = 'EXTRACT'
    template = '%(function)s(DAY from %(expressions)s)'
    output_field = models.IntegerField()


class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR from %(expressions)s)'
    output_field = models.IntegerField()


# CARDS
def get_cards_data(action_data, done_actions_data, period_data):
    done_actions = len(done_actions_data)
    total_invested = 0 if len(done_actions_data) == 0 else functools.reduce(lambda a, b: a + b,
                                                                            [action.invested_money for action in
                                                                             done_actions_data])
    total_hours_invested = 0 if len(done_actions_data) == 0 else functools.reduce(lambda a, b: a + b,
                                                                            [action.invested_hours for action in
                                                                             done_actions_data])
    pending_actions = len(action_data) - len(done_actions_data)
    promotion_fund_percentage = round(float(total_invested) / float(period_data['actions_budget']) * 100, 2)

    return {'done_actions': done_actions, 'total_invested': total_invested, 'total_hours_invested': total_hours_invested,
            'pending_actions': 0 if pending_actions < 0 else pending_actions,
            'promotion_fund_percentage': promotion_fund_percentage}


# PROGRESS
def get_progress_data(action_data, done_actions_data, period_data, user=None):
    date = datetime.today()
    period_progress_data = {
        "date_from": period_data['date_from'],
        "date_to": period_data['date_to'],
        "period_progress": round((t(date) - t(datetime.strptime(period_data['date_from'], '%Y-%m-%d'))) / (
                    t(datetime.strptime(period_data['date_to'], '%Y-%m-%d')) - t(
                datetime.strptime(period_data['date_from'], '%Y-%m-%d'))) * 100, 2)
    }
    actions_progress_data = {
        "actions_done": len(done_actions_data),
        "total_actions": len(action_data),
        "actions_progress": 0 if len(action_data) == 0 else round(len(done_actions_data) / len(action_data) * 100, 2)
    }
    invested = 0 if len(done_actions_data) == 0 else round(
        functools.reduce(lambda a, b: a + b, [action.invested_money for action in done_actions_data]), 2)
    invested_hours = 0 if len(done_actions_data) == 0 else round(
        functools.reduce(lambda a, b: a + b, [action.invested_hours for action in done_actions_data]), 2)

    investment_progress_data = {
        "invested": invested,
        "budget": period_data['actions_budget'],
        "partner_hours_goal": 0,
        "investment_progress": round(float(invested) / float(period_data['actions_budget']) * 100, 2)
    }
    if user:
        investment_progress_data['partner_hours_goal'] = user.hours_to_invest
        investment_progress_data['investment_progress'] = round(float(invested_hours) / float(user.hours_to_invest) * 100, 2)

    return {'period_progress_data': period_progress_data, 'actions_progress_data': actions_progress_data,
            "investment_progress_data": investment_progress_data}


# ALL PRINCIPLES ACTIONS DATA
def get_all_principles_data(actions_by_principles_data, principles):
    actions_by_principle = OrderedDict(
        {principle.main_principle.name_key: principle.total for principle in list(actions_by_principles_data)})
    for principle in principles.values():
        if principle not in actions_by_principle.keys():
            actions_by_principle[principle] = 0

    return {'labels': actions_by_principle.keys(), 'series': actions_by_principle.values()}

# ALL PRINCIPLES ACTIONS DATA
def get_all_principles_data_for_current_partner(actions_by_principles_data, principles):
    actions_list = list(actions_by_principles_data)
    actions_by_principle = OrderedDict(
        {principle['principles']: principle['total'] for principle in actions_list})
    for principle in principles.keys():
        if principle not in actions_by_principle.keys():
            actions_by_principle[principle] = 0

    return {'labels': principles.values(), 'series': actions_by_principle.values()}

# ACTIONS BY PARTNER
def get_actions_by_partner(partner_data):
    partners = OrderedDict(
        {'%s %s' % (partner.first_name.lower().capitalize(), partner.last_name.lower().capitalize()): partner.total for partner in list(partner_data)})

    result = {'labels': partners.keys(),
              'result': [{'name': 'Acciones Realizadas', 'data': partners.values()}]} if not len(
        partners.values()) == 0 else {}
    return result

#MONTHLY HOURS
def get_monthly_hours(action_data):
    actions_by_date = list(action_data.values('date', 'invested_hours') \
                            .order_by())

    dates_list = [action['date'] for action in actions_by_date]
    categories = list(set(dates_list))
    categories.sort()

    actions_by_date = [{'date': action['date'], 'hours': action['invested_hours']} for action in actions_by_date]

    hours_by_date = {}
    for action in actions_by_date:
        if action['date'] in hours_by_date.keys():
            hours_by_date[action['date']] += action['hours']
        else:
            hours_by_date[action['date']] = action['hours']

    result = {'name': 'all_principles', 'data': []}
    for date in hours_by_date.keys():
        result['data'].append(hours_by_date[date])

    return {'labels': categories, 'result': [result]}

# MONTHLY INVESTMENT BY PRINCIPLE

def get_monthly_investment_by_principle(action_data, date_from, principles):
    actions_amount_by_date = list(action_data.values('date', 'invested_money') \
                                  .order_by())

    dates_list = [action['date'] for action in actions_amount_by_date]
    categories = list(set(dates_list))
    categories.sort()

    actions_amount_by_date = [{'date': action['date'], 'amount': action['invested_money']} for action in actions_amount_by_date]
    amounts_by_date = {}
    for action in actions_amount_by_date:
        if action['date'] in amounts_by_date.keys():
            amounts_by_date[action['date']] += action['amount']
        else:
            amounts_by_date[action['date']] = action['amount']

    result = {'name': 'all_principles', 'data': []}
    for date in amounts_by_date.keys():
        result['data'].append(amounts_by_date[date])

    return {'labels': categories, 'result': [result]}


def sum_series_numbers(item, serie):
    return item + serie[serie.index(item) + 1]


# MONTHLY ACTIONS BY PRINCIPLE

def get_monthly_actions_by_principle(action_data, date_from, principles):
    date = datetime.today()

    actions_by_principle_and_month = list(action_data.annotate(m=Month('date'), y=Year('date')) \
                                          .values('m', 'y', 'principles') \
                                          .annotate(total=Count('id')) \
                                          .order_by())

    months_labels = list(create_date_range(date_from, date))

    actions_by_principles_by_month_list = [
        {'date': f"{action['m']:02d}" + "-" + str(action['y']), 'count': action['total'],
         'principle': principles[action['principles']]} for action in actions_by_principle_and_month]

    data = {principle: [0] * len(months_labels) for principle in principles.values()}

    for action in actions_by_principles_by_month_list:
        index = months_labels.index(action['date'])
        data[action['principle']][index] = action['count']
    result = [{'name_key': principle, 'data': data[principle]} for principle in data]

    return {'labels': months_labels, 'result': result}


def create_date_range(start, end):
    return OrderedDict(((start + timedelta(_)).strftime(r"%m-%Y"), None) for _ in range((end - start).days)).keys()
