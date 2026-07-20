from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from households.models import Household, HouseholdMember
from catalog.models import Catalog

User = get_user_model()


class CatalogViewTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner1", password="pass12345")
        self.other = User.objects.create_user(username="other1", password="pass12345")

        self.household = Household.objects.create(house_name="Home A")
        HouseholdMember.objects.create(
            household=self.household,
            user=self.owner,
            role=HouseholdMember.Role.OWNER,
        )

    def test_create_catalog_item(self):
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.post(
            f"/households/{self.household.id}/catalog",
            {"item_name": "Milk", "item_type": "dairy"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Catalog.objects.count(), 1)

    def test_create_catalog_item_for_non_member_forbidden(self):
        self.assertTrue(self.client.login(username="other1", password="pass12345"))
        res = self.client.post(
            f"/households/{self.household.id}/catalog",
            {"item_name": "Milk", "item_type": "dairy"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_catalog_items(self):
        item = Catalog.objects.create(
            household=self.household,
            item_name="Milk",
            item_type="dairy",
        )
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.get(f"/households/{self.household.id}/catalog/all")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("items", res.data)
        self.assertEqual(len(res.data["items"]), 1)
        returned_item = res.data["items"][0]
        self.assertEqual(str(returned_item["item_id"]), str(item.id))
        self.assertEqual(returned_item["item_name"], "Milk")
        self.assertEqual(returned_item["item_type"], "dairy")
        self.assertIn("created_at", returned_item)
        self.assertIn("updated_at", returned_item)

    def test_get_catalog_item(self):
        item = Catalog.objects.create(
            household=self.household,
            item_name="Milk",
            item_type="dairy",
        )
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.get(f"/households/{self.household.id}/catalog/{item.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["item_name"], "Milk")

    def test_patch_catalog_item(self):
        item = Catalog.objects.create(
            household=self.household,
            item_name="Milk",
            item_type="dairy",
        )
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.patch(
            f"/households/{self.household.id}/catalog/{item.id}",
            {"item_name": "Brown Milk"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        item.refresh_from_db()
        self.assertEqual(item.item_name, "Brown Milk")

    def test_delete_catalog_item(self):
        item = Catalog.objects.create(
            household=self.household,
            item_name="Milk",
            item_type="dairy",
        )
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.delete(f"/households/{self.household.id}/catalog/{item.id}")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Catalog.objects.filter(id=item.id).exists())

    def test_duplicate_catalog_item_rejected(self):
        Catalog.objects.create(
            household=self.household,
            item_name="Milk",
            item_type="dairy",
        )
        self.assertTrue(self.client.login(username="owner1", password="pass12345"))
        res = self.client.post(
            f"/households/{self.household.id}/catalog",
            {"item_name": "milk", "item_type": "dairy"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)