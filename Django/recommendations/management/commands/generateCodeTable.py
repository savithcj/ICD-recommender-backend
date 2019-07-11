from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code
from collections import defaultdict
from django.db import transaction
import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = 'Generates Table of ICD-10 Codes'

    def handle(self, *args, **options):
        Code.objects.all().delete()

        # Read codes and descriptions from text file
        allCodes = set()
        descriptions = defaultdict(str)
        with open('secret/codedescriptions.txt') as f:
            lines = f.readlines()
            for i in range(1, len(lines)):
                line = lines[i].split('\t')
                code = line[0].strip()
                desc = line[1].strip().replace('"', '')
                allCodes.add(code)
                descriptions[code] = desc

        print(len(allCodes), len(descriptions))

        # Generate all parents and add to code set
        parentsAdded = -1
        while parentsAdded != 0:
            parents = []
            for code in allCodes:
                parent = self.findParent(code)
                if parent != '':
                    parents.append(parent)
            oldLen = len(allCodes)
            allCodes.update(parents)
            parentsAdded = len(allCodes) - oldLen
            print("New Length: ", len(allCodes))
            print("Parents Added:", parentsAdded, '\n')

        # Store all parents
        parentDict = dict()
        for code in allCodes:
            parentDict[code] = self.findParent(code)

        # Store all children
        childrenDict = defaultdict(list)
        for code in allCodes:
            parent = self.findParent(code)
            if parent != '':
                childrenDict[parent].append(code)

        with transaction.atomic():
            count = 0
            codes = list(allCodes)
            codes.sort()
            for code in codes:
                description = descriptions[code]
                parent = parentDict[code]
                children = ''
                if len(childrenDict[code]) > 0:
                    childrenDict[code].sort()
                    for child in childrenDict[code]:
                        children += child + ','
                    children = children[:-1]

                row = Code.objects.create(code=code, children=children, parent=parent, description=description)
                row.save()
                count += 1
                if count % 1000 == 0:
                    print("Added", count, "codes")
        print("SAVED")

    # Returns parent code of any code
    def findParent(self, code):
        parent = ''
        if len(code) > 3:
            parent = code[:-1]
        elif len(code) == 3:
            parent = code[0]
        return parent
