from rest_framework import serializers
from recommendations.models import Rule, Code

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs","rhs")

class CodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code","description","parent","children")

class ChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code","description")