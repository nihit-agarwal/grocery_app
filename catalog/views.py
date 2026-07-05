from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from households.models import Household
from rest_framework.permissions import IsAuthenticated
from households.permissions import IsHouseholdMember
from catalog.serializer import ItemCreateSerializer
from catalog.models import Catalog


# Create your views here.
class ItemCreateView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def post(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        serializer = ItemCreateSerializer(
            data = request.data,
            context = {"household": household}
        )
        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        return Response(
            {
                "item_id": str(item.id),
                "item_name": item.item_name,
                "item_type": item.item_type,
                "household_id": str(item.household_id),
                "created_at": item.created_at

            },
            status=status.HTTP_201_CREATED,
        )

class CatalogListView(APIView):
    permission_classes=[IsAuthenticated, IsHouseholdMember]

    def get(self, request, household_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        items = Catalog.objects.filter(
            household_id = household_id
        )

        data = [
            {
                "item_name": item.item_name,
                "item_type": item.item_type,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ]

        return Response({"items": data}, status=status.HTTP_200_OK)
    

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated, IsHouseholdMember]

    def get(self, request, household_id, item_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        item = get_object_or_404(Catalog, id=item_id, household=household)

        
        return Response(
             {
                "item_name": item.item_name,
                "item_type": item.item_type,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, household_id, item_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        item = get_object_or_404(Catalog, id=item_id, household=household)

        serializer = ItemCreateSerializer(
            item,
            data=request.data,
            context= {"household": household},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        item = serializer.save()

        return Response(
            {
                "item_id": str(item.id),
                "item_name": item.item_name,
                "item_type": item.item_type,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, household_id, item_id):
        household = get_object_or_404(Household, id=household_id)
        self.check_object_permissions(request, household)
        
        item = get_object_or_404(Catalog, id=item_id, household=household)
        item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT,)
