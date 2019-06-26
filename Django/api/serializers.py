from rest_framework import serializers
from recommendations.models import Rule, Code, TreeCode, CodeBlockUsage, DaggerAsterisk


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "num_suggested")


class CodeBlockUsageSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    parent_description = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    def get_parent_description(self, obj):
        return obj.parent_description

    def get_parent(self, obj):
        return obj.parent

    class Meta:
        model = CodeBlockUsage
        fields = ("block", "times_coded", "parent", "destination_counts", "description", "parent_description")


class ExtendedRulesSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "description", "review_status")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description")


class TreeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeCode
        fields = ("code", "description")


class daggerAsteriskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaggerAsterisk
        fields = ("dagger", "asterisk", "daggerAsteriskDescription")
