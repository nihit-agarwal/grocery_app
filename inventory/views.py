from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from households.permissions import IsHouseholdMember
from rest_framework import status
from rest_framework.response import Response
from households.models import Household
from inventory.models import Inventory
from inventory.serializer import InventoryAddSerializer, InventoryQtyUpdateSerializer

# Create your views here.
class InventoryItemAddView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def post(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        serializer = InventoryAddSerializer(
            data = request.data,
            context = {"household": household}
        )

        serializer.is_valid(raise_exception=True)
        inventory_row = serializer.save()

        return Response(
            {
                "row_id": str(inventory_row.id),
                "household_id": str(inventory_row.household_id),
                "item_id": str(inventory_row.item.id),
                "purchased_on": inventory_row.purchased_on,
                "expiry_date": inventory_row.expiry_date,
                "quantity": inventory_row.qty,
                "unit": inventory_row.unit,

            },
            status=status.HTTP_201_CREATED,
        )

class InventoryListView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]
    def get(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        inventory = Inventory.objects.filter(
            household_id = household_id
        )

        # Get the item name
        


        data = [
            {
                "row_id": str(row.id),
                "household_id": str(row.household_id),
                "item_id": str(row.item.id),
                "item_name": row.item.item_name,
                "purchased_on": row.purchased_on,
                "expiry_date": row.expiry_date,
                "quantity": row.qty,
                "unit": row.unit,

            }
            for row in inventory
        ]

        return Response({"inventory": data}, status=status.HTTP_200_OK)
    


class InventoryItemDetailView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def get(self, request, household_id, item_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)

        inventory = Inventory.objects.filter(
            household_id = household_id,
            item_id = item_id
        )

        data = [
            {
                "row_id": str(row.id),
                "household_id": str(row.household_id),
                "item_id": str(row.item.id),
                "purchased_on": row.purchased_on,
                "expiry_date": row.expiry_date,
                "quantity": row.qty,
                "unit": row.unit,

            }
            for row in inventory
        ]

        return Response({"inventory": data}, status=status.HTTP_200_OK)
    



class InventoryUpdateView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def patch(self, request, household_id, inventory_row_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        row = get_object_or_404(
            Inventory, id=inventory_row_id, household=household
            )
        
        serializer = InventoryQtyUpdateSerializer(
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
                "purchased_on": row.purchased_on,
                "expiry_date": row.expiry_date,
                "quantity": row.qty,
                "unit": row.unit,

            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, household_id, inventory_row_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        row = get_object_or_404(
            Inventory, id=inventory_row_id, household=household
            )
        row.delete()

        return Response(status=status.HTTP_204_NO_CONTENT,)
        

        