from rest_framework import serializers
from .models import Society, Membership, SocietyRule

class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
        read_only_fields = ['joined_at']


class SocietyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocietyRule
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        if not data.get('rule_text'):
            raise serializers.ValidationError("Rule text cannot be empty.")
        return data