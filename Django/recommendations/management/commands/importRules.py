from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Rule
from django.db import transaction
import pandas as pd
import numpy as np
from utils.ImportDataFile import readDataFile


class Command(BaseCommand):
    help = 'Imports the oracle rules in addition to extra mined rules'

    def handle(self, *args, **options):
        print("Reading rules...")
        Rule.objects.all().delete()  # Deletes all existing rules before importing

        with transaction.atomic():  # Saves all of the rules at once
            # Adding the additional mined rules
            print("Adding in rules mined")
            for line in readDataFile("output_rules_cleaned.csv")[1:]:
                line = line.strip().split(",")
                potentialRule = (line[0].split("_")[0], line[1].split("_")[0], line[1].split("_")[
                    3], float(line[1].split("_")[1]), float(line[1].split("_")[2]))
                if potentialRule not in ruleSet:  # Checking to ensure there is no duplicate rules
                    rule = Rule.objects.create(lhs=line[0].split("_")[0],
                                               rhs=line[1].split("_")[0],
                                               gender=line[1].split("_")[3],
                                               min_age=line[1].split("_")[1],
                                               max_age=line[1].split("_")[2],
                                               support=line[2],
                                               confidence=line[3])
                    ruleSet.add(potentialRule)
                    rule.save()
        print("Done")
