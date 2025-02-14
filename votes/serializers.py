from django.utils import timezone
from rest_framework import serializers

from restaurants.models import Menu
from users.serializers import EmployeeSerializer
from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("menu", "created_at")

    def validate(self, data):
        request = self.context["request"]
        if Vote.objects.filter(employee=request.user, menu=data["menu"]).exists():
            raise serializers.ValidationError("You have already voted for this menu.")

        if data["menu"].date != timezone.now().date():
            raise serializers.ValidationError("Voting is only allowed for today's menu.")

        return data
