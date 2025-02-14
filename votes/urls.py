from django.urls import path, include
from rest_framework.routers import DefaultRouter

from votes.views import (
    VoteViewSet,
)

router = DefaultRouter()
router.register("votes", VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "votes"
