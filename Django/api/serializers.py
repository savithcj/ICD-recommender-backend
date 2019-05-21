from rest_framework import serializers
from recommendations.models import Rule, Code


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected")


class ExtendedRulesSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    class Meta:
        model = Rule
        fields = ("lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "description")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description")
