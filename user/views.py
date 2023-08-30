from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import CustomerSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Create a new customer",
        description="Create a new customer with provided details.",
    ),
)
class CreateCustomerView(generics.CreateAPIView):
    serializer_class = CustomerSerializer


@extend_schema_view(
    get=extend_schema(
        summary="Retrieve the current user",
        description="Retrieve credentials of the current authenticated user."
        "information.",
    ),
    put=extend_schema(
        summary="Update the current user",
        description="Update credentials of the current authenticated user.",
    ),
    patch=extend_schema(
        summary="Partial update the current user",
        description="Partial update credentials of the current authenticated "
                    "user.",
    ),
)
class ManageCustomerView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
