from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code, Rule
from django.db import transaction
from collections import defaultdict
import random


class Command(BaseCommand):
    help = ('Sets code usage numbers to zeros, random numbers, or raw DAD numbers. '
            'Sets rules to zeros or random numbers (random if dad is selected)')

    def add_arguments(self, parser):
        parser.add_argument('-m', '--mode', type=str)

    def handle(self, *args, **options):
        mode = options['mode']
        # Getting all code and rule objects
        codes = Code.objects.all()
        rules = Rule.objects.all()
        with transaction.atomic():
            print("Reading DAD usage numbers")
            dxCounts = dict()
            with open('secret/DAD_dx_counts.csv', 'r') as f:
                for line in f.readlines():
                    code, count = line.strip().split(',')
                    count = int(count)
                    dxCounts[code] = count
            for code in codes:
                code.times_coded_dad = dxCounts.get(code.code, 0)
            # set code usage numbers
            if mode == "random":
                print("Setting code usage numbers to a random counts")
                for code in codes:
                    code.times_coded = random.randint(1, 1001)
            else:
                print("Setting code usage numbers to 0")
                for code in codes:
                    code.times_coded = 0
            for code in codes:
                code.save()

        with transaction.atomic():
           # set rule usage numbers
            if mode == "random":
                print("Setting rule usage counts to random counts")
                for rule in rules:
                    rule.num_accepted = random.randint(1, 1001)
                    rule.num_rejected = random.randint(1, 1001)
                    rule.num_suggested = rule.num_accepted + rule.num_rejected + random.randint(1, 1001)
            else:
                print("Setting rule usage counts to 0")
                for rule in rules:
                    rule.num_accepted = 0
                    rule.num_rejected = 0
                    rule.num_suggested = 0
            for rule in rules:
                rule.save()
        print("Done")
