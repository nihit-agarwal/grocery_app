from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from households.models import Household, HouseholdMember

User = get_user_model()


class HouseholdViewTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner1", password="pass12345")
        self.other = User.objects.create_user(username="other1", password="pass12345")

    def test_create_household_creates_owner_membership(self):
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))

        res = self.client.post(
            "/households",
            {"house_name": "Home A"},
            format="json",
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Household.objects.count(), 1)

        household = Household.objects.get()
        self.assertEqual(household.house_name, "Home A")
        self.assertTrue(
            HouseholdMember.objects.filter(
                household=household,
                user=self.owner,
                role=HouseholdMember.Role.OWNER,
            ).exists()
        )

    def test_patch_household_owner_only(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )

        self.assertTrue(self.client.login(username="other1", password="pass12345"))
        res = self.client.patch(
            f"/households/{household.id}",
            {"house_name": "Monkey House"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.patch(
            f"/households/{household.id}",
            {"house_name": "York House"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        household.refresh_from_db()
        self.assertEqual(household.house_name, "York House")

    def test_delete_household_owner_only(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )

        self.assertTrue(self.client.login(username="other1", password="pass12345"))
        res = self.client.delete(f"/households/{household.id}")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.delete(f"/households/{household.id}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Household.objects.filter(id=household.id).exists())

    def test_add_household_member_owner_only(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )

        self.assertTrue(self.client.login(username="other1", password="pass12345"))
        res = self.client.post(
            f"/households/{household.id}/members",
            {"user_id": str(self.other.id)},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.post(
            f"/households/{household.id}/members",
            {"user_id": str(self.other.id)},
            format="json",
        )
        # print(res.status_code, res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            HouseholdMember.objects.filter(
                household=household,
                user=self.other,
                role=HouseholdMember.Role.MEMBER,
            ).exists()
        )

    def test_get_members_me_returns_user_households(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )

        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.get("/members/me")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("households", res.data)
        self.assertEqual(len(res.data["households"]), 1)

    def test_promote_member_to_owner(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )
        HouseholdMember.objects.create(
            household=household,
            user=self.other,
            role=HouseholdMember.Role.MEMBER,
        )

        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.patch(
            f"/households/{household.id}/members/{self.other.id}",
            {},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        membership = HouseholdMember.objects.get(household=household, user=self.other)
        self.assertEqual(membership.role, HouseholdMember.Role.OWNER)

    def test_delete_member_rejects_owner_delete(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )
        HouseholdMember.objects.create(
            household=household,
            user=self.other,
            role=HouseholdMember.Role.MEMBER,
        )

        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.delete(f"/households/{household.id}/members/{self.owner.id}")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_member(self):
        household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )
        HouseholdMember.objects.create(
            household=household,
            user=self.other,
            role=HouseholdMember.Role.MEMBER,
        )

        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.delete(f"/households/{household.id}/members/{self.other.id}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            HouseholdMember.objects.filter(
                household=household,
                user=self.other,
            ).exists()
        )