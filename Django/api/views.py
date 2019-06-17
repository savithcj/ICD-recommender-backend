from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Length
from recommendations.models import Rule, Code, TreeCode, CodeBlockUsage
from itertools import combinations
from django.http import HttpResponse


class ListAllRules(generics.ListAPIView):
    """
    Lists all rules
    """
    queryset = Rule.objects.all()
    serializer_class = serializers.RulesSerializer


@permission_classes((permissions.AllowAny,))
class ListCodeBlockUsage(APIView):
    def get(self, request, format=None, **kwargs):
        blocks = CodeBlockUsage.objects.all()
        for block in blocks:
            blockObject = TreeCode.objects.get(code=block.block)
            block.description = blockObject.description
            block.parent = blockObject.parent
            parentObject = TreeCode.objects.get(code=block.parent)
            block.parent_description = parentObject.description
        serializer = serializers.CodeBlockUsageSerializer(blocks, many=True)
        return Response(serializer.data)
    # queryset = CodeBlockUsage.objects.all()
    # serializer_class = serializers.CodeBlockUsageSerializer


@permission_classes((permissions.AllowAny,))
class SingleCodeDescription(APIView):
    def get(self, request, inCode, format=None, **kwargs):
        try:
            codeObject = Code.objects.get(code=inCode)
        except ObjectDoesNotExist:
            return Response({None})
        serializer = serializers.CodeSerializer(codeObject, many=False)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListChildrenOfCode(APIView):
    def get_object(self, inCode):
        try:
            childrenCodes = Code.objects.get(code=inCode).children
            childrenCodes = childrenCodes.split(",")
            children = Code.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get(self, request, inCode, format=None, **kwargs):
        children = self.get_object(inCode)
        serializer = serializers.CodeSerializer(children, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListRequestedRules(APIView):
    def get_object(self, inCodes, request):
        try:
            # Sort input codes
            inputCodes = inCodes
            inputRules = inputCodes.split(",")
            inputRules.sort()

            # Build combinations of codes
            lhs = []
            for i in range(len(inputRules)):
                lhs += list(combinations(inputRules, i+1))

            # Concatening items in combinations together
            new_lhs = []
            for entry in lhs:
                empty = ''
                for i in range(len(entry)):
                    empty += entry[i] + ","
                new_lhs.append(empty[:-1])

            # special params
            kwargs = dict()
            kwargs["min_age"] = None
            kwargs["max_age"] = None
            kwargs["gender"] = None

            # TODO: Implement gender

            ageRange = [65, 45, 20, 0]
            age_param = request.GET.get('age', None)
            if age_param is not None and age_param.isdigit():
                age = int(age_param)
                print("In Age:", age)
                for minAge in ageRange:
                    if age >= minAge:
                        kwargs["min_age"] = minAge
                        print("Min Age:", minAge)
                        break
                pass

            # get rules
            rules = Rule.objects.filter(
                lhs__in=new_lhs, **{k: v for k, v in kwargs.items() if v is not None}).order_by('-confidence')

            # exclude rules with code in RHS that already exist in the LHS
            rules = rules.exclude(rhs__iregex=r'(' + '|'.join(new_lhs) + ')')

            # append description
            for rule in rules:
                code = Code.objects.get(code=rule.rhs)
                rule.description = code.description

            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes, request)
        serializer = serializers.ExtendedRulesSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class Family(APIView):
    def get_children(self, inCode):
        try:
            childrenCodes = TreeCode.objects.get(code=inCode).children
            childrenCodes = childrenCodes.split(",")
            children = TreeCode.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_siblings(self, inCode):
        try:
            if(TreeCode.objects.get(code=inCode).parent):
                parent = TreeCode.objects.get(code=inCode).parent
                siblingCodes = TreeCode.objects.get(
                    code=parent).children.split(",")
                siblings = TreeCode.objects.filter(code__in=siblingCodes)
                return siblings
            else:
                return TreeCode.objects.filter(code=inCode)
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_single(self, inCode):
        try:
            selfs = TreeCode.objects.get(code=inCode)
            return selfs
        except ObjectDoesNotExist:
            return None

    def get(self, request, inCode, format=None, **kwargs):
        selfs = self.get_single(inCode)
        if selfs == None:
            return Response({'self': None, 'parent': None, 'siblings': None, 'children': None})
        parent = self.get_single(selfs.parent)
        children = self.get_children(inCode)
        siblings = self.get_siblings(inCode)
        selfSerializer = serializers.TreeCodeSerializer(selfs, many=False)
        parentSerializer = serializers.TreeCodeSerializer(parent, many=False)
        siblingSerializer = serializers.TreeCodeSerializer(siblings, many=True)
        childrenSerializer = serializers.TreeCodeSerializer(
            children, many=True)

        if parent:
            return Response({'self': selfSerializer.data, 'parent': parentSerializer.data, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})
        else:
            return Response({'self': selfSerializer.data, 'parent': None, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})


@permission_classes((permissions.AllowAny,))
class ListMatchingDescriptions(APIView):
    def get_object(self, descSubstring):
        if len(descSubstring) < 3:
            return Code.objects.none()
        return Code.objects.filter(description__icontains=descSubstring).order_by(Length('code').asc())[:15]

    def get(self, request, descSubstring, format=None, **kwargs):
        codes = self.get_object(descSubstring)
        serializer = serializers.CodeSerializer(codes, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListAncestors(APIView):
    def get_object(self, code):
        ancestors = []
        print("Getting ancestors of", code)
        while True:
            try:
                ancestor = TreeCode.objects.get(code=code)
                serializer = serializers.CodeSerializer(ancestor, many=False)
                ancestors.append(serializer)
                code = ancestor.parent
                print("parent:", ancestor.parent)
            except ObjectDoesNotExist:
                return ancestors

    def get(self, request, inCode, format=None, **kwargs):
        ancestors = self.get_object(inCode)
        return Response([ancestor.data for ancestor in ancestors])


@permission_classes((permissions.AllowAny,))
class ListCodeAutosuggestions(APIView):
    def get(self, request, matchString, format=None, **kwargs):
        descMatch = ListMatchingDescriptions()
        codeMatch = ListChildrenOfCode()

        matchesDesc = descMatch.get_object(matchString)
        matchesCode = codeMatch.get_object(matchString)

        serializerDesc = serializers.CodeSerializer(matchesDesc, many=True)
        serializerCode = serializers.CodeSerializer(matchesCode, many=True)
        return Response({"description matches": serializerDesc.data, "code matches": serializerCode.data, "keyword matches": []})


@permission_classes((permissions.AllowAny,))
class CodeUsed(APIView):
    def put(self, request, inCodes, format=None, **kwargs):
        codeList = inCodes.split(",")
        codes = Code.objects.filter(code__in=codeList)
        if len(codes) > 0:
            for code in codes:
                code.times_coded += 1
                code.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=204)

# TO DO: implement access permissions?
