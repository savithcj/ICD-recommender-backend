from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code
from collections import defaultdict
from django.db import transaction
import pandas as pd
import numpy as np
from secret import term_preprocessing


class Command(BaseCommand):
    help = 'Generates Table of ICD-10 Codes'

    def handle(self, *args, **options):
        Code.objects.all().delete()

        # Read codes and descriptions from text file
        allCodes = set()
        codeDescriptions = dict()
        with open('secret/codedescriptions.txt') as f:
            for line in f.readlines():
                line = line.split('\t')
                code = line[0].strip()
                desc = line[1].strip().replace('"', '')
                allCodes.add(code)
                codeDescriptions[code] = desc

        categoryDescriptions = dict()
        with open('secret/categories.csv') as f:
            for line in f.readlines():
                line = line.split(',')
                code = line[0].strip()
                desc = line[1].strip().replace('"', '')
                categoryDescriptions[code] = desc

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

        keywordDict = term_preprocessing.getKeywordTerms()
        with transaction.atomic():
            count = 0
            codes = list(allCodes)
            codes.sort()
            for code in codes:
                description = codeDescriptions.get(code, '')
                if description == '':
                    description = categoryDescriptions.get(code, '')
                parent = parentDict[code]
                children = ''
                if len(childrenDict[code]) > 0:
                    childrenDict[code].sort()
                    for child in childrenDict[code]:
                        children += child + ','
                    children = children[:-1]

                # check if code has keyword associated with it
                keyword_terms = keywordDict[code].lower()
                if keyword_terms == '' and len(code) > 3:
                    # add keywords from children if empty (due to using CM keywords)
                    for i in range(10):
                        keyword_terms += keywordDict[code + str(i)].lower()
                row = Code.objects.create(code=code, children=children, parent=parent,
                                          description=description, keyword_terms=keyword_terms)
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
