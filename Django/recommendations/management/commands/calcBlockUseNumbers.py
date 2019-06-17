from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code, Rule, TreeCode, CodeBlockUsage
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import random
import numpy as np


class Command(BaseCommand):
    help = '''Sums the number of times each code has been coded under a certain block'''

    def findBlock(self, code, blockNames):
        ancestorCodes = []
        ancestorCode = code
        while True:
            try:
                ancestor = TreeCode.objects.get(code=ancestorCode)
                ancestorCode = ancestor.parent
                ancestorCodes.append(ancestorCode)
            except ObjectDoesNotExist:
                break
        # add code usage to the appropriate block
        for ancestorCode in ancestorCodes:
            try:
                if ancestorCode in blockNames:
                    return ancestorCode
                    # print(codeObject.code, ancestorCode, blockUsage[ancestorCode])
            except ValueError:
                continue
        return None

    def handle(self, *args, **options):
        CodeBlockUsage.objects.all().delete()

        # find all blocks. Will have a chapter as its parent
        print("Finding blocks...")
        blockObjects = TreeCode.objects.filter(parent__contains='Chapter').order_by('code')

        # initialize code usage numbers for each block
        blockNames = []
        blockUsage = dict()
        for blockObject in blockObjects:
            blockNames.append(blockObject.code)
            blockUsage[blockObject.code] = 0

        # Find number of rule destinations for each block
        print("Calculating rule destinations for each block...")
        numBlocks = len(blockNames)
        # first row is block A00-A09. elements in this row show
        # how many rules have block A00-A09 as a LHS and this element as RHS
        destinationMatrix = np.zeros([numBlocks, numBlocks])
        rules = Rule.objects.all()
        for rule in rules:
            lhsCodes = rule.lhs.split(',')

            lhsBlocks = [self.findBlock(lhsCode, blockNames) for lhsCode in lhsCodes]
            rhsBlock = self.findBlock(rule.rhs, blockNames)
            # print(lhsCodes, lhsBlocks, rule.rhs, rhsBlock)
            for lhsBlock in lhsBlocks:
                if lhsBlock != rhsBlock:
                    lhsIndex = blockNames.index(lhsBlock)
                    rhsIndex = blockNames.index(rhsBlock)
                    destinationMatrix[lhsIndex, rhsIndex] += 1

        print("Calculating block usage numbers...")
        codeObjects = Code.objects.all()
        for count, codeObject in enumerate(codeObjects):
            # get ancestry of codes
            blockName = self.findBlock(codeObject.code, blockNames)
            if blockName is not None:
                blockUsage[blockName] += codeObject.times_coded
            if count % 1000 == 0:
                print(count, "codes processed")

        # save block usage numbers in the CodeBlockUsage table
        print("Saving block usage numbers...")
        with transaction.atomic():
            for index, blockName in enumerate(blockNames):
                destStr = ''
                for destNum in destinationMatrix[index, :]:
                    destStr = destStr + str(int(destNum)) + ','
                destStr = destStr[:-1]
                block = CodeBlockUsage.objects.create(
                    block=blockName, times_coded=blockUsage[blockName],
                    destination_counts=destStr)
                block.save()
        print("Done")
