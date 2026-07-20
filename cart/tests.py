from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from cart.models import Cart
from catalog.models import Catalog
from households.models import Household, HouseholdMember

User = get_user_model()


class CartViewTests(APITestCase):
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

	def test_add_cart_item(self):
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/cart",
			{
				"item": str(self.catalog_item.id),
				"qty_needed": "2.50",
				"unit": "l",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Cart.objects.count(), 1)

		row = Cart.objects.get()
		self.assertEqual(row.household_id, self.household.id)
		self.assertEqual(row.item_id, self.catalog_item.id)

	def test_add_cart_item_forbidden_for_non_member(self):
		self.assertTrue(self.client.login(username="outsider1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/cart",
			{
				"item": str(self.catalog_item.id),
				"qty_needed": "1.00",
				"unit": "pieces",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(Cart.objects.count(), 0)

	def test_add_cart_item_rejects_catalog_item_from_other_household(self):
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/cart",
			{
				"item": str(self.other_household_item.id),
				"qty_needed": "1.00",
				"unit": "kg",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Cart.objects.count(), 0)

	def test_add_cart_item_rejects_duplicate_item(self):
		Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="1.00",
			unit="pieces",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.post(
			f"/households/{self.household.id}/cart",
			{
				"item": str(self.catalog_item.id),
				"qty_needed": "2.00",
				"unit": "pieces",
			},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Cart.objects.count(), 1)

	def test_list_cart_items(self):
		Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="3.00",
			unit="l",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="member1", password="pass12345"))

		res = self.client.get(f"/households/{self.household.id}/cart/all")

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn("cart", res.data)
		self.assertEqual(len(res.data["cart"]), 1)
		returned_row = res.data["cart"][0]
		self.assertEqual(returned_row["item_id"], str(self.catalog_item.id))
		self.assertEqual(returned_row["item_name"], "Milk")
		self.assertEqual(str(returned_row["quantity"]), "3.00")
		self.assertEqual(returned_row["unit"], "l")
		self.assertFalse(returned_row["is_bought"])

	def test_get_cart_item_by_item_id(self):
		Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="1.00",
			unit="l",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.get(f"/households/{self.household.id}/cart/{self.catalog_item.id}")

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertIn("cart", res.data)
		self.assertEqual(len(res.data["cart"]), 1)

	def test_patch_cart_row(self):
		row = Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="1.00",
			unit="pieces",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.patch(
			f"/households/{self.household.id}/cart/row/{row.id}",
			{"qty_needed": "4.75", "is_bought": True},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_200_OK)
		row.refresh_from_db()
		self.assertEqual(str(row.qty_needed), "4.75")
		self.assertTrue(row.is_bought)

	def test_patch_cart_row_rejects_non_positive_value(self):
		row = Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="1.00",
			unit="pieces",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="owner1", password="pass12345"))

		res = self.client.patch(
			f"/households/{self.household.id}/cart/row/{row.id}",
			{"qty_needed": "0"},
			format="json",
		)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		row.refresh_from_db()
		self.assertEqual(str(row.qty_needed), "1.00")

	def test_delete_cart_row(self):
		row = Cart.objects.create(
			household=self.household,
			item=self.catalog_item,
			qty_needed="1.00",
			unit="pieces",
			is_bought=False,
		)
		self.assertTrue(self.client.login(username="member1", password="pass12345"))

		res = self.client.delete(f"/households/{self.household.id}/cart/row/{row.id}")

		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Cart.objects.filter(id=row.id).exists())
