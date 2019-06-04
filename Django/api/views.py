from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from recommendations.models import Rule, Code, TreeCode
from itertools import combinations

# Create your views here.


class ListAllRules(generics.ListAPIView):
    """
    Lists all rules
    """
    queryset = Rule.objects.all()
    serializer_class = serializers.RulesSerializer


@permission_classes((permissions.AllowAny,))
class SingleCodeDescription(APIView):
    def get(self, request, pk, format=None, **kwargs):
        try:
            codeObject = Code.objects.get(code=pk)
        except ObjectDoesNotExist:
            return Response({None})
        serializer = serializers.CodeSerializer(codeObject, many=False)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class ListChildrenOfCode(APIView):
    def get_object(self, pk):
        try:
            childrenCodes = Code.objects.get(code=pk).children
            childrenCodes = childrenCodes.split(",")
            children = Code.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get(self, request, pk, format=None, **kwargs):
        children = self.get_object(pk)
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
    def get_children(self, pk):
        try:
            childrenCodes = TreeCode.objects.get(code=pk).children
            childrenCodes = childrenCodes.split(",")
            children = TreeCode.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_siblings(self, pk):
        try:
            if(TreeCode.objects.get(code=pk).parent):
                parent = TreeCode.objects.get(code=pk).parent
                siblingCodes = TreeCode.objects.get(
                    code=parent).children.split(",")
                siblings = TreeCode.objects.filter(code__in=siblingCodes)
                return siblings
            else:
                return TreeCode.objects.filter(code=pk)
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get_single(self, pk):
        try:
            selfs = TreeCode.objects.get(code=pk)
            return selfs
        except ObjectDoesNotExist:
            return TreeCode.objects.none()

    def get(self, request, pk, format=None, **kwargs):
        # pk = pk.upper()
        selfs = self.get_single(pk)
        print("PK:", pk)
        print("SELF: ", selfs)
        parent = self.get_single(selfs.parent)
        children = self.get_children(pk)
        siblings = self.get_siblings(pk)
        selfSerializer = serializers.TreeCodeSerializer(selfs, many=False)
        parentSerializer = serializers.TreeCodeSerializer(parent, many=False)
        siblingSerializer = serializers.TreeCodeSerializer(siblings, many=True)
        childrenSerializer = serializers.TreeCodeSerializer(children, many=True)

        if parent:
            return Response({'self': selfSerializer.data, 'parent': parentSerializer.data, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})
        else:
            return Response({'self': selfSerializer.data, 'parent': None, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})


@permission_classes((permissions.AllowAny,))
class ListMatchingDescriptions(APIView):
    def get_object(self, descSubstring):
        if len(descSubstring) < 3:
            return Code.objects.none()
        return Code.objects.filter(description__icontains=descSubstring)

    def get(self, request, descSubstring, format=None, **kwargs):
        codes = self.get_object(descSubstring)
        print("CODES MATCHING SUBSTRING: ", codes)
        serializer = serializers.CodeSerializer(codes, many=True)
        return Response(serializer.data)
# TO DO: implement access permissions?
