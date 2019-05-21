from rest_framework import serializers
from recommendations.models import Rule, Code

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs","rhs","confidence")

class CodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code","description","parent","children")

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code","description")
