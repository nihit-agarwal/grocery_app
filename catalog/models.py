from django.db import models
import uuid

# Create your models here.
class Catalog(models.Model):
    class ItemType(models.TextChoices):
        FROZEN = "frozen", "Frozen"
        DAIRY = "dairy", "Dairy"
        PULSES = "pulses", "Pulses"
        MISCELLANEOUS = "miscellaneous", "Miscellaneous"
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    item_name = models.CharField(max_length=120)

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="catalog_items",
    )

    item_type = models.CharField(max_length=50, 
                            choices=ItemType.choices,
                            default=ItemType.MISCELLANEOUS)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item_name", "household"],
                name="uniq_household_item",
            )
        ]

    def __str__(self):
        return f"{self.item_name} in {self.household.id}"