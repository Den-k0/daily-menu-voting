from rest_framework import viewsets

from restaurants.models import Restaurant, Menu
from restaurants.permissions import IsAdminOrIfAuthenticatedReadOnly
from restaurants.serializers import RestaurantSerializer, MenuSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
