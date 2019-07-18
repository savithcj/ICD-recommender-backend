from rest_framework import serializers
from recommendations.models import Rule, Code, TreeCode, CodeBlockUsage, DaggerAsterisk


# Standard rule serializer
class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "num_suggested", "active", "gender")


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


class FlaggedRuleSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "gender", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "description",
                  "review_status", "oracle")


class ExtendedRulesSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    conf_factor = serializers.SerializerMethodField()
    interact_factor = serializers.SerializerMethodField()
    # can remove conf_factor and interact_factor later
    score = serializers.SerializerMethodField()

    def get_description(self, obj):
        return obj.description

    def get_conf_factor(self, obj):
        return obj.conf_factor

    def get_interact_factor(self, obj):
        return obj.interact_factor

    def get_score(self, obj):
        return obj.score

    class Meta:
        model = Rule
        fields = ("id", "lhs", "rhs", "gender", "min_age", "max_age", "support",
                  "confidence", "num_accepted", "num_rejected", "description",
                  "review_status", "conf_factor", "interact_factor", "score", "oracle", "active")


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ("code", "description")


class TreeCodeSerializer(serializers.ModelSerializer):
    hasChildren = serializers.SerializerMethodField()

    def get_hasChildren(self, obj):
        return obj.hasChildren

    class Meta:
        model = TreeCode
        fields = ("code", "description", "hasChildren")


class daggerAsteriskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DaggerAsterisk
        fields = ("dagger", "asterisk")
