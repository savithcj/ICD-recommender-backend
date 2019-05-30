from django.core.management.base import BaseCommand, CommandError
from recommendations.models import TreeCode
from collections import defaultdict
from django.db import transaction
import pandas as pd
import numpy as np


class Command(BaseCommand):
    help = 'Generates Table of ICD-10 Codes'

    def findParent(self, code):
        # returns parent code of actual codes
        parent = ''
        if len(code) > 3:
            parent = code[:-1]
        return parent

    def setCategoryHiearchy(self, start, end, code, parentCode, parentDict, childrenDict):
        # sets hierarchy of block categories
        parentDict[code] = parentCode
        for j in range(start, end+1):
            child = parentCode + '{:02d}'.format(j)
            parentDict[child] = code
            childrenDict[code].append(child)

    def handle(self, *args, **options):
        # Read codes and descriptions from text file
        TreeCode.objects.all().delete()

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

        # below is extra code for adding three digit code branches
        with open('secret/bigCats.txt') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].split('\t')
                code = line[0].strip()
                code = code.replace('–', '-')
                desc = line[1].strip().replace('"', '')
                allCodes.add(code)
                descriptions[code] = desc
                if len(code) > 3:
                    print(code, ': ', code[0], code[1:3], code[5:7])
                    start = int(code[1:3])
                    end = int(code[5:7])
                    parentCode = code[0]
                    parentDict[code] = parentCode
                    # for single letter code
                    allCodes.add(parentCode)
                    childrenDict[parentCode].append(code)
                    parentDict[parentCode] = ''
                    if start < end:
                        self.setCategoryHiearchy(start, end, code, parentCode, parentDict, childrenDict)
                    if start > end:
                        end = 99
                        self.setCategoryHiearchy(start, end, code, parentCode, parentDict, childrenDict)
                        parentCode = code[4]
                        start = 00
                        end = end = int(code[5:7])
                        self.setCategoryHiearchy(start, end, code, parentCode, parentDict, childrenDict)
                else:
                    print(code)

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

                row = TreeCode.objects.create(code=code, children=children, parent=parent, description=description)
                row.save()
                count += 1
                if count % 1000 == 0:
                    print("Added", count, "codes")
        print("SAVED")
