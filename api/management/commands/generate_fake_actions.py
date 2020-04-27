import datetime
import random
from django.core.management.base import BaseCommand, CommandError
from api.models import Cooperative, Action, Principle, Partner, SustainableDevelopmentGoal


class Command(BaseCommand):
    help = """command used to generate test actions, receives coop_id, quantity, 
        a boolean value to indicate if you would like to associate multiple principles to each action (the quantity of principles to associate is generated randomly)
        and a boolean value to indicate if you would like to associate multiple ODSs to each action (the quantity of ODSs to associate is generated randomly) """

    def add_arguments(self, parser):
        parser.add_argument('coop_id', type=int, help='for which cooperative id you want to add actions?')
        parser.add_argument('quantity', type=int, help='how many actions do you want to create?')
        parser.add_argument('associate_multiple_principles', type=int, default=0, help=' indicate 1 if you would like to associate multiple principles to each action (the quantity of principles to associate is generated randomly)')
        parser.add_argument('associate_multiple_ods', type=int, default=0, help=' indicate 1 if you would like to associate multiple ODSs to each action (the quantity of ODSs to associate is generated randomly)')

    def handle(self, *args, **options):
        try:
            ods = list(SustainableDevelopmentGoal.objects.all())
            principles = list(Principle.objects.filter(cooperative=options['coop_id']))
            partners = list(Partner.objects.filter(cooperative=options['coop_id']))
            investments = random.sample(range(1, 1000), options['quantity'])
            coop = Cooperative.objects.get(pk=options['coop_id'])

            for n in range(options['quantity']):
                action = Action(date=datetime.date.today(), name="Action {}".format(n),
                                description="Action {} description".format(n), invested_money=random.choice(investments),
                                cooperative=coop, public=True)
                action.save()
                associated_principles = []
                associated_ods = []
                if options['associate_multiple_principles']:
                    random.seed()
                    quantity = random.randint(1, principles.__len__()-1)
                    for i in range(quantity):
                        associated_principles.append(random.choice(principles))
                else:
                    associated_principles.append(random.choice(principles))

                if options['associate_multiple_ods']:
                    random.seed()
                    quantity = random.randint(1, ods.__len__()-1)
                    for i in range(quantity):
                        associated_ods.append(random.choice(ods))
                else:
                    associated_ods.append(random.choice(ods))

                action.principles.set(associated_principles)
                action.sustainable_development_goals.set(associated_ods)
                action.save()

                if partners:
                    action.partners_involved.add(random.choice(partners))
                    action.save()

        except Cooperative.DoesNotExist:
            raise CommandError("Ups! The cooperative with id {} does not exist".format(options['coop_id']))
