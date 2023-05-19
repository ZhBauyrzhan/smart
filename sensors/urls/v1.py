from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sensors.views import SensorViewSet, MeasurementViewSet, new_measure

router = DefaultRouter()
router.register('sensors', SensorViewSet, basename='sensor')
router.register('measurements', MeasurementViewSet, basename='measurement')

urlpatterns = [
    path('', include(router.urls))
]
