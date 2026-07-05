from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from households.models import Household, HouseholdMember
from households.serializer import HouseholdCreateSerializer, HouseholdMemberCreateSerializer
from households.permissions import IsHouseholdOwner
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model



# Create your views here.
class HouseholdCreateView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer = HouseholdCreateSerializer(data = request.data)
        
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            household = serializer.save()
            HouseholdMember.objects.create(
                user=request.user,
                household=household,
                role=HouseholdMember.Role.OWNER
            )
        return Response(
            {
                "house_name":household.house_name,
                "household_id":str(household.id),
                "created_at":household.created_at
            },
            status=status.HTTP_201_CREATED,
        )

class HouseholdDetailView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdOwner]

    def _get_household_and_check_owner(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        return household

    def patch(self, request, household_id):
        household = self._get_household_and_check_owner(request, household_id)
        serializer = HouseholdCreateSerializer(
            household,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "house_name": household.house_name,
                "created_at": household.created_at,
                "updated_at": household.updated_at,
            },
            status=status.HTTP_200_OK,
        )
    
    def delete(self, request, household_id):
        household = self._get_household_and_check_owner(request, household_id)
        household.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )   

class HouseholdMemberCreateView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdOwner]

    def post(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        serializer = HouseholdMemberCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_to_add_id = serializer.validated_data["user_id"]
        role = serializer.validated_data["role"]

        User = get_user_model()
        user_to_add = get_object_or_404(User, id=user_to_add_id)

        membership, created = HouseholdMember.objects.get_or_create(
            user=user_to_add,
            household=household,
            defaults={"role": role},
        )
        if not created:
            return Response(
                {"error": "User is already a member of this household"},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            {
                "user_id": str(user_to_add_id),
                "household_id": str(household_id),
                "role": membership.role,
                "created_at": membership.created_at,
            },
            status=status.HTTP_201_CREATED,
        )

        
class HouseholdListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = (
            HouseholdMember.objects.filter(user=request.user)
            .select_related("household")
            .order_by("-created_at")
        )

        data = [
            {
                "household_id": str(membership.household.id),
                "house_name": membership.household.house_name,
                "role": membership.role,
                "joined_at": membership.created_at,
            }
            for membership in memberships
        ]

        return Response({"households": data}, status=status.HTTP_200_OK)
        
    
class HouseholdMemberUpdateView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdOwner]

    def patch(self, request, household_id, user_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
    
        membership = get_object_or_404(
            HouseholdMember,
            household=household,
            user_id=user_id,
        )

        # Reject if already owner
        if membership.role == HouseholdMember.Role.OWNER:
            return Response(
                {
                    "error": "User is already an owner"
                },
                status=status.HTTP_409_CONFLICT,
            )
        
        membership.role = HouseholdMember.Role.OWNER
        membership.save(update_fields=["role", "updated_at"])

        return Response(
            {
                "user_id": str(membership.user_id),
                "household_id": str(membership.household_id),
                "role": membership.role,
                "updated_at": membership.updated_at,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, household_id, user_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
    
        membership = get_object_or_404(
            HouseholdMember,
            household=household,
            user_id=user_id,
        )

        if membership.role == HouseholdMember.Role.OWNER:
            return Response(
                {
                    "error": "You cannot delete an owner record, delete household instead."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

