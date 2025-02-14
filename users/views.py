from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import EmployeeSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = EmployeeSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
