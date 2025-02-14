from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from votes.models import Vote
from votes.serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Vote.objects.all()
        return Vote.objects.filter(employee=self.request.user)

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)

    def create(self, request, *args, **kwargs):
        menu_id = request.data.get("menu")
        if Vote.objects.filter(employee=request.user, menu_id=menu_id).exists():
            return Response({"detail": "You have already voted for this menu."}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to delete votes."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
