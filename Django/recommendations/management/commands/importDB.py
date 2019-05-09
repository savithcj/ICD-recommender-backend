from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Rule
import pandas as pd
import numpy as np

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        Rule.objects.all().delete()
        
        df1 = pd.read_csv("three_digit_rules.csv")
        df2 = pd.read_csv("four_digit_rules.csv")
        df = pd.concat([df1,df2])
        df = df.reset_index()

        df = df.drop(columns = ["Unnamed: 0","id","group","role","score_group","counts","voter_total","round"])

        lhs = []
        rhs = []
        age_min = []
        age_max = []
        num_accepted = []
        num_rejected = []

        for row in range(df.shape[0]):
            df.loc[row,"confidence"] = float(df.loc[row,"confidence"][:-1])/100
            rule = df.loc[row,"rules"].split(" => ")
            lhs.append(rule[0][1:-1])
            rhs.append(rule[1][1:-1])
            if(df.loc[row,"age_group"] == ">=65"):
                age_min.append(65)
                age_max.append(150)
            else:
                age = df.loc[row,"age_group"].split(" to ")
                age_min.append(float(age[0]))
                age_max.append(float(age[1]))
            num_accepted.append(0)
            num_rejected.append(0)
            
        df["confidence"] = df["confidence"].astype("float")
        df["lhs"] = lhs
        df["rhs"] = rhs
        df["min_age"] = age_min
        df["max_age"] = age_max
        df["num_accepted"] = num_accepted
        df["num_rejected"] = num_rejected
        df = df.drop(columns = ["rules","age_group","index"])

        for row in range(df.shape[0]):
            rule = Rule.objects.create(lhs = df.loc[row,"lhs"],rhs = df.loc[row,"rhs"],min_age = df.loc[row,"min_age"],max_age = df.loc[row,"max_age"],support = df.loc[row,"support"],confidence = df.loc[row,"confidence"],num_accepted = df.loc[row,"num_accepted"],num_rejected = df.loc[row,"num_rejected"],)
            rule.save()