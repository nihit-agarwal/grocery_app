from django.urls import path
from catalog.views import (
    ItemCreateView,
    CatalogListView,
    ItemDetailView
)

urlpatterns = [
    path("households/<uuid:household_id>/catalog", ItemCreateView.as_view(), name="item-create"),
    path("households/<uuid:household_id>/catalog/all", CatalogListView.as_view(), name="catalog-list" ),
    path("households/<uuid:household_id>/catalog/<uuid:item_id>", ItemDetailView.as_view(), name="item-detail"),
   
]