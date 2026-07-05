from rest_framework.permissions import BasePermission
from households.models import HouseholdMember


class IsHouseholdMember(BasePermission):
    message = "You are not allowed to access this household."

    def has_object_permission(self, request, view, obj):
        return HouseholdMember.objects.filter(
            household=obj,
            user=request.user,
        ).exists()
    
class IsHouseholdOwner(BasePermission):
    message = "You must be a household owner to perform this action."

    def has_object_permission(self, request, view, obj):
        return HouseholdMember.objects.filter(
            household=obj,
            user=request.user,
            role=HouseholdMember.Role.OWNER,
        ).exists()