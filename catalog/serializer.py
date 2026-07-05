from rest_framework import serializers
from catalog.models import Catalog

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ["item_name", "item_type"]
    
    def validate_item_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("item name cannot be empty")
        return value
    
    def validate(self, attrs):
        household = self.context.get("household")
        item_name = attrs.get("item_name")

        if household is None:
            raise serializers.ValidationError("Household context is needed")
        # If item_name not in PATCH
        if not item_name:
            return attrs
        
        duplicate_qs = Catalog.objects.filter(
            household=household,
            item_name__iexact=item_name,
        )

        # If a PATCH, then exclude instance for 
        # duplicate check
        if self.instance is not None:
            duplicate_qs = duplicate_qs.exclude(id=self.instance.id)

        if duplicate_qs.exists():
            raise serializers.ValidationError(
                "This item already exists in the household"
            )
        return attrs
    
    def create(self, validated_data):
        household = self.context["household"]
        return Catalog.objects.create(
            household=household,
            **validated_data
        )