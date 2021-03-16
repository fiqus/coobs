import datetime
import random
from django.core.management.base import BaseCommand, CommandError
from api.models import Cooperative, Action, Principle, Partner, SustainableDevelopmentGoal


class Command(BaseCommand):
    help = """command used to generate test actions, receives coop_id, quantity, 
        a boolean value to indicate if you would like to associate multiple principles to each action (the quantity of principles to associate is generated randomly)
        and a boolean value to indicate if you would like to associate multiple SDGs to each action (the quantity of SDGs to associate is generated randomly) """

    def add_arguments(self, parser):
        parser.add_argument('coop_id', type=int, help='for which cooperative id you want to add actions?')
        parser.add_argument('quantity', type=int, help='how many actions do you want to create?')
        parser.add_argument('associate_multiple_principles', type=int, default=0, help=' indicate 1 if you would like to associate multiple principles to each action (the quantity of principles to associate is generated randomly)')
        parser.add_argument('associate_multiple_sdg', type=int, default=0, help=' indicate 1 if you would like to associate multiple SDGs to each action (the quantity of SDGs to associate is generated randomly)')

    def handle(self, *args, **options):
        try:
            sdg = list(SustainableDevelopmentGoal.objects.all())
            principles = list(Principle.objects.filter(cooperative=options['coop_id']))
            partners = list(Partner.objects.filter(cooperative=options['coop_id']))
            investments = random.sample(range(1, 1000), options['quantity'])
            coop = Cooperative.objects.get(pk=options['coop_id'])

            for n in range(options['quantity']):
                action = Action(date=datetime.date.today(), name=f"Action {n}",
                                description=f"Action {n} description", invested_money=random.choice(investments),
                                cooperative=coop, public=True)
                action.save()
                associated_principles = []
                associated_sdg = []
                if options['associate_multiple_principles']:
                    random.seed()
                    quantity = random.randint(1, principles.__len__()-1)
                    for i in range(quantity):
                        associated_principles.append(random.choice(principles))
                else:
                    associated_principles.append(random.choice(principles))

                if options['associate_multiple_sdg']:
                    random.seed()
                    quantity = random.randint(1, sdg.__len__()-1)
                    for i in range(quantity):
                        associated_sdg.append(random.choice(sdg))
                else:
                    associated_sdg.append(random.choice(sdg))

                action.principles.set(associated_principles)
                action.sustainable_development_goals.set(associated_sdg)
                action.save()

                if partners:
                    action.partners_involved.add(random.choice(partners))
                    action.save()

        except Cooperative.DoesNotExist:
            raise CommandError(f"Ups! The cooperative with id {options['coop_id']} does not exist")
