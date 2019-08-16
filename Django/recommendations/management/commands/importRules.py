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

        df1 = pd.read_csv("secret/three_digit_rules.csv")  # 3 digit oracle rules
        df2 = pd.read_csv("secret/four_digit_rules.csv")  # 4 digit oracle rules
        df = pd.concat([df1, df2])  # Concatenating to one dataframe
        df = df.reset_index()

        # Removing unnecessary columns
        df = df.drop(columns=["Unnamed: 0", "id", "group", "role", "score_group", "counts", "voter_total", "round"])

        lhs = []
        rhs = []
        age_min = []
        age_max = []

        for row in range(df.shape[0]):
            # Making confidence to float
            df.loc[row, "confidence"] = float(df.loc[row, "confidence"][:-1])/100
            rule = df.loc[row, "rules"].split(" => ")  # Splitting rule into LHS and RHS
            lhs.append(rule[0][1:-1])  # Adding LHS
            rhs.append(rule[1][1:-1])  # Adding RHS
            # Setting age bracket for >=65
            if(df.loc[row, "age_group"] == ">=65"):
                age_min.append(65)
                age_max.append(150)
            # Setting age bracket for other age groups
            else:
                age = df.loc[row, "age_group"].split(" to ")
                age_min.append(float(age[0]))
                age_max.append(float(age[1]))

        df["confidence"] = df["confidence"].astype("float")
        df["lhs"] = lhs
        df["rhs"] = rhs
        df["min_age"] = age_min
        df["max_age"] = age_max

        ruleSet = set()  # Create a set of rules to prevent duplicate rules
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
