from rest_framework import serializers
from recommendations.models import Rule

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ("lhs","rhs")