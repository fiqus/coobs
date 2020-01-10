from django.core.management.base import BaseCommand, CommandError
import string
import random


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        try:
            # Get ascii Characters numbers and punctuation (minus quote characters as they could terminate string).
            chars = ''.join([string.ascii_letters, string.digits, string.punctuation])\
                .replace('\'', '').replace('"', '').replace('\\', '')

            secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(50)])
            print(secret_key)
        except:
            raise CommandError("Ups! Couldn't generate the secret key")
