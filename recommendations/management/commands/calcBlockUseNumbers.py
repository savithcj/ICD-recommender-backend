from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code, Rule, TreeCode, CodeBlockUsage
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import random
import numpy as np


class Command(BaseCommand):
    help = ('Calculates number of times codes within each block has been coded '
            ' and also the number of rules between blocks')

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
        for ruleCount, rule in enumerate(rules):
            if ruleCount % 1000 == 0:
                print("Rule:", ruleCount, end='\r')
            lhsCodes = rule.lhs.split(',')

            lhsBlocks = [self.findBlock(lhsCode, blockNames) for lhsCode in lhsCodes]
            rhsBlock = self.findBlock(rule.rhs, blockNames)
            # print(lhsCodes, lhsBlocks, rule.rhs, rhsBlock)
            # TEMPORARY FIX. If block doesnt exist don't count it
            if (any([lhsBlock == None for lhsBlock in lhsBlocks]) or rhsBlock == None):
                continue
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
                blockUsage[blockName] += codeObject.times_coded_dad
            if count % 1000 == 0:
                print(count, "codes processed", end='\r')

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

    def findBlock(self, code, blockNames):
        # get full ancestry
        ancestorCode = code
        while True:
            try:
                ancestor = TreeCode.objects.get(code=ancestorCode)
                if "Chapter" in ancestor.parent:
                    return ancestor.code
                ancestorCode = ancestor.parent
            except ObjectDoesNotExist:
                break
        # # if any code in the ancestry is contained within the blockname then it must
        # # exist within that block.
        # # eg A001 will have A00 in its ancestry. A00 is a substring of A00-A23
        # for ancestorCode in ancestorCodes:
        #     try:
        #         if ancestorCode in blockNames:
        #             return ancestorCode
        #     except ValueError:
        #         continue
        return None
