from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code, Rule
from django.db import transaction
import random


class Command(BaseCommand):
    help = '''Adds random numbers to times_coded in Code table,
              or resets to all zeros, depending on the argument.'''

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', type=str)

    def handle(self, *args, **options):
        mode = options['mode']
        # Getting all code and rule objects
        codes = Code.objects.all()
        rules = Rule.objects.all()
        if mode == "random":
            print("Setting use numbers to a random int")
        else:
            print("Setting use numbers to 0")
        with transaction.atomic():
            print("Setting codes")
            for code in codes:
                if mode == "random":
                    # Setting codes to random
                    code.times_coded = random.randint(1, 1001)
                else:
                    # Setting codes to 0
                    code.times_coded = 0
                code.save()
            print("Setting rules")
            for rule in rules:
                if mode == "random":
                    # Setting accepted, rejected and suggested to random numbers
                    rule.num_accepted = random.randint(1, 1001)
                    rule.num_rejected = random.randint(1, 1001)
                    rule.num_suggested = rule.num_accepted + rule.num_rejected + random.randint(1, 1001)
                else:
                    # Setting accepted, rejected and suggested to 0
                    rule.num_accepted = 0
                    rule.num_rejected = 0
                    rule.num_suggested = 0
                # Saving the rule
                rule.save()
        print("Done")
