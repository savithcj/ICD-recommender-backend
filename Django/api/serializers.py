from rest_framework import serializers
from recommendations.models import Rule, Code, TreeCode, CodeBlockUsage


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected")


class CodeBlockUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeBlockUsage
        fields = ("block", "times_coded", "parent")


class ExtendedRulesSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "description")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description")


class TreeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeCode
        fields = ("code", "description")
