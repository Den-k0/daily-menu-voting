from rest_framework import serializers

from restaurants.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("id", "name")


class MenuSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all()
    )
    date = serializers.DateField()

    class Meta:
        model = Menu
        fields = ("id", "restaurant", "items", "date")
