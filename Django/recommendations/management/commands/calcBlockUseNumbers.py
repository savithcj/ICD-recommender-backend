from django.core.management.base import BaseCommand, CommandError
from recommendations.models import Code, Rule, TreeCode, CodeBlockUsage
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
import random


class Command(BaseCommand):
    help = '''Sums the number of times each code has been coded under a certain block'''

    def handle(self, *args, **options):
        CodeBlockUsage.objects.all().delete()

        # find all blocks. Will have a chapter as its parent
        blockObjects = TreeCode.objects.filter(parent__contains='Chapter').order_by('code')

        # initialize code usage numbers for each block
        blockUsage = dict()
        blockNames = []
        blockParents = dict()
        for blockObject in blockObjects:
            blockUsage[blockObject.code] = 0
            blockNames.append(blockObject.code)
            blockParents[blockObject.code] = blockObject.parent

        codeObjects = Code.objects.all()
        for count, codeObject in enumerate(codeObjects):
            # get ancestry of codes
            ancestorCodes = []
            ancestorCode = codeObject.code
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
                        blockUsage[ancestorCode] += codeObject.times_coded
                        break
                        # print(codeObject.code, ancestorCode, blockUsage[ancestorCode])
                except ValueError:
                    continue
            if count % 1000 == 0:
                print(count, "codes processed")
        # save block usage numbers in the CodeBlockUsage table
        print("Saving block usage numbers...")
        with transaction.atomic():
            for blockName in blockNames:
                block = CodeBlockUsage.objects.create(
                    block=blockName, times_coded=blockUsage[blockName], parent=blockParents[blockName])
                block.save()
        print("Done")
