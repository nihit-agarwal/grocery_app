from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Catalog
from households.models import Household, HouseholdMember
from inventory.models import Inventory

User = get_user_model()


class InventoryViewTests(APITestCase):
	def setUp(self):
		self.owner = User.objects.create_user(username="owner1", password="pass12345")
		self.member = User.objects.create_user(username="member1", password="pass12345")
		self.outsider = User.objects.create_user(username="outsider1", password="pass12345")

		self.household = Household.objects.create(house_name="Home A")
		self.other_household = Household.objects.create(house_name="Home B")

		HouseholdMember.objects.create(
			household=self.household,
			user=self.owner,
			role=HouseholdMember.Role.OWNER,
		)
		HouseholdMember.objects.create(
			household=self.household,
			user=self.member,
			role=HouseholdMember.Role.MEMBER,
		)

		self.catalog_item = Catalog.objects.create(
			household=self.household,
			item_name="Milk",
			item_type=Catalog.ItemType.DAIRY,
		)
		self.other_household_item = Catalog.objects.create(
			household=self.other_household,
			item_name="Peas",
			item_type=Catalog.ItemType.FROZEN,
		)

	def test_add_inventory_item(self):
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/inventory",
			{
				"item": str(self.catalog_item.id),
				"purchased_on": "2026-01-10",
				"expiry_date": "2026-01-20",
				"qty": "2.50",
				"unit": "l",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Inventory.objects.count(), 1)

		row = Inventory.objects.get()
		self.assertEqual(row.household_id, self.household.id)
		self.assertEqual(row.item_id, self.catalog_item.id)

	def test_add_inventory_item_forbidden_for_non_member(self):
		self.assertTrue(self.client.login(username="outsider1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/inventory",
			{
				"item": str(self.catalog_item.id),
				"purchased_on": "2026-01-10",
				"expiry_date": "2026-01-20",
				"qty": "1.00",
				"unit": "pieces",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(Inventory.objects.count(), 0)

	def test_add_inventory_item_rejects_catalog_item_from_other_household(self):
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/inventory",
			{
				"item": str(self.other_household_item.id),
				"purchased_on": "2026-01-10",
				"expiry_date": "2026-01-20",
				"qty": "1.00",
				"unit": "kg",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Inventory.objects.count(), 0)

	def test_add_inventory_item_rejects_duplicate_batch(self):
		Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="1.00",
			unit="pieces",
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/inventory",
			{
				"item": str(self.catalog_item.id),
				"purchased_on": "2026-01-10",
				"expiry_date": "2026-01-20",
				"qty": "2.00",
				"unit": "pieces",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Inventory.objects.count(), 1)

	def test_add_inventory_item_rejects_purchase_after_expiry(self):
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/inventory",
			{
				"item": str(self.catalog_item.id),
				"purchased_on": "2026-01-21",
				"expiry_date": "2026-01-20",
				"qty": "1.00",
				"unit": "kg",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Inventory.objects.count(), 0)

	def test_list_inventory_items(self):
		Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="3.00",
			unit="l",
		)
		self.assertTrue(self.client.login(username="member1", password="pass12345"))

		res = self.client.get(f"/households/{self.household.id}/inventory/all")

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn("inventory", res.data)
		self.assertEqual(len(res.data["inventory"]), 1)

	def test_get_inventory_rows_for_item(self):
		Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="1.00",
			unit="l",
		)
		Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-12",
			expiry_date="2026-01-22",
			qty="2.00",
			unit="l",
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.get(
			f"/households/{self.household.id}/catalog/{self.catalog_item.id}/inventory"
		)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn("inventory", res.data)
		self.assertEqual(len(res.data["inventory"]), 2)

	def test_patch_inventory_qty(self):
		row = Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="1.00",
			unit="pieces",
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.patch(
			f"/households/{self.household.id}/inventory/{row.id}",
			{"qty": "4.75"},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		row.refresh_from_db()
		self.assertEqual(str(row.qty), "4.75")

	def test_patch_inventory_qty_rejects_non_positive_value(self):
		row = Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="1.00",
			unit="pieces",
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.patch(
			f"/households/{self.household.id}/inventory/{row.id}",
			{"qty": "0"},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		row.refresh_from_db()
		self.assertEqual(str(row.qty), "1.00")

	def test_delete_inventory_row(self):
		row = Inventory.objects.create(
			household=self.household,
			item=self.catalog_item,
			purchased_on="2026-01-10",
			expiry_date="2026-01-20",
			qty="1.00",
			unit="pieces",
		)
		self.assertTrue(self.client.login(username="member1", password="pass12345"))

		res = self.client.delete(f"/households/{self.household.id}/inventory/{row.id}")

		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Inventory.objects.filter(id=row.id).exists())
