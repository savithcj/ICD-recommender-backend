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

    def setCategoryHiearchy(self, start, end, block, startLetter, parentDict, childrenDict):
        # sets hierarchy of block categories
        # parentDict[block] = startLetter
        for j in range(start, end+1):
            child = startLetter + '{:02d}'.format(j)
            parentDict[child] = block
            childrenDict[block].append(child)

    def findChapter(self, block):
        # determine which chapter the block belongs to by some character math
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

            self.chapterRanges.reverse()
            # chapChild1 = chapChildren[0]
            # chapChild2 = chapChildren[4]

            # descriptions[chapChild1] = chapDesc
            # descriptions[chapChild2] = chapDesc

            # parentDict[chapChild1] = chap
            # parentDict[chapChild2] = chap

            # childrenDict[chap].append(chapChild1)
            # if chapChild1 != chapChild2:
            #     childrenDict[chap].append(chapChild2)

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
                    start = int(block[1:3])
                    end = int(block[5:7])
                    startLetter = block[0]
                    # parentDict[code] = startLetter
                    # for single letter code
                    # allCodes.add(startLetter)
                    # childrenDict[startLetter].append(code)
                    # parentDict[startLetter] = ''
                    if start < end:
                        self.setCategoryHiearchy(start, end, block, startLetter, parentDict, childrenDict)
                    if start > end:
                        end = 99
                        self.setCategoryHiearchy(start, end, block, startLetter, parentDict, childrenDict)
                        startLetter = block[4]
                        start = 00
                        end = end = int(block[5:7])
                        self.setCategoryHiearchy(start, end, block, startLetter, parentDict, childrenDict)
                else:
                    print(block)

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
