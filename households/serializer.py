from rest_framework import serializers
from households.models import Household, HouseholdMember
from django.contrib.auth import get_user_model

class HouseholdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = ["house_name"]

User = get_user_model()
class HouseholdMemberCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(
        choices=[HouseholdMember.Role.OWNER, HouseholdMember.Role.MEMBER],
        required=False,
        default=HouseholdMember.Role.MEMBER,
    )

    def validate_user_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist.")
        return value
    