from django.urls import path
from households.views import (
    HouseholdCreateView,
    HouseholdDetailView,
    HouseholdMemberCreateView,
    HouseholdListView,
    HouseholdMemberUpdateView
)

urlpatterns = [
    path("households", HouseholdCreateView.as_view(), name="household-create"),
    path("households/<uuid:household_id>", HouseholdDetailView.as_view(), name="household-detail"),
    path("households/<uuid:household_id>/members", HouseholdMemberCreateView.as_view(), name="householdMember-create"),
    path("members/me", HouseholdListView.as_view(), name="household-list"),
    path("households/<uuid:household_id>/members/<int:user_id>", HouseholdMemberUpdateView.as_view(), name="householdMember-update")

]