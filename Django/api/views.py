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
    def get_object(self, inCodes):
        try:
            # Sort input codes
            inputCodes = inCodes
            inputRules = inputCodes.split(",")
            inputRules.sort()

            # Build combinations of codes
            lhs = []
            for i in range(len(inputRules)):
                lhs += list(combinations(inputRules, i+1))
            print("LHS", lhs)

            # Concatening items in combinations together
            new_lhs = []
            for entry in lhs:
                empty = ''
                for i in range(len(entry)):
                    empty += entry[i] + ","
                new_lhs.append(empty[:-1])

            # get rules
            rules = Rule.objects.filter(
                lhs__in=new_lhs).order_by('-confidence')

            # exclude rules with code in RHS that already exist in the LHS
            print(r'(' + '|'.join(new_lhs) + ')')
            rules = rules.exclude(rhs__iregex=r'(' + '|'.join(new_lhs) + ')')

            # append description
            for rule in rules:
                code = Code.objects.get(code=rule.rhs)
                rule.description = code.description

            return rules
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, inCodes, format=None, **kwargs):
        rules = self.get_object(inCodes)
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
        pk = pk.upper()
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

# TO DO: implement access permissions?
