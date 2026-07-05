from django.db import models
from django.conf import settings
import uuid
# Create your models here.

class Household(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    house_name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.house_name

class HouseholdMember(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MEMBER = "member", "Member"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="household_memberships"
    )

    household = models.ForeignKey(
        "households.Household",
        on_delete=models.CASCADE,
        related_name="members",
    )


    role = models.CharField(max_length=10, 
                            choices=Role.choices,
                            default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "household"],
                name="uniq_user_household_membership",
            )
        ]
    
    def __str__(self):
        return f"{self.user.id} in {self.household.id} as {self.role}"
    

