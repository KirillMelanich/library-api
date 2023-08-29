from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import CustomerSerializer


class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


class ManageCustomerView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
