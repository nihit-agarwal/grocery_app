from rest_framework import serializers
from inventory.models import Inventory

class InventoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["item", "purchased_on", "expiry_date", "qty", "unit"]
    
    def validate(self, attrs):
        household = self.context.get("household")

        # Cannot perform updates without household
        if household is None:
            raise serializers.ValidationError("Household context is needed")
     
        item = attrs.get("item")
        if item.household_id != household.id:
            raise serializers.ValidationError("The item does not belong to your catalog")


        # Ensure that expiry date >= purchased_on
        expiry_date = attrs.get("expiry_date")
        purchase_date = attrs.get("purchased_on")

        
        if purchase_date > expiry_date:
            raise serializers.ValidationError("Purchase date cannot be after expiry")
        

        # Ensure that same item_id, household, expiry_date,
        # purchased_on  does not exist
        # already
        duplicate_qs = Inventory.objects.filter(
            household=household,
            item = item,
            expiry_date = expiry_date,
            purchased_on = purchase_date,
        )

        if duplicate_qs.exists():
            raise serializers.ValidationError(
                "The batch already exists in inventory. Update the qty for it."
            )
        
        return attrs
    
    
    def create(self, validated_data):
        household = self.context["household"]
        return Inventory.objects.create(
            household=household,
            **validated_data
        )

class InventoryQtyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["qty"]
