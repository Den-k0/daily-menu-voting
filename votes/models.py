from django.db import models

from restaurants.models import Menu
from users.models import Employee


class Vote(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("employee", "menu")

    def __str__(self):
        return (f"{self.employee.email} voted for"
                f"{self.menu.restaurant.name} on {self.menu.date}")
