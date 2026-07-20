from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import Inventory
import uuid

# Create your models here.
class Cart(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    unit = models.CharField(
        max_length=10,
        choices=Inventory.UnitType.choices,
        default=Inventory.UnitType.PC
    )

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    item = models.ForeignKey(
        "catalog.Catalog",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )

    qty_needed = models.DecimalField(max_digits=5, decimal_places=2, 
                              validators=[MinValueValidator(Decimal("0.01"))])
    
    is_bought = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["household", "item"],
                name="uniq_cart_household_item",
            ),
            models.CheckConstraint(
                condition=models.Q(qty_needed__gt=0),
                name="check_cart_qty_gt_0",
            )
        ]
    
    def __str__(self):
        return f" {'Bought' if self.is_bought else 'To buy'} {self.qty_needed} {self.unit} of {self.item.id} in {self.household.id}"


