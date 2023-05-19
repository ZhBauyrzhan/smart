from django.urls import path, include
from rest_framework.routers import DefaultRouter
from address.views import AddressViewSet

router = DefaultRouter()
router.register('address', AddressViewSet, basename='adress')

urlpatterns = [
    path('', include(router.urls)),
]
