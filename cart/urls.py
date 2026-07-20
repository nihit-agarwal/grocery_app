from django.urls import path
from cart.views import (
    CartAddView,
    CartListView,
    CartItemDetailView,
    CartUpdateView,
)

urlpatterns = [
    path("households/<uuid:household_id>/cart", CartAddView.as_view(), name="cart-add"),
    path("households/<uuid:household_id>/cart/all", CartListView.as_view(), name="cart-list"),
    path("households/<uuid:household_id>/catalog/<uuid:item_id>/cart", CartItemDetailView.as_view(), name="cart-item-detail"),
    path("households/<uuid:household_id>/cart/<uuid:cart_row_id>", CartUpdateView.as_view(), name="cart-row-update"),
]