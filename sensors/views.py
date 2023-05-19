import requests
from rest_framework import mixins
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
        print(r.raw)
        return Response(r.json())
    return Response({'message': 'Sensor not found'}, status=404)