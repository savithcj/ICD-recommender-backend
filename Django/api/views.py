from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from recommendations.models import Rule, Code
from itertools import combinations

# Create your views here.


class ListAllRules(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Rule.objects.all()
    serializer_class = serializers.RulesSerializer


class ListAllCodes(generics.ListAPIView):
    queryset = Code.objects.all()
    serializer_class = serializers.CodesSerializer


@permission_classes((permissions.AllowAny,))
class CodeInformation(APIView):
    def get(self, request, pk, format=None, **kwargs):
        CodeInfo = get_object_or_404(Code, pk=pk)
        serializer = serializers.CodesSerializer(CodeInfo)
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
    def get_object(self, pk):
        try:
            # Sort input codes
            inputCodes = pk
            inputRules = inputCodes.split(",")
            inputRules.sort()

            # Build combinations of codes
            lhs = []
            for i in range(len(inputRules)):
                lhs += list(combinations(inputRules, i+1))

            new_lhs = []
            for entry in lhs:
                empty = ''
                for i in range(len(entry)):
                    empty += entry[i] + ","
                new_lhs.append(empty[:-1])
            qs = Rule.objects.none()

            for combination in new_lhs:
                qTemp = Rule.objects.filter(lhs=combination)
                print(qTemp)
                qs = qs.union(qTemp).distinct()
            return qs
        except ObjectDoesNotExist:
            return Rule.objects.none()

    def get(self, request, pk, format=None, **kwargs):
        rules = self.get_object(pk)
        serializer = serializers.RulesSerializer(rules, many=True)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny,))
class Family(APIView):
    def get_parent(self, pk):
        try:
            parentCode = Code.objects.get(code=pk).parent
            parent = Code.objects.filter(code__iexact=parentCode)
            return parent
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get_children(self, pk):
        try:
            childrenCodes = Code.objects.get(code=pk).children
            childrenCodes = childrenCodes.split(",")
            children = Code.objects.filter(code__in=childrenCodes)
            return children
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get_siblings(self, pk):
        try:
            parent = Code.objects.get(code=pk).parent
            siblingCodes = Code.objects.get(code=parent).children.split(",")
            siblingCodes.remove(pk)
            siblings = Code.objects.filter(code__in=siblingCodes)
            return siblings
        except ObjectDoesNotExist:
            return Code.objects.none()

    def get(self, request, pk, format=None, **kwargs):
        parent = self.get_parent(pk)
        children = self.get_children(pk)
        siblings = self.get_siblings(pk)
        parentSerializer = serializers.CodeSerializer(parent, many=True)
        siblingSerializer = serializers.CodeSerializer(siblings, many=True)
        childrenSerializer = serializers.CodeSerializer(children, many=True)
        return Response({'parent': parentSerializer.data, 'siblings': siblingSerializer.data, 'children': childrenSerializer.data})

# TO DO: implement access permissions?
