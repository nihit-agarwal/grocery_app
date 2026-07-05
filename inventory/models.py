from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid 

# Create your models here.
class Inventory(models.Model):
    class UnitType(models.TextChoices):
        G = "g"
        KG = "kg"
        L =  "l"
        ML = "ml"
        PC = "pieces"
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="inventory_items",
    )

    item = models.ForeignKey(
        "catalog.Catalog",
        on_delete=models.CASCADE,
        related_name="inventory_items",
    )

    purchased_on = models.DateField()
    expiry_date = models.DateField()
    qty = models.DecimalField(max_digits=5, decimal_places=2, 
                              validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.CharField(max_length=10,
                            choices=UnitType.choices,
                            default=UnitType.PC)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["household", "item", "expiry_date", "purchased_on"],
                name="uniq_inventory_household_item",
            ),
            models.CheckConstraint(
                condition=models.Q(qty__gt=0),
                name="check_inventory_qty_gt_0",
            )
        ]
    
    def __str__(self):
        return f"{self.qty} {self.unit} of {self.item.id} in {self.household.id}"
