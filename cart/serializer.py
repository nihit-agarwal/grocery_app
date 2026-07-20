from rest_framework import serializers
from cart.models import Cart

class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["item", "qty_needed", "unit"]
    
    def validate(self, attrs):
        household = self.context.get("household")

        # Cannot perform updates without household
        if household is None:
            raise serializers.ValidationError("Household context is needed")
     
        item = attrs.get("item")
        if item.household_id != household.id:
            raise serializers.ValidationError("The item does not belong to your catalog")


    
        

        # Ensure that same item_id, household, expiry_date,
        # purchased_on  does not exist
        # already
        duplicate_qs = Cart.objects.filter(
            household=household,
            item = item
        )

        if duplicate_qs.exists():
            raise serializers.ValidationError(
                "The item already exists in cart. Update the qty for it."
            )
        
        return attrs
    
    
    def create(self, validated_data):
        household = self.context["household"]
        return Cart.objects.create(
            household=household,
            **validated_data
        )

class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["qty_needed", "is_bought"]
    
