from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Rule
from django.db import transaction
import pandas as pd
import numpy as np
from utils.ImportDataFile import readDataFile


class Command(BaseCommand):
    help = 'Imports the oracle rules in addition to extra mined rules'

    def handle(self, *args, **options):
        print("Adding in Oracle rules")
        Rule.objects.all().delete()  # Deletes all existing rules before importing

        ruleSet = set()  # Create a set of rules to prevent duplicate rules

        with transaction.atomic():  # Saves all of the rules at once
<<<<<<< HEAD
            # Adding the additional mined rules
=======
            for row in range(df.shape[0]):
                # Creating male version of the rule (oracle rules did not have a gender)
                ruleM = Rule.objects.create(lhs=df.loc[row, "lhs"],
                                            rhs=df.loc[row, "rhs"],
                                            gender='M',
                                            min_age=df.loc[row, "min_age"],
                                            max_age=df.loc[row, "max_age"],
                                            support=df.loc[row, "support"],
                                            confidence=df.loc[row, "confidence"],
                                            oracle=True)
                # Adding the rule to the set
                ruleSet.add((df.loc[row, "lhs"], df.loc[row, "rhs"], 'M',
                             df.loc[row, "min_age"], df.loc[row, "max_age"]))
                ruleM.save()  # Saving

                # Creating female version of the rule
                ruleF = Rule.objects.create(lhs=df.loc[row, "lhs"],
                                            rhs=df.loc[row, "rhs"],
                                            gender='F',
                                            min_age=df.loc[row, "min_age"],
                                            max_age=df.loc[row, "max_age"],
                                            support=df.loc[row, "support"],
                                            confidence=df.loc[row, "confidence"],
                                            oracle=True)
                # Adding the rule to the set
                ruleSet.add((df.loc[row, "lhs"], df.loc[row, "rhs"], 'F',
                             df.loc[row, "min_age"], df.loc[row, "max_age"]))
                ruleF.save()
            
        # Adding the additional mined rules
        with transaction.atomic():  # Saves all of the rules at once
>>>>>>> master
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
<<<<<<< HEAD
=======

        # Adding in mined rules truncated to 3 characters
        with transaction.atomic():  # Saves all of the rules at once
            print("Adding in rules truncated to 3 characters")
            for line in readDataFile("output_rules_cleaned_trunc3.csv")[1:]:
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
            
        # Adding in mined rules truncated to 4 characters
        with transaction.atomic():  # Saves all of the rules at once
            print("Adding in rules truncated to 4 characters")
            for line in readDataFile("output_rules_cleaned_trunc4.csv")[1:]:
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

        # Adding in rules without age or gender
        with transaction.atomic():  # Saves all of the rules at once
            print("Adding in rules without age or gender")
            for line in readDataFile("output_rules_500_no_age_or_gender.csv")[1:]:
                line = line.strip().split(",")
                # Creating male version
                potentialRule = (line[0], line[1], 'M', 0, 150)
                if potentialRule not in ruleSet:  # Checking to ensure there is no duplicate rules
                    rule = Rule.objects.create(lhs=line[0],
                                               rhs=line[1],
                                               gender='M',
                                               min_age=0,
                                               max_age=150,
                                               support=line[2],
                                               confidence=line[3])
                    ruleSet.add(potentialRule)
                    rule.save()
                # Creating female version
                potentialRule = (line[0], line[1], 'F', 0, 150)
                if potentialRule not in ruleSet:  # Checking to ensure there is no duplicate rules
                    rule = Rule.objects.create(lhs=line[0],
                                               rhs=line[1],
                                               gender='F',
                                               min_age=0,
                                               max_age=150,
                                               support=line[2],
                                               confidence=line[3])
                    ruleSet.add(potentialRule)
                    rule.save()
>>>>>>> master
        print("Done")
