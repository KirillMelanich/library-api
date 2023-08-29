from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from book.views import BookViewSet
from user.views import CreateCustomerView, ManageCustomerView

app_name = "book"

router = DefaultRouter()
router.register("", BookViewSet)

urlpatterns = router.urls