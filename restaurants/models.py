from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
    date = models.DateField(default=timezone.now, unique=True)
    items = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"Menu for {self.date} at {self.restaurant.name}"

    class Meta:
        unique_together = ("restaurant", "date")
