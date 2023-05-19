import json

import requests
from rest_framework import mixins, status
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class MeasurementViewSet(ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


@api_view(['POST'])
def new_measure(request):
    data = request.data
    sensor = get_object_or_404(Sensor, **data)
    with requests.get(f'http://{sensor.ip}:{sensor.port}/') as r:
        if r.status_code == 200:
            measurement_data = {
                "data": r.json(),
                "sensor": sensor.id,
            }
            serializer = MeasurementSerializer(data=measurement_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)
