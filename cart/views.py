from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from households.permissions import IsHouseholdMember
from rest_framework import status
from rest_framework.response import Response
from households.models import Household
from cart.models import Cart
from cart.serializer import CartAddSerializer, CartUpdateSerializer

# Create your views here.
class CartAddView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def post(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        serializer = CartAddSerializer(
            data = request.data,
            context = {"household": household}
        )

        serializer.is_valid(raise_exception=True)
        cart_row = serializer.save()

        return Response(
            {
                "row_id": str(cart_row.id),
                "household_id": str(cart_row.household_id),
                "item_id": str(cart_row.item.id),
                "quantity": cart_row.qty_needed,
                "unit": cart_row.unit,
                "is_bought": cart_row.is_bought,

            },
            status=status.HTTP_201_CREATED,
        )

class CartListView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]
    def get(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        cart = Cart.objects.filter(
            household_id = household_id
        )

        # Get the item name
        


        data = [
            {
                "row_id": str(row.id),
                "household_id": str(row.household_id),
                "item_id": str(row.item.id),
                "item_name": row.item.item_name,
                "quantity": row.qty_needed,
                "unit": row.unit,
                "is_bought": row.is_bought

            }
            for row in cart
        ]

        return Response({"cart": data}, status=status.HTTP_200_OK)
    


class CartItemDetailView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def get(self, request, household_id, item_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        cart = Cart.objects.filter(
            household_id = household_id,
            item_id = item_id
        )

        data = [
            {
                "row_id": str(row.id),
                "household_id": str(row.household_id),
                "item_id": str(row.item.id),
                "item_name": row.item.item_name,
                "quantity": row.qty_needed,
                "unit": row.unit,
                "is_bought": row.is_bought

            }
            for row in cart
        ]

        return Response({"cart": data}, status=status.HTTP_200_OK)
    



class CartUpdateView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def patch(self, request, household_id, cart_row_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        row = get_object_or_404(
            Cart, id=cart_row_id, household=household
            )
        
        serializer = CartUpdateSerializer(
            row,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        row = serializer.save()

        return Response (
            {
                "row_id": str(row.id),
                "household_id": str(row.household_id),
                "item_id": str(row.item.id),
                "quantity": row.qty_needed,
                "unit": row.unit,
                "is_bought": row.is_bought,

            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, household_id, cart_row_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        row = get_object_or_404(
            Cart, id=cart_row_id, household=household
            )
        row.delete()

        return Response(status=status.HTTP_204_NO_CONTENT,)
        

        