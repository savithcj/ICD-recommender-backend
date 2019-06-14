from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code
from django.db import transaction
import random


class Command(BaseCommand):
    help = '''Adds random numbers to times_coded in Code table,
              or resets to all zeros, depending on the argument.'''

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', type=str)

    def handle(self, *args, **options):
        mode = options['mode']
        codes = Code.objects.all()
        with transaction.atomic():
            for code in codes:
                if mode == "random":
                    code.times_coded = random.randint(1, 1001)
                else:
                    code.times_coded = 0
                code.save()
            if mode == "random":
                print("set all times_coded to a random int")
            else:
                print("set all times_coded to 0")
