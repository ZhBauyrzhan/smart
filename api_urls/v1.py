from django.urls import path, include

urlpatterns = [
    path('', include('users.urls.v1')),
    path('', include('address.urls.v1')),
    path('', include('sensors.urls.v1')),
]