from django.urls import path, include
from rest_framework.routers import DefaultRouter

from restaurants.views import (
    RestaurantViewSet,
    MenuViewSet,
)

router = DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "restaurants"
