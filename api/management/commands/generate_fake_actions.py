import datetime
import random
from django.core.management.base import BaseCommand, CommandError
from api.models import Cooperative, Action, Principle, Partner


class Command(BaseCommand):
    help = "command used to generate test actions"

    def add_arguments(self, parser):
        parser.add_argument('coop_id', type=int)
        parser.add_argument('quantity', type=int)

    def handle(self, *args, **options):
        try:
            principles = list(Principle.objects.all())
            partners = list(Partner.objects.all())
            investments = random.sample(range(1, 1000), options['quantity'])
            coop = Cooperative.objects.get(pk=options['coop_id'])

            for n in range(options['quantity']):
                action = Action(date=datetime.date.today(), name="Action {}".format(n),
                                description="Action {} description".format(n), invested_money=random.choice(investments),
                                cooperative=coop, public=True,
                                principle=random.choice(principles))
                action.save()

                if partners:
                    action.partners_involved.add(random.choice(partners))
                    action.save()

        except Cooperative.DoesNotExist:
            raise CommandError("Ups! The cooperative with id {} does not exist".format(options['coop_id']))
