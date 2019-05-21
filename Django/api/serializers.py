from rest_framework import serializers
from recommendations.models import Rule, Code


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected")


class CodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description", "parent", "children")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description")
