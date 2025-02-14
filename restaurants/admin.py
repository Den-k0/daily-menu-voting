from django.contrib import admin

from restaurants.models import Restaurant, Dish, Menu

admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Menu)
