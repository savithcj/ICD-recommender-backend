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

    def setCategoryHiearchy(self, startNum, endNum, block, startLetter, parentDict, childrenDict):
        # Sets hierarchy of block categories
        for j in range(startNum, endNum+1):
            child = startLetter + '{:02d}'.format(j)
            parentDict[child] = block
            childrenDict[block].append(child)

    def findChapter(self, block):
        # Determine which chapter the block belongs to by some character math
        for chapterRange in self.chapterRanges:
            blockVal = ord(block[0])*100 + int(block[1:3])
            chapVal = ord(chapterRange[0])*100 + int(chapterRange[1:3])
            if blockVal >= chapVal:
                chapter = self.chapters[chapterRange]
                print("BLOCK:", block, "CHAPTER", chapter, "CHAPTER RANGE:", chapterRange)
                return chapter
        chapter = self.chapters[chapterRange]
        return chapter

    def handle(self, *args, **options):
        # Read codes and descriptions from text file
        TreeCode.objects.all().delete()

        allCodes = set()
        descriptions = dict()
        with open('secret/codedescriptions.txt') as f:
            for line in f.readlines():
                line = line.split('\t')
                code = line[0].strip()
                desc = line[1].strip().replace('"', '')
                allCodes.add(code)
                descriptions[code] = desc

        categoryDescriptions = dict()
        with open('secret/categories.csv') as f:
            for line in f.readlines():
                line = line.split(',')
                code = line[0].strip()
                desc = line[1].strip().replace('"', '')
                categoryDescriptions[code] = desc

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

        # Add ICD-10 chapters
        self.chapterRanges = []
        self.chapters = dict()
        with open('secret/ICDChapters.txt') as f:
            lines = f.readlines()
            baseCode = 'ICD-10-CA'
            allCodes.add(baseCode)
            descriptions[baseCode] = ''
            parentDict[baseCode] = ''
            for i in range(len(lines)):
                line = lines[i].replace('\n', '').split('\t')
                print(line)
                chap = 'Chapter ' + line[0]
                chapChildren = line[1]
                chapDesc = line[2]
                allCodes.add(chap)
                descriptions[chap] = chapDesc
                parentDict[chap] = baseCode
                childrenDict[baseCode].append(chap)
                self.chapterRanges.append(chapChildren)
                self.chapters[chapChildren] = chap

            self.chapterRanges.sort()
            self.chapterRanges.reverse()

        # Add ICD-10 blocks
        with open('secret/ICDBlocks.txt') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i].split('\t')
                block = line[0].strip()
                blockDesc = line[1].strip().replace('"', '')
                allCodes.add(block)
                descriptions[block] = blockDesc
                chapter = self.findChapter(block)
                parentDict[block] = chapter
                childrenDict[chapter].append(block)

                # Add 3 letter codes to blocks
                if len(block) > 3:
                    print(block, ': ', block[0], block[1:3], block[5:7])
                    startNum = int(block[1:3])
                    endNum = int(block[5:7])
                    startLetter = block[0]
                    endLetter = block[4]
                    if startLetter != endLetter:
                        self.setCategoryHiearchy(startNum, 99, block, startLetter, parentDict, childrenDict)
                        numLettersBetween = ord(endLetter) - ord(startLetter) - 1
                        for i in range(numLettersBetween):
                            print(chr(ord(startLetter)+i+1))
                            self.setCategoryHiearchy(0, 99, block, chr(ord(startLetter)+i+1), parentDict, childrenDict)
                        self.setCategoryHiearchy(0, endNum, block, endLetter, parentDict, childrenDict)
                    else:
                        self.setCategoryHiearchy(startNum, endNum, block, startLetter, parentDict, childrenDict)
                else:
                    print(block)

        # Creating and saving objects
        with transaction.atomic():
            count = 0
            codes = list(allCodes)
            codes.sort()
            for code in codes:
                # Check if ICD-10-CA has a description first and use that
                description = codeDescriptions.get(code, '')
                if description == '':
                    # Use descfiption from ICD-10-CM if it doesn't exist
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
