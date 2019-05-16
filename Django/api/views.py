from api import serializers
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from recommendations.models import Rule, Code

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
class ListChildrenOfCode(APIView):
    def get_object(self, pk):
        try:
            code = Code.objects.get(code=pk)
            children = Code.objects.filter(parent=code.code)
            return children
        except ObjectDoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None, **kwargs):
        children = self.get_object(pk)
        serializer = serializers.ChildrenSerializer(children, many=True)
        return Response(serializer.data)

#TO DO: implement access permissions?