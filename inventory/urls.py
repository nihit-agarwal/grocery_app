from django.urls import path
from inventory.views import (
    InventoryItemAddView,
    InventoryListView,
    InventoryItemDetailView,
    InventoryUpdateView
)

urlpatterns = [
    path("households/<uuid:household_id>/inventory", InventoryItemAddView.as_view(), name="inventory-item-add"),
    path("households/<uuid:household_id>/inventory/all", InventoryListView.as_view(), name="inventory-list"),
    path("households/<uuid:household_id>/catalog/<uuid:item_id>/inventory", InventoryItemDetailView.as_view(), name="inventory-item-get"),
    path("households/<uuid:household_id>/inventory/<uuid:inventory_row_id>", InventoryUpdateView.as_view(), name="inventory-row-update"),

]